Project Overview

This project is a Streamlit-based application that processes movie and actor metadata from the CMU MovieSummaries dataset. The app automatically downloads, extracts, and analyzes the data. In addition to the original analyses (movie genre frequency, actor counts, and actor distribution), this updated version includes:

    Chronological Analysis:
    A new page that shows the number of movies released per year. Users can optionally filter by genre. It also includes an analysis of actor birth dates (grouped either by year or by month).

    Genre Classification Simulation:
    A third page simulates an AI pipeline that "classifies" a random movie’s genres. This page displays:
        A random movie title with its summary.
        The list of genres from the database.
        A simulated LLM output (for example, by uppercasing the genres).
        A comparison result showing whether the simulated LLM output matches the database genres.

### Project Structure

| Path                   | Description                        |
|------------------------|--------------------------------|
| `/Group_07/`          | Root project directory         |
| ├── `MovieSummaries/` | Directory for dataset storage  |
| ├── `movie_data.py`   | MovieData class for data handling |
| ├── `app.py`          | Streamlit application          |
| ├── `test_movie_data.py` | Pytest unit tests          |
| ├── `README.md`       | Project documentation         |

### Installation  
To run the app, you need **Python 3.8+** and the required dependencies.

#### Install Required Libraries  
Run:  
`pip install -r requirements.txt`

### Running the App
Start the Streamlit application by running:
`streamlit run app.py`

This will open the web app in your default browser.

### Running Tests
To validate functionality, run the following in the main project directory:
`pytest -v`

This will test:
- test_movie_type_invalid_input(): Ensures movie_type() raises an error for invalid input.
- test_movie_type_output_structure(): Validates that movie_type() returns a correctly structured DataFrame.
- test_actor_count_structure(): Checks that actor_count() returns a DataFrame with expected structure and integer values.
- test_actor_distributions_invalid_inputs(): Ensures actor_distributions() raises errors for invalid gender or height values.
- test_actor_distributions_valid_output(): Verifies that actor_distributions() returns a correctly structured DataFrame.
- test_actor_distributions_no_results(): Checks that actor_distributions() returns an empty DataFrame when no actors match the filter.


### Features & Methods
- Movie Genre Analysis
`movie_data.movie_type(N)`

- Input:
`N (int)`: Number of top genres to display.

- Output -> A Pandas DataFrame with columns:
`["Movie_Type", "Count"]`

- Actor Count Distribution
`movie_data.actor_count()`

- Output -> A Pandas DataFrame with columns:
`["Number_of_Actors", "Movie_Count"]`

- Actor Filtering by Gender & Height
`movie_data.actor_distributions(gender, max_height, min_height, plot)`

Input:
- gender (str): "M", "F", or "All"
- max_height (float): Maximum height in cm
- min_height (float): Minimum height in cm
- plot (bool): If True, displays a height distribution plot in Streamlit.

Output:
A Pandas DataFrame with columns:
`["Actor_Name", "Height_cm", "Gender"]`

### Troubleshooting
Dataset Not Found

If files are missing, run:
`python movie_data.py`

This will re-download and extract the dataset if it is missing.

Streamlit App Not Displaying Charts  
Ensure you are using:  
st.pyplot(fig)  
instead of:  
plt.show()  

The project now includes three pages:
• The main page (app.py) for basic analysis,
• A second page (app2.py) for chronological movie and actor birth analyses, and
• A third page (app3.py) for AI-based genre classification (using a local LLM from ollama).
Installation instructions (using the new requirements.txt).
A short essay discussing how text classification in this project could help in analyzing and categorizing documents in support of the UN’s Sustainable Development Goals (SDGs).

### License
This project is open-source and available under the MIT License.

Contributors  
- Leon Veltrup - 67561@novasbe.pt
- Felix Specht - 64725@novasbe.pt
- Florian Nolte - 64386@novasbe.pt
- Martin Mayer-Figge - 68131@novasbe.pt  

