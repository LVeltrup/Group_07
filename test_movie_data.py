import pytest
import pandas as pd
from movie_data import MovieData

@pytest.fixture
def movie_data():
    """
    Fixture to initialize the MovieData class for use in tests.
    
    Returns:
        MovieData: An instance of the MovieData class.
    """
    return MovieData()

def test_movie_type_invalid_input(movie_data):
    """
    Test that movie_type() correctly raises a ValueError when given an invalid argument.

    Expected Input:
        - N (int): The number of top movie genres to return.

    Expected Behavior:
        - Raises ValueError if N is not an integer.
    """
    with pytest.raises(ValueError):
        movie_data.movie_type("invalid")  # N should be an integer

def test_movie_type_output_structure(movie_data):
    """
    Test that movie_type() returns a DataFrame with the expected structure.

    Expected Output:
        - A pandas DataFrame with columns ["Movie_Type", "Count"].

    Expected Behavior:
        - DataFrame should contain valid columns.
    """
    result = movie_data.movie_type(10)
    assert isinstance(result, pd.DataFrame), "Expected a pandas DataFrame"
    assert "Movie_Type" in result.columns, "Column 'Movie_Type' is missing"
    assert "Count" in result.columns, "Column 'Count' is missing"

def test_actor_count_structure(movie_data):
    """
    Test that actor_count() returns a properly formatted DataFrame.

    Expected Output:
        - A pandas DataFrame with columns ["Number_of_Actors", "Movie_Count"].
        - The DataFrame should not be empty.
        - The columns should be of integer type.

    Expected Behavior:
        - DataFrame should contain the expected structure and types.
    """
    result = movie_data.actor_count()
    
    assert not result.empty, "Actor count DataFrame is empty"
    assert "Number_of_Actors" in result.columns, "Column 'Number_of_Actors' is missing"
    assert "Movie_Count" in result.columns, "Column 'Movie_Count' is missing"
    assert pd.api.types.is_integer_dtype(result["Number_of_Actors"]), "Column 'Number_of_Actors' should be integers"
    assert pd.api.types.is_integer_dtype(result["Movie_Count"]), "Column 'Movie_Count' should be integers"
def test_actor_distributions_invalid_inputs(movie_data):
    """
    Test that actor_distributions() correctly raises errors for invalid inputs.

    Expected Inputs:
        - gender (str): "M", "F", or "All".
        - max_height_cm (float): Maximum height threshold in centimeters.
        - min_height_cm (float): Minimum height threshold in centimeters.
        - plot (bool, optional): Whether to generate a matplotlib histogram (default: False).

    Expected Behavior:
        - Raises ValueError for invalid gender (non-string).
        - Raises ValueError for invalid height values (non-numeric).
        - Raises ValueError if min_height > max_height.
    """
    with pytest.raises(ValueError):
        movie_data.actor_distributions(123, 180, 160)  # Gender should be a string
    
    with pytest.raises(ValueError):
        movie_data.actor_distributions("Male", "invalid", 160)  # Height should be numeric
    
    with pytest.raises(ValueError):
        movie_data.actor_distributions("M", 150, 180)  # min_height > max_height

def test_actor_distributions_valid_output(movie_data):
    """
    Test that actor_distributions() returns a correctly structured DataFrame.

    Expected Output:
        - A pandas DataFrame with columns ["Actor_Name", "Height_cm", "Gender"].
        - The DataFrame should not be empty.

    Expected Behavior:
        - DataFrame should contain the expected columns.
    """
    df = movie_data.actor_distributions("M", 200, 150)
    assert isinstance(df, pd.DataFrame), "Expected a pandas DataFrame"
    assert "Actor_Name" in df.columns, "Column 'Actor_Name' is missing"
    assert "Height_cm" in df.columns, "Column 'Height_cm' is missing"
    assert "Gender" in df.columns, "Column 'Gender' is missing"

def test_actor_distributions_no_results(movie_data):
    """
    Test that actor_distributions() returns an empty DataFrame when no actors match the criteria.

    Expected Input:
        - A height range where no actors exist (e.g., min_height = max_height = 50 cm).

    Expected Behavior:
        - Returns an empty pandas DataFrame.
    """
    df = movie_data.actor_distributions("M", 50, 50)  # No actors should be 50cm tall
    assert df.empty, "Expected an empty DataFrame but got results"
