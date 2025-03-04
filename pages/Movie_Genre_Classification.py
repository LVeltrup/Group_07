# page_title: Movie Genre Classification

import streamlit as st
import pandas as pd
import random
from movie_data import MovieData

movie_data = MovieData()

st.title("🤖 Movie Genre Classification")

if st.button("Shuffle"):
    # Select a random movie row
    random_row = movie_data.movies_df.sample(n=1).iloc[0]
    movie_title = random_row[2]  # Movie name is at column 2
    # Simulate a summary (if plot summaries are not available)
    summary = f"This is a summary for {movie_title}."
    
    # Extract genres from column 8 (which is stored as a dictionary)
    genres_dict = random_row[8]
    if isinstance(genres_dict, dict):
        genres_list = list(genres_dict.values())
    else:
        genres_list = []
    db_genres = ", ".join(genres_list)
    
    # Simulate a local LLM classification (for example, by simply upper-casing the genres)
    llm_classification = ", ".join([g.upper() for g in genres_list])
    
    # Check if the LLM output (ignoring case) matches the database genres
    classification_check = "Yes" if set(g.lower() for g in genres_list) == set(g.lower() for g in llm_classification.split(", ")) else "No"
    
    st.text_area("Movie Title and Summary", f"{movie_title}\n\n{summary}", height=100)
    st.text_area("Database Genres", db_genres, height=68)
    st.text_area("LLM Genre Classification", llm_classification, height=68)
    st.write("LLM classification matches database:", classification_check)
