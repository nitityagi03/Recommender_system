import pickle
import streamlit as st
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=779640ca3735119751135c7d7abac064&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500" + poster_path

    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse = True , key =  lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommended_movies_poster
        


st.header("MOVIE RECOMMENDATION SYSTEM")

movie_list = pickle.load(open('artificats/movie_list.pkl','rb'))
movies = pd.DataFrame(movie_list)

similarity = pickle.load(open('artificats/similarity.pkl','rb'))

selected_movie = st.selectbox(
   'Type or select a movie to get recommendation',movies['title'].values)

if st.button('Show recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    def display_movie(column, name, poster_url):
        with column:
            st.image(poster_url, width=130)  # Adjust image width
            st.markdown(f"<p style='text-align: center; width: 130px; font-weight: bold;'>{name}</p>", 
                        unsafe_allow_html=True)  # Center text & set width

    # Display each movie in its respective column
    display_movie(col1, recommended_movies_name[0], recommended_movies_poster[0])
    display_movie(col2, recommended_movies_name[1], recommended_movies_poster[1])
    display_movie(col3, recommended_movies_name[2], recommended_movies_poster[2])
    display_movie(col4, recommended_movies_name[3], recommended_movies_poster[3])
    display_movie(col5, recommended_movies_name[4], recommended_movies_poster[4])