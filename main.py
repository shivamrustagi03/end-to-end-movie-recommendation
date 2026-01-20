import os
import pickle
from typing import Optional, List, Dict, Any, Tuple

import numpy as np
import pandas as pd
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from contextlib import asynccontextmanager

# =========================
# ENV
# =========================
load_dotenv(".env")
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY not found in .env")

OMDB_BASE = "http://www.omdbapi.com/"

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DF_PATH = os.path.join(BASE_DIR, "df.pkl")
INDICES_PATH = os.path.join(BASE_DIR, "indices.pkl")
TFIDF_MATRIX_PATH = os.path.join(BASE_DIR, "tfidf_matrix.pkl")
TFIDF_PATH = os.path.join(BASE_DIR, "tfidf.pkl")

df = None
tfidf_matrix = None
TITLE_TO_IDX = None

# =========================
# MODELS
# =========================
class OMDBMovieCard(BaseModel):
    tmdb_id: int
    title: str
    poster_url: Optional[str]
    release_date: Optional[str]
    vote_average: Optional[float] = None


class OMDBMovieDetails(BaseModel):
    tmdb_id: int
    title: str
    overview: Optional[str]
    release_date: Optional[str]
    poster_url: Optional[str]
    backdrop_url: Optional[str] = None
    genres: List[dict] = []


class TFIDFRecItem(BaseModel):
    title: str
    score: float
    tmdb: Optional[OMDBMovieCard] = None


class SearchBundleResponse(BaseModel):
    query: str
    movie_details: OMDBMovieDetails
    tfidf_recommendations: List[TFIDFRecItem]
    genre_recommendations: List[OMDBMovieCard]

# =========================
# UTILS
# =========================
def _norm_title(t: str) -> str:
    return str(t).strip().lower()


def imdb_to_int(imdb_id: str) -> int:
    return int(imdb_id.replace("tt", ""))


async def omdb_get(params: Dict[str, Any]) -> Dict[str, Any]:
    params["apikey"] = OMDB_API_KEY
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(OMDB_BASE, params=params)
    if r.status_code != 200:
        raise HTTPException(502, r.text)
    return r.json()


# =========================
# OMDB HELPERS
# =========================
async def omdb_search(query: str, page: int = 1):
    return await omdb_get({"s": query, "type": "movie", "page": page})


async def omdb_search_first(query: str):
    data = await omdb_search(query)
    results = data.get("Search", [])
    return results[0] if results else None


async def omdb_movie_details(imdb_id: str) -> OMDBMovieDetails:
    data = await omdb_get({"i": imdb_id, "plot": "full"})
    return OMDBMovieDetails(
        tmdb_id=imdb_to_int(imdb_id),
        title=data.get("Title"),
        overview=data.get("Plot"),
        release_date=data.get("Released"),
        poster_url=None if data.get("Poster") == "N/A" else data.get("Poster"),
        genres=[{"name": g} for g in (data.get("Genre") or "").split(", ") if g],
    )


# =========================
# TF-IDF
# =========================
def build_title_map(indices):
    return {_norm_title(k): int(v) for k, v in indices.items()}


def tfidf_recommend_titles(title: str, top_n: int):
    idx = TITLE_TO_IDX.get(_norm_title(title))
    if idx is None:
        return []
    scores = (tfidf_matrix @ tfidf_matrix[idx].T).toarray().ravel()
    order = np.argsort(-scores)

    out = []
    for i in order:
        if i == idx:
            continue
        out.append((df.iloc[i]["title"], float(scores[i])))
        if len(out) >= top_n:
            break
    return out


async def attach_card(title: str):
    m = await omdb_search_first(title)
    if not m:
        return None
    return OMDBMovieCard(
        tmdb_id=imdb_to_int(m["imdbID"]),
        title=m["Title"],
        poster_url=None if m["Poster"] == "N/A" else m["Poster"],
        release_date=m.get("Year"),
    )


# =========================
# STARTUP
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    global df, tfidf_matrix, TITLE_TO_IDX

    with open(DF_PATH, "rb") as f:
        df = pickle.load(f)
    with open(INDICES_PATH, "rb") as f:
        TITLE_TO_IDX = build_title_map(pickle.load(f))
    with open(TFIDF_MATRIX_PATH, "rb") as f:
        tfidf_matrix = pickle.load(f)
    yield

app = FastAPI(title="Movie Recommender API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTES
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/home", response_model=List[OMDBMovieCard])
async def home(category: str = "trending", limit: int = 24):
    keyword_map = {
        "trending": "avengers",
        "popular": "batman",
        "top_rated": "godfather",
        "now_playing": "2024",
        "upcoming": "2025",
    }
    keyword = keyword_map.get(category, "movie")
    data = await omdb_search(keyword)
    cards = []
    for m in data.get("Search", [])[:limit]:
        cards.append(
            OMDBMovieCard(
                tmdb_id=imdb_to_int(m["imdbID"]),
                title=m["Title"],
                poster_url=None if m["Poster"] == "N/A" else m["Poster"],
                release_date=m.get("Year"),
            )
        )
    return cards


@app.get("/tmdb/search")
async def tmdb_search(query: str):
    return await omdb_search(query)


@app.get("/movie/id/{tmdb_id}", response_model=OMDBMovieDetails)
async def movie_details_route(tmdb_id: int):
    return await omdb_movie_details(f"tt{tmdb_id}")


@app.get("/recommend/tfidf")
async def recommend_tfidf(title: str, top_n: int = 10):
    return [{"title": t, "score": s} for t, s in tfidf_recommend_titles(title, top_n)]


@app.get("/movie/search", response_model=SearchBundleResponse)
async def search_bundle(query: str, tfidf_top_n: int = 12):
    best = await omdb_search_first(query)
    if not best:
        raise HTTPException(404, "Movie not found")

    details = await omdb_movie_details(best["imdbID"])

    tfidf_items = []
    for t, s in tfidf_recommend_titles(details.title, tfidf_top_n):
        card = await attach_card(t)
        tfidf_items.append(TFIDFRecItem(title=t, score=s, tmdb=card))

    return SearchBundleResponse(
        query=query,
        movie_details=details,
        tfidf_recommendations=tfidf_items,
        genre_recommendations=[],
    )
