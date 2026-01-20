import requests
import streamlit as st

# =============================
# BACKEND API (YOUR FASTAPI)
# =============================
API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# STYLES (minimal modern)
# =============================
st.markdown(
    """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
.small-muted { color:#6b7280; font-size: 0.92rem; }
.movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
.card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.7); }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "⚠️ Backend not running! Please start FastAPI with: uvicorn main:app --reload"
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title = m.get("title", "Untitled")
            poster = m.get("poster_url")

            with colset[c]:
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button("Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True,
                )


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    # Handle OMDB response format: {"Search": [...], "totalResults": "..."}
    if isinstance(data, dict) and "Search" in data:
        raw_items = []
        for m in data.get("Search", []):
            title = (m.get("Title") or "").strip()
            imdb_id = m.get("imdbID", "")
            poster = m.get("Poster")
            year = m.get("Year", "")
            
            # Convert IMDB ID to integer (remove 'tt' prefix)
            try:
                tmdb_id = int(imdb_id.replace("tt", "")) if imdb_id else None
            except:
                tmdb_id = None
            
            if title and tmdb_id:
                raw_items.append(
                    {
                        "tmdb_id": tmdb_id,
                        "title": title,
                        "poster_url": None if poster == "N/A" else poster,
                        "release_date": year,
                    }
                )
    # Handle TMDB-style response format (fallback)
    elif isinstance(data, dict) and "results" in data:
        raw_items = []
        for m in data.get("results", []):
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster = m.get("poster_path")
            if title and tmdb_id:
                raw_items.append(
                    {
                        "tmdb_id": int(tmdb_id),
                        "title": title,
                        "poster_url": poster,
                        "release_date": m.get("release_date", ""),
                    }
                )
    elif isinstance(data, list):
        raw_items = [
            {
                "tmdb_id": m.get("tmdb_id"),
                "title": m.get("title"),
                "poster_url": m.get("poster_url"),
                "release_date": m.get("release_date", ""),
            }
            for m in data
            if m.get("tmdb_id") and m.get("title")
        ]
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"],
            "title": x["title"],
            "poster_url": x["poster_url"],
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards



# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    st.markdown("### 🏠 Home Feed")
    home_category = st.selectbox(
        "Category",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 6)

# =============================
# HEADER
# =============================
st.title("🎬 Movie Recommender")
st.markdown(
    "<div class='small-muted'>Search → Select → Details → Recommendations</div>",
    unsafe_allow_html=True,
)
st.divider()

# =============================
# VIEW: HOME
# =============================
if st.session_state.view == "home":
    typed = st.text_input("Search movie", placeholder="avengers, batman, love...")

    st.divider()

    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("Type at least 2 characters.")
        else:
            data, err = api_get_json("/tmdb/search", {"query": typed.strip()})
            if err:
                st.error(err)
            else:
                suggestions, cards = parse_tmdb_search_to_cards(data, typed.strip())

                if suggestions:
                    labels = ["-- Select --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("Suggestions", labels)
                    if selected != "-- Select --":
                        goto_details(dict(suggestions)[selected])

                st.markdown("### Results")
                poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    st.markdown(f"### 🏠 {home_category.title()}")
    home_cards, err = api_get_json("/home", {"category": home_category, "limit": 24})
    if err:
        st.error(err)
    else:
        poster_grid(home_cards, cols=grid_cols, key_prefix="home")

# =============================
# VIEW: DETAILS
# =============================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        goto_home()

    if st.button("← Back"):
        goto_home()

    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err:
        st.error(err)
        st.stop()

    left, right = st.columns([1, 2.5])
    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
    with right:
        st.markdown(f"## {data.get('title')}")
        st.write(data.get("overview") or "No overview.")

    st.divider()
    st.markdown("### Recommendations")

    bundle, err = api_get_json("/movie/search", {"query": data["title"]})
    if err:
        st.warning(f"Could not load recommendations: {err}")
    elif bundle:
        st.markdown("#### 🔎 Similar Movies")
        poster_grid(
            to_cards_from_tfidf_items(bundle["tfidf_recommendations"]),
            cols=grid_cols,
            key_prefix="tfidf",
        )
        st.markdown("#### 🎭 Genre Based")
        poster_grid(
            bundle["genre_recommendations"],
            cols=grid_cols,
            key_prefix="genre",
        )
