# Movie Recommendation System

A content-based movie recommendation web app built with Streamlit. Select any movie and get up to 50 similar recommendations with posters fetched live from the TMDB API.

# Streamlit app 
``` bash 
https://movierecomndation-pc4w6xzckhkkkazbkfvuib.streamlit.app/

```

## Demo

- Choose a movie from the dropdown
- Click **Recommend**
- Browse results paginated 10 per page (5 per row)

## How It Works

The model uses **content-based filtering**:

1. Merges `movies.csv` and `credits.csv` from the TMDB 5000 dataset
2. Extracts features: genres, keywords, top-5 cast members, director
3. Combines them into a single `tags` string per movie
4. Applies **Porter Stemming** (NLTK) and vectorizes with `CountVectorizer` (5000 features)
5. Computes **cosine similarity** across all 1500 movies
6. At query time, returns the top-N closest movies by similarity score

Precomputed data is stored in `movie.pkl` and `similarity.pkl` so the app loads instantly.

## Project Structure

```
Movie_recomndation/
├── app.py              # Streamlit web app
├── model.ipynb         # Data processing & model training notebook
├── movie.pkl           # Serialized movie DataFrame
├── similarity.pkl      # Precomputed cosine similarity matrix
├── requirements.txt    # Python dependencies
└── data/
    ├── movies.csv      # TMDB 5000 movies metadata
    └── credits.csv     # Cast and crew data
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/vk4433/Movie_recomndation
cd Movie_recomndation
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web UI |
| `pandas` | Data manipulation |
| `numpy` | Numerical operations |
| `scikit-learn` | CountVectorizer, cosine similarity |
| `nltk` | Porter Stemmer |
| `requests` | TMDB API calls for posters |

## Dataset

[TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — `movies.csv` and `credits.csv`. Place both files inside the `data/` folder before running the notebook.

## Retraining the Model

Open `model.ipynb` and run all cells. This regenerates `movie.pkl` and `similarity.pkl`.

## API Key

The app uses the TMDB API to fetch movie posters. The key is set in `app.py`:


Get a free key at [themoviedb.org](https://www.themoviedb.org/settings/api).


## License

[MIT](LICENSE)
