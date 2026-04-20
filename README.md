# 🎬 CineMatch AI

> **Smart Movie Recommendations Powered by Machine Learning.**  
> A full-stack **Movie Recommendation System** built with **TF-IDF + Cosine Similarity**, featuring a **FastAPI backend** and an interactive **Streamlit frontend** for real-time movie discovery.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Machine Learning](https://img.shields.io/badge/ML-Recommendation-green)
![FastAPI](https://img.shields.io/badge/API-FastAPI-teal)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🚀 Overview

**CineMatch AI** is an end-to-end **Movie Recommendation System** that suggests similar movies based on content such as genres, keywords, and metadata.

Instead of random suggestions, the system uses **Machine Learning** techniques to understand movie similarity and recommend relevant titles instantly.

It also integrates the **OMDb API** to fetch posters, ratings, release details, and movie metadata for a polished real-world user experience.

---

## ✨ Key Highlights

✅ Content-based recommendation engine  
✅ TF-IDF vectorization + cosine similarity  
✅ FastAPI backend with REST APIs  
✅ Beautiful Streamlit frontend  
✅ Real-time movie search  
✅ Movie posters + metadata using OMDb API  
✅ Recruiter-ready full-stack ML project  
✅ Production-style modular architecture  

---

## 🎯 What This Project Demonstrates

This project showcases practical AI + software engineering skills.

### 🤖 Machine Learning Skills

- Recommendation Systems  
- TF-IDF Vectorization  
- Cosine Similarity  
- NLP-style feature engineering  
- Model serving concepts  

### 💻 Engineering Skills

- FastAPI backend development  
- REST API design  
- Frontend integration with Streamlit  
- External API integration  
- End-to-end deployment workflow  

---

## 🧠 How It Works

```text id="k4g1ds"
User Searches Movie
      ↓
Frontend Sends Request
      ↓
FastAPI Backend Processes Query
      ↓
Movie Title Matched in Dataset
      ↓
TF-IDF Vector Comparison
      ↓
Cosine Similarity Ranking
      ↓
Top Similar Movies Returned
      ↓
OMDb Metadata + Posters Added
      ↓
Displayed in Streamlit UI

⚙️ Core Features
🔍 Movie Search & Discovery
Search movies by title
Real-time suggestions
Detailed metadata results

🤖 Recommendation Engine
TF-IDF on movie metadata
Cosine similarity ranking
Similar movie suggestions instantly

⚡ FastAPI Backend
Clean REST APIs
Fast inference responses
Handles recommendation logic

🎨 Streamlit Frontend
Interactive UI
Poster-based display
Smooth browsing experience

🧠 Optimized Performance
Precomputed similarity features
Pickle-based fast loading
Lightweight architecture

🛠️ Tech Stack
Programming
Python
Machine Learning
Scikit-learn
TF-IDF Vectorization
Cosine Similarity
Backend
FastAPI
Pydantic
HTTPX
Frontend
Streamlit
Data / Utilities
Pandas
NumPy
Pickle
External API
OMDb API

📂 Project Structure
.
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI backend
├── df.pkl                 # Movie dataset
├── tfidf.pkl              # TF-IDF vectorizer
├── tfidf_matrix.pkl       # TF-IDF matrix
├── indices.pkl            # Title-to-index mapping
├── .env                   # API keys
├── requirements.txt
└── README.md

⚙️ Installation
Clone Repository
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
Create Virtual Environment
python -m venv .venv
Activate Environment

Windows

.venv\Scripts\activate

Mac / Linux

source .venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Configure API Key

Create .env

OMDB_API_KEY=your_api_key_here
Start Backend
uvicorn main:app --reload
Start Frontend
streamlit run app.py

Open in browser:

http://localhost:8501

💡 Example Use Cases
Recommend movies similar to Inception
Search by movie title
Explore genres and metadata
Learn how recommendation systems work
Full-stack ML portfolio showcase

🔮 Future Improvements
Collaborative filtering recommendations
Hybrid recommendation engine
Personalized user accounts
Better ranking algorithms
Redis caching for API calls
Cloud deployment (AWS / Render / Railway)
User watchlists & favorites
Dockerized deployment

👨‍💻 Author

Shivam Rustagi
AI Engineer | Data Science | Python Developer

🔗 GitHub: https://github.com/shivamrustagi03
