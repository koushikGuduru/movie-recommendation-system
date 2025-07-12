import streamlit as st
import pickle
import pandas as pd
import requests

# TMDB API key
TMDB_API_KEY = "a6e7b7185c0fabae8adb05afbc4d6e5e"

# Fetch poster from TMDB
def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    )
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"

# Recommendation logic
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# Streamlit UI Setup
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        color: #FF4B4B;
        margin-bottom: 30px;
    }
    .movie-title {
        font-size: 18px;
        font-weight: 600;
        text-align: center;
        margin-top: 8px;
        color: #333333;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)

# Movie selection
selected_movie_name = st.selectbox("🎥 Select a movie you like:", movies['title'].values)

# Show recommendations
if st.button("🔍 Recommend Movies"):
    names, posters = recommend(selected_movie_name)

    st.markdown("---")
    st.markdown("### 🎯 Click a poster to search on Google")
    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            search_url = f"https://www.google.com/search?q={names[i].replace(' ', '+')}+movie"
            html = f"""
                <a href="{search_url}" target="_blank">
                    <img src="{posters[i]}" style="width:100%; border-radius: 10px;">
                </a>
                <div class="movie-title">{names[i]}</div>
            """
            st.markdown(html, unsafe_allow_html=True)
