import streamlit as st
import pickle
import requests
import time


def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8ec7ed039e3c3d87c311d91dbcf255e8"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching movie poster for ID {movie_id}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movie_dict[movie_dict['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x:x[1])[1:6]

    recomended_movies = []
    movies_poster = []
    for i in movies_list:
        movie_id = movie_dict.iloc[i[0]].movie_id
        #fetch poster form API
        recomended_movies.append(movie_dict.iloc[i[0]].title)
        movies_poster.append(fetch_poster(movie_id))
        time.sleep(0.3)
    return recomended_movies, movies_poster

movie_dict = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movie_dict['title'].values

st.title('Movie Recommender System')

option = st.selectbox(
    "How would you like to be contacted?",
    movie_list,
    index=None,
    placeholder="Select movie",
)

if st.button('Recommend') and option is not None:
    names, posters = recommend(option)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
else:
    st.warning("Please select a movie first.")