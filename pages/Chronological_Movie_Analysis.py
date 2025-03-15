import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from BackendStructure.movie_data import MovieData

# Initialize movie data
movie_data = MovieData()

st.title("📆 Chronological Movie Analysis")

# Sidebar for genre selection for releases
st.sidebar.header("🔍 Filter by Genre")
# Get top 10 genres from the dataset
top_genres = movie_data.movie_type(10)["Movie_Type"].tolist()
selected_genre = st.sidebar.selectbox("Select Genre (or All)", ["All"] + top_genres)

# Compute movie releases per year
if selected_genre == "All":
    releases_df = movie_data.releases()
else:
    releases_df = movie_data.releases(selected_genre)

st.subheader("🎬 Movies Released Per Year")
st.bar_chart(releases_df.set_index("Year"))

# Sidebar for actor birth analysis
st.sidebar.header("🧑‍🎭 Actor Birth Analysis")
age_option = st.sidebar.selectbox("Select Period", ["Year", "Month"])
if age_option == "Year":
    ages_df = movie_data.ages("Y")
else:
    ages_df = movie_data.ages("M")

st.subheader("👶 Actor Births Count")
# Use the first column name as the grouping label (BirthYear or BirthMonth)
group_col = ages_df.columns[0]
st.bar_chart(ages_df.set_index(group_col))
