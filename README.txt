# Movie Data Analysis Project

## Overview
This project is a *Streamlit-based application* that processes movie and actor metadata from the *CMU MovieSummaries dataset*. The app automatically downloads, extracts, and analyzes the data. It includes:

### Features:
- *Movie Data Analysis:*
  - Provides an overview of movie genres.
  - Displays actor distribution based on gender and height.
  - Allows filtering and visualization of actor count per movie.
- *Chronological Analysis:*
  - Displays the number of movies released per year.
  - Users can optionally filter by genre.
  - Analyzes actor birth dates (grouped by year or month).
  
- *Genre Classification Simulation:*
  - Simulates an AI pipeline that "classifies" a random movie’s genres.
  - Displays:
    - A random movie title with its summary.
    - The list of genres from the database.
    - A simulated LLM output (e.g., uppercasing the genres).
    - A comparison between the simulated LLM output and the database genres.

## Project Structure

| Path                             | Description                             |
|----------------------------------|-----------------------------------------|
| /Group_07/                    | Root project directory                 |
| ├── BackendStructure/         | Backend processing scripts             |
| │   ├── movie_data.py         | MovieData class for data handling      |
| │   ├── test_movie_data.py    | Pytest unit tests                      |
| │   ├── __pycache__/          | Cached Python bytecode files           |
| ├── GenerellProjectFiles/     | General project-related files          |
| │   ├── LICENSE               | Project license                        |
| │   ├── Project_2425_Part_II.md | Project documentation                 |
| │   ├── README.md             | Project documentation                  |
| │   ├── requirements.txt      | Required dependencies                  |
| │   ├── Task.mb               | Task management file                   |
| ├── MovieSummaries/           | Dataset storage                        |
| │   ├── character.metadata.tsv| Character data                         |
| │   ├── movie.metadata.tsv    | Movie metadata                         |
| │   ├── MovieSummaries.tar.gz | Compressed dataset                     |
| │   ├── name.clusters.txt     | Name clustering data                    |
| │   ├── plot_summaries.txt    | Movie plot summaries                   |
| │   ├── tvropes.clusters.txt  | TV tropes clustering                    |
| ├── pages/                    | Streamlit additional pages             |
| │   ├── Chronological_Movie_Analysis.py | Chronological movie analysis |
| │   ├── Movie_Genre_Classification.py  | Genre classification analysis |
| ├── .gitignore                | Git ignore file                         |
| ├── Movie_Data_Analysis.py    | Main Streamlit app                      |

## Installation
This project requires *Python 3.8+* and the necessary dependencies.

### Install Required Libraries
Run the following command:
bash
pip install -r requirements.txt


### Running the App
To start the Streamlit application, run:
bash
streamlit run Movie_Data_Analysis.py

This will open the web app in your default browser.

### Running Tests
To validate functionality, execute:
bash
pytest -v

This will test various functions, including:
- *Movie Genre Analysis:* Ensures correct data structure.
- *Actor Count & Distribution Analysis:* Validates expected results.

## Features & Methods

### Movie Genre Analysis
python
movie_data.movie_type(N)

- *Input:* N (int): Number of top genres to display.
- *Output:* Pandas DataFrame with columns ['Movie_Type', 'Count']

### Actor Count Distribution
python
movie_data.actor_count()

- *Output:* Pandas DataFrame with columns ['Number_of_Actors', 'Movie_Count']

### Actor Filtering by Gender & Height
python
movie_data.actor_distributions(gender, max_height, min_height, plot)

*Inputs:*
- gender (str): "M", "F", or "All"
- max_height (float): Maximum height in cm
- min_height (float): Minimum height in cm
- plot (bool): If True, displays a height distribution plot in Streamlit.

*Output:* A Pandas DataFrame with columns ['Actor_Name', 'Height_cm', 'Gender']

## Using Ollama for Genre Classification
This project uses *Ollama* to classify movie genres using an LLM.

### Install Ollama
Ensure that you have *Ollama* installed. Check the version:
bash
ollama --version

If not installed, download it from [Ollama’s website](https://ollama.com/download).

### Running the Ollama Service
Before running the Streamlit app, ensure Ollama is running:
bash
ollama serve


### Genre Classification Function
The app extracts genres from the database and classifies them using an LLM:
python
import ast
import ollama

def get_llm_genre_classification(summary):
    model = "mistral"
    prompt = (
        "Classify the following movie summary into genres. "
        "Only return a comma-separated list of genres based on common movie genres "
        "(e.g., Drama, Comedy, Action, Thriller, Sci-Fi, Romance, Horror, Mystery, Documentary). "
        "Do NOT include extra commentary or explanations.\n\n"
        f"Summary: {summary}"
    )
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content'] if response else "Unknown"

The LLM classification is then compared with database genres to check for matches.

## Troubleshooting

### Dataset Not Found
If files are missing, run:
bash
python BackendStructure/movie_data.py

This will re-download and extract the dataset if necessary.

### Streamlit App Not Displaying Charts
Ensure you are using:
python
st.pyplot(fig)

instead of:
python
plt.show()


## Contributors
- *Leon Veltrup* - 67561@novasbe.pt
- *Jan Felix Specht* - 64725@novasbe.pt
- *Florian Nolte* - 64386@novasbe.pt
- *Martin Mayer-Figge* - 68131@novasbe.pt

## License
This project is open-source and available under the *MIT License*.