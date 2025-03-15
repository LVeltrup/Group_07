# page_title: Movie Genre Classification

import streamlit as st
import pandas as pd
import random
import ollama
import ast
from Group_07.BackendStructure.movie_data import MovieData

movie_data = MovieData()

st.title("🤖 Movie Genre Classification")

if st.button("Shuffle"):
    # Select a random movie row
    random_row = movie_data.movies_df.sample(n=1).iloc[0]
    movie_title = random_row[2]  # Movie name is at column 2
    # Extract the actual movie summary (Check the correct column index)
    summary = random_row["summary"] if isinstance(random_row["summary"], str) and len(random_row["summary"]) > 10 else "No summary available."

    # Extract genres from column 8 (which is stored as a dictionary in string format)
    genres_str = random_row[8]
    try:
        genres_dict = ast.literal_eval(genres_str) if isinstance(genres_str, str) else {}
        genres_list = list(genres_dict.values()) if isinstance(genres_dict, dict) else []
    except (ValueError, SyntaxError):
        genres_list = []  # Fallback if parsing fails
    db_genres = ", ".join(genres_list)
    
    # Function to get genre classification from LLM
    def get_llm_genre_classification(summary):
        model = "mistral"  # Choose an Ollama model (or use another small model)
        prompt = (
            "Classify the following movie summary into genres. "
            "Only return a comma-separated list of genres that best fit the summary, based on common movie genres "
            "(e.g., Drama, Comedy, Action, Thriller, Sci-Fi, Romance, Horror, Mystery, Documentary). "
            "Do NOT include any extra commentary or explanations.\n\n"
            f"Summary: {summary}"
        )
        response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
        return response['message']['content'] if response else "Unknown"

    # Get LLM genre classification
    llm_classification = get_llm_genre_classification(summary)

    # Improve genre matching logic: Allow partial matches
    db_genres_set = set(g.lower() for g in genres_list)
    llm_genres_set = set(g.lower().strip() for g in llm_classification.split(","))

    classification_check = "Yes" if db_genres_set & llm_genres_set else "No"

    # Adjust dynamic height for summary box
    summary_box_height = min(400, max(150, len(summary) // 3))

    # Display UI components with improved visuals
    st.text_area("📖 **Movie Title and Summary**", f"{movie_title}\n\n{summary}", height=summary_box_height)
    st.text_area("🎬 **Database Genres**", db_genres, height=80)
    st.text_area("🤖 **LLM Genre Classification**", llm_classification, height=80)

    # Add a horizontal separator for clarity
    st.markdown("---")

    # Display UI feedback based on classification check
    if classification_check == "Yes":
        st.success("✅ **The LLM correctly classified at least one matching genre!**")
    else:
        st.warning("❌ **The LLM's classification does not match the database genres.**")
