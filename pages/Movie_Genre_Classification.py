# page_title: Movie Genre Classification

import streamlit as st
import pandas as pd
import random
import ollama
import ast
from BackendStructure.movie_data import MovieData

# --- Initialize movie data ---
movie_data = MovieData()

st.title("🤖 Movie Genre Classification")

# --- Default placeholders shown before shuffle ---
movie_title_summary = "Press Shuffle to load a random movie and its summary."
db_genres = "Press Shuffle to show genres from database."
llm_classification = "Press Shuffle to get LLM genre classification."

# --- Set default value for classification check in session_state ---
if "classification_check" not in st.session_state:
    st.session_state["classification_check"] = None  # Will hold "Yes" or "No"

# --- Function to get genre classification from LLM (defined outside button) ---
def get_llm_genre_classification(summary):
    model = "mistral"  # Ollama model
    prompt = (
        "Classify the following movie summary into genres. "
        "Only return a comma-separated list of genres that best fit the summary, based on common movie genres "
        "(e.g., Drama, Comedy, Action, Thriller, Sci-Fi, Romance, Horror, Mystery, Documentary). "
        "Do NOT include any extra commentary or explanations.\n\n"
        f"Summary: {summary}"
    )
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'] if response else "Unknown"

# --- Shuffle logic: updates variables when button is clicked ---
if st.button("Shuffle"):
    # Select a random movie row
    random_row = movie_data.movies_df.sample(n=1).iloc[0]
    movie_title = random_row[2]  # Movie title (assuming column 2)

    # Extract the movie summary (check if valid string)
    summary = random_row["summary"] if isinstance(random_row["summary"], str) and len(random_row["summary"]) > 10 else "No summary available."
    movie_title_summary = f"{movie_title}\n\n{summary}"

    # Extract genres from column 8 (which is stored as a dictionary in string format)
    genres_str = random_row[8]
    try:
        genres_dict = ast.literal_eval(genres_str) if isinstance(genres_str, str) else {}
        genres_list = list(genres_dict.values()) if isinstance(genres_dict, dict) else []
    except (ValueError, SyntaxError):
        genres_list = []  # Safe fallback
    db_genres = ", ".join(genres_list) if genres_list else "No genres available."

    # --- Get LLM genre classification ---
    llm_classification = get_llm_genre_classification(summary)

    # --- Optional: Genre matching check ---
    db_genres_set = set(g.lower() for g in genres_list)
    llm_genres_set = set(g.lower().strip() for g in llm_classification.split(","))
    classification_check = "Yes" if db_genres_set & llm_genres_set else "No"

    # --- Save everything in session_state ---
    st.session_state["movie_title_summary"] = movie_title_summary
    st.session_state["db_genres"] = db_genres
    st.session_state["llm_classification"] = llm_classification
    st.session_state["classification_check"] = classification_check

# --- Always display text boxes with either placeholder or actual content ---
# Use session_state if values exist, otherwise use placeholders
movie_title_summary = st.session_state.get("movie_title_summary", movie_title_summary)
db_genres = st.session_state.get("db_genres", db_genres)
llm_classification = st.session_state.get("llm_classification", llm_classification)
classification_check = st.session_state.get("classification_check", None)

# Adjust height dynamically based on summary length
summary_box_height = min(400, max(150, len(movie_title_summary) // 3))

# Display UI components with improved visuals
st.text_area("📖 **Movie Title and Summary**", movie_title_summary, height=summary_box_height)
st.text_area("🎬 **Database Genres**", db_genres, height=80)
st.text_area("🤖 **LLM Genre Classification**", llm_classification, height=80)


# --- Now show validation message at the bottom (if any) ---
if classification_check == "Yes":
    st.success("✅ **The LLM correctly classified at least one matching genre!**")
elif classification_check == "No":
    st.warning("❌ **The LLM's classification does not match the database genres.**")
