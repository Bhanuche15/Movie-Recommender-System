import pickle
import streamlit as st
import requests
import time

# ================================
# CONFIGURATION
# ================================
API_KEY = "c7e68e5eec8357a655818201112d742f"

# Page settings
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# Custom CSS for UI + Background Color
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); /* Dark blue-purple gradient */
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .movie-card {
        padding: 10px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.15);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        text-align: center;
        color: white;
        font-weight: bold;
        animation: fadeInUp 1s ease-in-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .movie-card:hover {
        transform: scale(1.08);
        box-shadow: 0 8px 20px rgba(0,0,0,0.7);
    }
    .stButton>button {
        background-color: #ff4b5c;
        color: white;
        border-radius: 10px;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff6b81;
        transform: scale(1.05);
    }

    @keyframes fadeInUp {
        0% {
            opacity: 0;
            transform: translateY(40px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# ================================
# FUNCTIONS
# ================================
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image"
    except Exception:
        st.warning("⚠️ Could not fetch poster for some movies.")
        return "https://via.placeholder.com/500x750.png?text=Error"
    finally:
        time.sleep(0.2)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# ================================
# STREAMLIT APP
# ================================
st.markdown("<h1 style='text-align: center; color: #FFD700;'>🎬 Movie Recommender System 🍿</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #00FFFF;'>Find the Best Movies for You!</h3>", unsafe_allow_html=True)

# Load Data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎥 Type or select a movie from the dropdown",
    movie_list
)

if st.button('✨ Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Caption for recommendations
    st.markdown("<h3 style='text-align:center; color:#FFA500;'>Your Personalized Picks! 🍿</h3>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{recommended_movie_posters[idx]}" width="150" style="border-radius:10px;"><br>
                    {recommended_movie_names[idx]}
                </div>
            """, unsafe_allow_html=True)
