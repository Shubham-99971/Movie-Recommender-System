import streamlit as st
import pickle
import pandas as pd
import requests

#for background image-------------------------------------
import base64
import mimetypes
def set_background(image):
    mime_type = mimetypes.guess_type(image)[0] or "image/png"

    with open(image, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)),
                url("data:{mime_type};base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        h1, label, p, div {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

#bg image code ends here------------------------------- 

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters =[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id ))
    return recommended_movies,recommended_movies_posters                                                  


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

set_background("image.png")
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3 ,col4, col5= st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])    
    with col5:
        st.text(names[4])
        st.image(posters[4])

