import streamlit as st
import pickle
import pandas as pd
import requests

api_key = ""

movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
movies_list = movies['title'].values

similarity = pickle.load(open("similarity_scores.pkl", "rb"))


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommendation_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []
    recommended_movie_posters = []
    for movie in recommendation_list:
        movie_id = movies.iloc[movie[0]].movie_id
        recommended.append(movies.iloc[movie[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended, recommended_movie_posters


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}')
    data = response.json()
    return f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'


st.title('Movie Recommender System')

selected_movie = st.selectbox("Select a Movie", movies_list)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
