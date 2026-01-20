# 🎬 Movie Recommendation System (End-to-End)

An end-to-end **Movie Recommendation System** built using **Machine Learning (TF-IDF + Cosine Similarity)** with a **FastAPI backend** and an interactive **Streamlit frontend**.  
The system provides **content-based movie recommendations**, real-time movie search, and detailed movie information by integrating the **OMDb API**.

This project demonstrates how to take a machine learning model from **offline training to a full-stack application**.

---

## 🚀 Features

- 🔍 **Movie Search & Discovery**
  - Search movies by title with real-time results
  - Fetch movie posters and metadata using OMDb API

- 🤖 **Content-Based Recommendation Engine**
  - TF-IDF vectorization on movie metadata
  - Cosine similarity for finding similar movies

- ⚡ **FastAPI Backend**
  - Clean REST APIs for search, details, and recommendations
  - Handles ML inference and API integration

- 🎨 **Streamlit Frontend**
  - Interactive UI for searching and exploring movies
  - Displays posters, details, and recommendations

- 🧠 **Optimized for Performance**
  - Precomputed TF-IDF matrix
  - Pickle-based model and data loading

---

## 🛠️ Tech Stack

**Programming Language**
- Python

**Machine Learning**
- TF-IDF Vectorization
- Cosine Similarity
- Scikit-learn

**Backend**
- FastAPI
- HTTPX
- Pydantic

**Frontend**
- Streamlit

**Data & Utilities**
- Pandas
- NumPy
- Pickle

**External API**
- OMDb API (movie metadata & posters)

---

## 🧩 Project Architecture



├── app.py # Streamlit frontend
├── main.py # FastAPI backend
├── df.pkl # Movie dataset
├── tfidf.pkl # TF-IDF vectorizer
├── tfidf_matrix.pkl # TF-IDF matrix
├── indices.pkl # Title-to-index mapping
├── .env # API keys
└── README.md


---

## 🔄 How the System Works

1. User searches for a movie using the Streamlit UI  
2. FastAPI fetches movie metadata from OMDb  
3. The selected movie title is matched with the local dataset  
4. TF-IDF vectors are compared using cosine similarity  
5. Similar movies are recommended and enriched with metadata  
6. Results are displayed back in the frontend  

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository

git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system

2️⃣ Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up environment variables

Create a .env file in the root directory:

OMDB_API_KEY=your_api_key_here

5️⃣ Start the FastAPI backend
uvicorn main:app --reload

6️⃣ Run the Streamlit app
streamlit run app.py


Open browser at:

http://localhost:8501

🎯 Use Cases

Learning content-based recommendation systems

Understanding ML model deployment

Building full-stack ML applications

Portfolio project for AI/ML, Data Science, Python Backend roles

📌 Key Learning Outcomes

Implemented a real-world recommendation engine

Integrated machine learning with REST APIs

Built an end-to-end ML pipeline

Worked with external APIs and frontend integration

Followed production-style project structure

🚧 Future Improvements

Add user-based or hybrid recommendations

Improve ranking using weighted similarity

Add caching for API responses

Deploy on cloud platforms (Render / AWS / Railway)

👤 Author

Shivam Rustagi
Aspiring AI / Machine Learning Engineer
GitHub: https://github.com/shivamrustagi03

⭐ If you found this project useful, feel free to star the repository!
