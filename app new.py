import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from movie_data import MovieData  # Import the class

# Initialize movie data class
movie_data = MovieData()

st.title("Movie Data Analysis App")

# Movie Type Analysis
st.sidebar.header("Movie Type Analysis")
N = st.sidebar.number_input("Select N for top movie types", min_value=1, max_value=50, value=10, step=1)
movie_types_df = movie_data.movie_type(N)
st.subheader("Top Movie Types")
st.bar_chart(movie_types_df.set_index("Movie_Type"))

# Actor Count Analysis
st.subheader("Actor Count Distribution")
actor_count_df = movie_data.actor_count()
st.bar_chart(actor_count_df.set_index("Number_of_Actors"))

# Actor Distribution Analysis
st.sidebar.header("Actor Distribution Analysis")
gender = st.sidebar.selectbox("Select Gender", ["All"] + list(movie_data.actors_df[5].dropna().unique()))
min_height = st.sidebar.number_input("Minimum Height", min_value=100.0, max_value=250.0, value=150.0)
max_height = st.sidebar.number_input("Maximum Height", min_value=100.0, max_value=250.0, value=200.0)
plot_distribution = st.sidebar.checkbox("Show Distribution Plot")

actor_dist_df = movie_data.actor_distributions(gender, max_height, min_height, plot=plot_distribution)
st.subheader("Filtered Actor Distribution")
st.dataframe(actor_dist_df)
