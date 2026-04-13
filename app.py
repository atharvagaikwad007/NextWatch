import streamlit as st
import pickle
import requests
import json
import os
from datetime import datetime
import streamlit.components.v1 as components


# CONFIG & STYLING

st.set_page_config(page_title="NextWatch", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html, body, [class*="css"] {
    background: #111111;
}

.main {
    background: #111111;
    padding-top: 2rem;
}

.stApp {
    background: #111111;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: #282A3A;
    border-right: 2px solid #735F32;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: #282A3A;
}

/* Title Styling */
.title {
    font-size: 72px;
    font-weight: 900;
    color: #C69749;
    text-align: center;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.subtitle {
    font-size: 18px;
    color: #b0b0b0;
    text-align: center;
    margin-bottom: 30px;
    font-weight: 300;
    letter-spacing: 1px;
}

/* Movie Card Wrapper - FIXED CONTAINER */
.movie-card-wrapper {
    background: rgba(198, 151, 73, 0.08);
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
    display: flex;
    flex-direction: column;
    height: 100%;
}

.movie-card-wrapper:hover {
    transform: translateY(-8px);
    background: rgba(198, 151, 73, 0.15);
}

.movie-image-container {
    width: 100%;
    overflow: hidden;
    flex-shrink: 0;
}

.movie-image-container img {
    width: 100%;
    height: auto;
    display: block;
}

.movie-title-container {
    padding: 12px 10px;
    flex-grow: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 50px;
    background: rgba(17, 17, 17, 0.5);
}

.movie-title {
    font-weight: 600;
    font-size: 13px;
    color: #C69749;
    text-align: center;
    line-height: 1.4;
    word-wrap: break-word;
}

/* Section Headers */
.section-header {
    font-size: 28px;
    font-weight: 700;
    color: #C69749;
    margin-top: 40px;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 2px solid #735F32;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* Button Styling */
.stButton button {
    background: #735F32;
    color: #C69749;
    border: 2px solid #735F32;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stButton button:hover {
    background: #C69749;
    color: #111111;
    border: 2px solid #C69749;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(198, 151, 73, 0.5);
}

.stButton button:active {
    transform: translateY(0);
}

/* Input Fields */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stMultiSelect > div > div > div {
    background: rgba(115, 95, 50, 0.15) !important;
    border: 2px solid #735F32 !important;
    color: #C69749 !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

.stTextInput > div > div > input::placeholder {
    color: #735F32 !important;
}

/* Sidebar Profile Section */
.sidebar-header {
    font-size: 24px;
    font-weight: 700;
    color: #C69749;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 2px solid #735F32;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.profile-section {
    backdrop-filter: blur(10px);
}

.profile-info {
    background: rgba(115, 95, 50, 0.15);
    border-radius: 10px;
    padding: 15px;
    margin-top: 10px;
    border-left: 4px solid #C69749;
    color: #e8e8e8;
    font-weight: 500;
}

/* Divider */
.divider {
    border: 0;
    height: 2px;
    background: #735F32;
    margin: 30px 0;
}

/* Details Section */
.details-container {
    border-radius: 15px;
    backdrop-filter: blur(10px);
    margin: 30px 0;
}

.details-title {
    font-size: 32px;
    font-weight: 700;
    color: #C69749;
    margin-bottom: 25px;
    text-transform: uppercase;
    border-bottom: 2px solid #735F32;
    padding-bottom: 15px;
}

.details-info {
    color: #e8e8e8;
    font-size: 16px;
    margin-bottom: 15px;
    line-height: 1.8;
}

.details-info-label {
    color: #C69749;
    font-weight: 600;
}

.details-overview {
    color: #d0d0d0;
    font-size: 15px;
    line-height: 1.8;
    margin-top: 20px;
    padding: 15px;
    background: rgba(115, 95, 50, 0.15);
    border-left: 4px solid #C69749;
    border-radius: 5px;
}

/* Text Colors */
h1, h2, h3, h4, h5, h6 {
    color: #C69749 !important;
}

p, label, [class*="css"] {
    color: #e8e8e8 !important;
}

/* Sidebar Text */
[data-testid="stSidebar"] label {
    color: #e8e8e8 !important;
}

[data-testid="stSidebar"] p {
    color: #e8e8e8 !important;
}

/* Success/Warning Messages */
.stSuccess {
    background: rgba(76, 175, 80, 0.1) !important;
    border: 1px solid #4CAF50 !important;
    border-radius: 8px !important;
}

.stWarning {
    background: rgba(255, 152, 0, 0.1) !important;
    border: 1px solid #FF9800 !important;
    border-radius: 8px !important;
}

/* Horizontal Line */
hr {
    border: 0;
    height: 2px;
    background: #735F32;
}

/* Column Container */
.stColumn {
    padding: 0 5px;
}

/* Caption and small text */
.stCaption {
    color: #b0b0b0 !important;
    font-size: 13px;
}

/* Section subtitle */
.section-subtitle {
    font-size: 18px;
    color: #C69749;
    margin-bottom: 20px;
    font-weight: 300;
}
</style>
""", unsafe_allow_html=True)


# USERS FOLDER

if not os.path.exists("users"):
    os.makedirs("users")


# LOAD DATA

movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

API_KEY = "c7ec19ffdd3279641fb606d19ceb9bb1"


# PREPROCESS GENRE COLUMN

if 'genre' not in movies.columns:
    st.error("The 'genre' column does not exist in your movies dataset.")
else:
    movies['genre'] = movies['genre'].apply(lambda x: [g.strip() for g in x.split(',')] if isinstance(x, str) else [])

all_genres = sorted(list(set(g for sublist in movies['genre'] for g in sublist)))


# INITIALIZE SESSION STATE

if "user" not in st.session_state:
    st.session_state.user = None
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "is_new_user" not in st.session_state:
    st.session_state.is_new_user = False
if "time_based_movies" not in st.session_state:
    st.session_state.time_based_movies = None
if "personalized_movies" not in st.session_state:
    st.session_state.personalized_movies = None
if "genre_based_movies" not in st.session_state:
    st.session_state.genre_based_movies = None
if "selected_genre" not in st.session_state:
    st.session_state.selected_genre = None
if "show_details_movie" not in st.session_state:
    st.session_state.show_details_movie = None
if "search_similar_movies" not in st.session_state:
    st.session_state.search_similar_movies = None
if "show_genre_selector" not in st.session_state:
    st.session_state.show_genre_selector = False


# HELPER FUNCTIONS

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_titles, recommended_posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_titles, recommended_posters

def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    return requests.get(url).json()

def get_movies_by_genres(genres, sample_size=5):
    """Returns filtered and sampled movies without displaying them"""
    filtered = movies[movies['genre'].apply(lambda g: any(genre in g for genre in genres))]
    if filtered.empty:
        return None
    return filtered.sample(min(sample_size, len(filtered)))

def display_movie_card(movie_id, movie_title, key_suffix=""):
    """Display a single movie card with proper container and view button"""
    st.markdown('<div class="movie-card-wrapper">', unsafe_allow_html=True)
    
    st.markdown('<div class="movie-image-container">', unsafe_allow_html=True)
    st.image(fetch_poster(movie_id), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="movie-title-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="movie-title">{movie_title}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show Details Button
    if st.button("Show Details", use_container_width=True, key=f"show_details_btn_{key_suffix}_{movie_id}"):
        st.session_state.show_details_movie = movie_title
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_movies_grid(movies_df, title="Movies", grid_key=""):
    """Display movies in a grid format with proper containers"""
    if movies_df is None or movies_df.empty:
        st.markdown(f"### {title}")
        st.info("No movies available for this selection.")
        return
    
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    cols = st.columns(len(movies_df))
    for i, col in enumerate(cols):
        with col:
            m_id = movies_df.iloc[i].id
            m_title = movies_df.iloc[i].title
            display_movie_card(m_id, m_title, key_suffix=f"{grid_key}_{i}")


# SIDEBAR - USER PROFILE

# Determine header text
if st.session_state.user:
    profile_header = st.session_state.user
else:
    profile_header = "User Profile"

st.sidebar.markdown(f'<div class="sidebar-header">{profile_header}</div>', unsafe_allow_html=True)

# LOGIN SECTION - Show only when user is not logged in
if not st.session_state.user:
    username = st.sidebar.text_input("Enter your name:", placeholder="Your name here", key="login_username")
    
    if st.sidebar.button("Login", use_container_width=True, key="login_btn"):
        if username.strip():
            is_new = False
            try:
                with open(f"users/{username}.json", "r") as f:
                    st.session_state.user_data = json.load(f)
                    is_new = False
            except FileNotFoundError:
                st.session_state.user_data = {"username": username, "genres": [], "watched": []}
                with open(f"users/{username}.json", "w") as f:
                    json.dump(st.session_state.user_data, f)
                is_new = True
            
            st.session_state.user = username
            st.session_state.is_new_user = is_new
            st.session_state.show_genre_selector = False
            st.rerun()
        else:
            st.sidebar.warning("Please enter your name.")

# USER LOGGED IN SECTION
else:
    # Welcome message
    if st.session_state.is_new_user:
        st.sidebar.success(f"Welcome {st.session_state.user}")
    else:
        st.sidebar.success(f"Welcome again {st.session_state.user}")
    
    st.sidebar.markdown('<hr style="border: 0; height: 2px; background: #735F32; margin: 20px 0;">', unsafe_allow_html=True)
    
    current_genres = st.session_state.user_data.get("genres", [])
    
    # SELECTED GENRES DISPLAY SECTION
    if current_genres:
        st.sidebar.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-header" style="margin: 0 0 15px 0; border: none; font-size: 16px;">Your Genres</div>', unsafe_allow_html=True)
        
        # Display selected genres as tags in a grid
        genres_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 15px;">'
        for genre in current_genres:
            genres_html += f'<div style="background: #735F32; color: white; padding: 8px 8px; border-radius: 8px; border: 1px solid white; font-size: 11px; font-weight: 600; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{genre}</div>'
        genres_html += '</div>'
        st.sidebar.markdown(genres_html, unsafe_allow_html=True)
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # GENRE PREFERENCES SECTION
    if not st.session_state.show_genre_selector:
        if st.sidebar.button("Add/Edit Genres", use_container_width=True, key="open_genres_btn"):
            st.session_state.show_genre_selector = True
            st.rerun()
    else:
        st.sidebar.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-header" style="margin: 0 0 15px 0; border: none; font-size: 16px;">Select Genres</div>', unsafe_allow_html=True)
        
        # Dropdown to add genres
        user_genres = st.sidebar.multiselect(
            "Choose your favorite genres:",
            all_genres,
            default=st.session_state.user_data.get("genres", []),
            label_visibility="collapsed"
        )
        
        # Display selected genres count and removal block
        if user_genres:
            st.sidebar.markdown(f'<div style="background: rgba(198, 151, 73, 0.1); border: 2px solid #735F32; border-radius: 8px; padding: 12px; margin-bottom: 15px;">', unsafe_allow_html=True)
            st.sidebar.markdown(f'<div style="color: #C69749; font-size: 13px; font-weight: 700; margin-bottom: 10px;">{len(user_genres)} Genres Selected</div>', unsafe_allow_html=True)
            
            # Display selected genres as removable tags in grid
            genres_preview_html = '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px;">'
            for genre in user_genres:
                genres_preview_html += f'<div style="background: #735F32; color: #C69749; padding: 6px 8px; border-radius: 5px; font-size: 11px; font-weight: 600; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{genre}</div>'
            genres_preview_html += '</div>'
            st.sidebar.markdown(genres_preview_html, unsafe_allow_html=True)
            st.sidebar.markdown('</div>', unsafe_allow_html=True)
        else:
            st.sidebar.markdown(f'<div style="background: rgba(198, 151, 73, 0.1); border: 2px solid #735F32; border-radius: 8px; padding: 12px; margin-bottom: 15px; text-align: center;">', unsafe_allow_html=True)
            st.sidebar.markdown(f'<div style="color: #b0b0b0; font-size: 12px;">No genres selected</div>', unsafe_allow_html=True)
            st.sidebar.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("Save", use_container_width=True, key="save_genres_btn"):
                st.session_state.user_data["genres"] = user_genres
                with open(f"users/{st.session_state.user}.json", "w") as f:
                    json.dump(st.session_state.user_data, f)
                st.session_state.show_genre_selector = False
                st.sidebar.success("Preferences saved!")
                st.rerun()
        
        with col2:
            if st.button("Cancel", use_container_width=True, key="cancel_genres_btn"):
                st.session_state.show_genre_selector = False
                st.rerun()
        
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('<hr style="border: 0; height: 2px; background: #735F32; margin: 20px 0;">', unsafe_allow_html=True)
    
    # LOGOUT BUTTON
    if st.sidebar.button("Logout", use_container_width=True, key="logout_btn"):
        st.session_state.user = None
        st.session_state.user_data = None
        st.session_state.is_new_user = False
        st.session_state.show_genre_selector = False
        st.rerun()

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown("#### About NextWatch")
st.sidebar.info("Get personalized movie recommendations based on your preferences, time of day, and selected genres!")


# HEADER

st.markdown('<div class="title">NextWatch</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Your Personalized Movie Recommendation Engine</div>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)


# MOVIE DETAILS DISPLAY (SHOW AT TOP WHEN CLICKED)

if st.session_state.show_details_movie:
    st.markdown('<div class="details-container">', unsafe_allow_html=True)
    
    movie_row = movies[movies['title'] == st.session_state.show_details_movie].iloc[0]
    movie_id = movie_row.id
    details = get_movie_details(movie_id)

    st.markdown(f'<div class="details-title">{details.get("title", "Unknown")}</div>', unsafe_allow_html=True)
    
    # Side by side: poster + details
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(fetch_poster(movie_id), use_container_width=True)
    with col2:
        st.markdown(f'<div class="details-info"><span class="details-info-label">Rating:</span> {details.get("vote_average", "N/A")} / 10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-info"><span class="details-info-label">Release Date:</span> {details.get("release_date", "N/A")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-info"><span class="details-info-label">Runtime:</span> {details.get("runtime", "N/A")} minutes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-overview"><span class="details-info-label">Overview</span><br><br>{details.get("overview", "No overview available.")}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Similar movies for details page
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Similar Movies You May Like</div>', unsafe_allow_html=True)
    rec_names, rec_posters = recommend(st.session_state.show_details_movie)
    cols = st.columns(len(rec_names))
    for i, col in enumerate(cols):
        with col:
            display_movie_card(movies[movies['title'] == rec_names[i]].iloc[0].id, rec_names[i], key_suffix=f"similar_{i}")
    
    # Close details button
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Close Details", use_container_width=True, key="close_details_btn"):
            st.session_state.show_details_movie = None
            st.rerun()
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)


# TIME-OF-DAY RECOMMENDATIONS

hour = datetime.now().hour
if 6 <= hour < 12:
    time_genres = ['Comedy', 'Adventure']
elif 12 <= hour < 18:
    time_genres = ['Action', 'Sci-Fi']
elif 18 <= hour < 22:
    time_genres = ['Romance', 'Drama']
else:
    time_genres = ['Thriller', 'Horror']

if st.session_state.time_based_movies is None:
    st.session_state.time_based_movies = get_movies_by_genres(time_genres)

display_movies_grid(st.session_state.time_based_movies, f"Time-Based Recommendations ({', '.join(time_genres)})", "time_based")


# USER PROFILE BASED RECOMMENDATIONS

if st.session_state.user and st.session_state.user_data.get("genres"):
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    if st.session_state.personalized_movies is None:
        st.session_state.personalized_movies = get_movies_by_genres(st.session_state.user_data["genres"])
    
    display_movies_grid(st.session_state.personalized_movies, f"Recommended for {st.session_state.user}", "personalized")


# GENRE-BASED RECOMMENDATIONS

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Explore by Genre</div>', unsafe_allow_html=True)

prev_genre = st.session_state.selected_genre
selected_genre = st.selectbox("Choose a genre:", all_genres, label_visibility="collapsed")

if selected_genre != prev_genre:
    st.session_state.selected_genre = selected_genre
    st.session_state.genre_based_movies = get_movies_by_genres([selected_genre])
else:
    if st.session_state.selected_genre is None:
        st.session_state.selected_genre = selected_genre
        st.session_state.genre_based_movies = get_movies_by_genres([selected_genre])

display_movies_grid(st.session_state.genre_based_movies, f"Top {selected_genre} Movies", "genre_based")


# MOVIE SEARCH + DETAILS

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="section-header">Search for a Movie</div>', unsafe_allow_html=True)

selected_movie = st.selectbox("Select or search a movie:", movies['title'].values, label_visibility="collapsed")

# Show Details button BEFORE recommendations
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Show Details", use_container_width=True, key="show_details_btn"):
        st.session_state.show_details_movie = selected_movie


# MOVIE DETAILS DISPLAY (BEFORE SIMILAR MOVIES)

if st.session_state.show_details_movie:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="details-container">', unsafe_allow_html=True)
    
    movie_row = movies[movies['title'] == st.session_state.show_details_movie].iloc[0]
    movie_id = movie_row.id
    details = get_movie_details(movie_id)

    st.markdown(f'<div class="details-title">{details.get("title", "Unknown")}</div>', unsafe_allow_html=True)
    
    # Side by side: poster + details
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(fetch_poster(movie_id), use_container_width=True)
    with col2:
        st.markdown(f'<div class="details-info"><span class="details-info-label">Rating:</span> {details.get("vote_average", "N/A")} / 10</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-info"><span class="details-info-label">Release Date:</span> {details.get("release_date", "N/A")}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-info"><span class="details-info-label">Runtime:</span> {details.get("runtime", "N/A")} minutes</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="details-overview"><span class="details-info-label">Overview</span><br><br>{details.get("overview", "No overview available.")}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Similar movies for details page
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    rec_names, rec_posters = recommend(st.session_state.show_details_movie)
    
    st.markdown('<div class="section-header">Similar Movies You May Like</div>', unsafe_allow_html=True)
    cols = st.columns(len(rec_names))
    for i, col in enumerate(cols):
        with col:
            display_movie_card(movies[movies['title'] == rec_names[i]].iloc[0].id, rec_names[i])
    
    # Close details button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Close Details", use_container_width=True, key="close_details_btn"):
            st.session_state.show_details_movie = None
            st.rerun()

# Display search results only if NOT showing details
else:
    if selected_movie:
        st.markdown('<div class="section-subtitle">Similar Movies for Your Search</div>', unsafe_allow_html=True)
        if st.session_state.search_similar_movies is None or st.session_state.search_similar_movies[0] != selected_movie:
            rec_names, rec_posters = recommend(selected_movie)
            st.session_state.search_similar_movies = (selected_movie, rec_names, rec_posters)
        else:
            _, rec_names, rec_posters = st.session_state.search_similar_movies
        
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                display_movie_card(movies[movies['title'] == rec_names[i]].iloc[0].id, rec_names[i], key_suffix=f"search_{i}")


# FOOTER

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #999; margin-top: 40px; padding-bottom: 20px;">
    <p style="font-size: 14px; margin-bottom: 10px;"><strong>NextWatch</strong> — Professional Movie Recommendation Engine</p>
    <p style="font-size: 12px; color: #666;">Personalized • Time-based • Profile-based | Built for Movie Enthusiasts</p>
    <p style="font-size: 11px; color: #555; margin-top: 15px;">© 2025 NextWatch. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)


# To run this program: streamlit run app.py