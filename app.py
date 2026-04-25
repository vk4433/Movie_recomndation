import streamlit as st
import pickle
import pandas as pd
import requests

# =========================
# CONFIGURATION
# =========================

API_KEY = "a6380491cc65873c1435ca0b246b02e9"
POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER_IMAGE = "https://via.placeholder.com/500x750?text=No+Image"

MOVIES_PER_PAGE = 10
MOVIES_PER_ROW = 5


# =========================
# CACHE DATA LOADING
# =========================

@st.cache_data
def load_data():
    movies_dict = pickle.load(open("movie.pkl", "rb"))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity


movies, similarity = load_data()

title_col = "title" if "title" in movies.columns else movies.columns[0]

movie_index_map = pd.Series(movies.index, index=movies[title_col]).to_dict()


# =========================
# CACHE POSTER API
# =========================

@st.cache_data
def fetch_poster_by_title(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return f"{POSTER_BASE_URL}{poster_path}"

        return PLACEHOLDER_IMAGE

    except Exception:
        return PLACEHOLDER_IMAGE


# =========================
# RECOMMENDATION LOGIC
# =========================

def recommend(movie):
    if movie not in movie_index_map:
        return [], []

    movie_index = movie_index_map[movie]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[:51]

    names = []
    posters = []

    # selected movie first
    names.append(movie)
    posters.append(fetch_poster_by_title(movie))

    # recommendations
    for idx, _ in movies_list:
        if idx != movie_index:
            title = movies.iloc[idx][title_col]
            names.append(title)
            posters.append(fetch_poster_by_title(title))

    return names, posters


# =========================
# UI SETUP
# =========================

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)


# =========================
# MOVIE SELECTOR
# =========================

col1, col2 = st.columns([6, 1])

with col1:
    selected_movie_name = st.selectbox(
        "Choose a movie",
        movies[title_col].values,
        label_visibility="collapsed"
    )

    if selected_movie_name:
        st.image(fetch_poster_by_title(selected_movie_name), width=200)


with col2:
    recommend_clicked = st.button("🎯 Recommend", width="stretch")


# =========================
# SESSION STATE
# =========================

if "page" not in st.session_state:
    st.session_state.page = 1

if "names" not in st.session_state:
    st.session_state.names = []
    st.session_state.posters = []


# =========================
# HANDLE RECOMMENDATION
# =========================

if recommend_clicked:
    st.session_state.names, st.session_state.posters = recommend(selected_movie_name)
    st.session_state.page = 1


# =========================
# DISPLAY RESULTS
# =========================

if st.session_state.names:

    total_pages = (len(st.session_state.names) + MOVIES_PER_PAGE - 1) // MOVIES_PER_PAGE

    col_prev, _, col_next = st.columns([1, 8, 1])

    with col_prev:
        if st.button("⬅ Previous", width="stretch", disabled=(st.session_state.page == 1)):
            st.session_state.page -= 1

    with col_next:
        if st.button("Next ➡", width="stretch", disabled=(st.session_state.page == total_pages)):
            st.session_state.page += 1

    start = (st.session_state.page - 1) * MOVIES_PER_PAGE
    end = start + MOVIES_PER_PAGE

    page_names = st.session_state.names[start:end]
    page_posters = st.session_state.posters[start:end]

    for i in range(0, len(page_names), MOVIES_PER_ROW):
        cols = st.columns(MOVIES_PER_ROW)

        for j, col in enumerate(cols):
            idx = i + j

            if idx < len(page_names):
                with col:
                    st.image(page_posters[idx], use_container_width=True)
                    st.markdown(
                        f"<p style='text-align:center'>{page_names[idx]}</p>",
                        unsafe_allow_html=True
                    )