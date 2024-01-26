import pandas as pd
import streamlit as st
import pickle
import requests


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # get index of the movie
    distances = similarity[movie_index]  # get similarity scores of the index
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                  0:5]  # sort top 5 similarity score of requested movie
    recommended_movies = []
    recommended_movies_poster = []
    for similar_movie in movies_list:
        recommended_movies.append(movies.iloc[similar_movie[0]].title)
        movie_id = movies.iloc[similar_movie[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9c3c54efb7377f783bbfd558dbbca66b&language=en-US'.format(movie_id))
    data = response.json()

    return "https://image.tmdb.org/t/p/original/" + data['poster_path']


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# 9c3c54efb7377f783bbfd558dbbca66b

# https://api.themoviedb.org/3/movie/{movie_id}?api_key=9c3c54efb7377f783bbfd558dbbca66b&language=en-US

st.title('Movie Recommender system (Content-Based)')


selected_movie_name = st.selectbox('How would you like to be contacted?',movies['title'].values)

if st.button('Recommend'):
    st.write(selected_movie_name)
    recommendations, posters = recommend(selected_movie_name)
    num_columns = 5
    column_names = [f"col{i}" for i in range(1, num_columns + 1)]
    columns = st.columns(num_columns)
    for i, (col_name, recommendation, poster) in enumerate(zip(column_names, recommendations, posters)):
        with columns[i]:
            container = st.container()
            container.image(poster)
            container.write(recommendation)

