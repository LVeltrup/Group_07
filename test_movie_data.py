import pytest
from movie_data import MovieData

def test_movie_type():
    """
    Test that movie_type() correctly raises a ValueError when given an invalid argument.

    Expected Input:
        - N (int): The number of top movie genres to return.

    Expected Behavior:
        - Raises ValueError if N is not an integer.
    """
    movie_data = MovieData()
    with pytest.raises(ValueError):
        movie_data.movie_type("invalid")  # Should raise ValueError if N is not an integer.

def test_actor_count():
    """
    Test that actor_count() returns a non-empty DataFrame with the expected structure.

    Expected Output:
        - A pandas DataFrame with columns ["Number_of_Actors", "Movie_Count"].
        - DataFrame should not be empty.

    Expected Behavior:
        - Returns a valid DataFrame.
        - Contains correct column names.
    """
    movie_data = MovieData()
    result = movie_data.actor_count()
    
    assert not result.empty, "Actor count DataFrame is empty"
    assert "Number_of_Actors" in result.columns, "Column 'Number_of_Actors' missing"
    assert "Movie_Count" in result.columns, "Column 'Movie_Count' missing"

def test_actor_distributions():
    """
    Test that actor_distributions() correctly filters actors and raises errors for invalid inputs.

    Expected Inputs:
        - gender (str): "M", "F", or "All".
        - max_height_cm (float): Maximum height threshold in centimeters.
        - min_height_cm (float): Minimum height threshold in centimeters.
        - plot (bool, optional): Whether to generate a matplotlib histogram (default: False).

    Expected Behavior:
        - Raises ValueError for invalid gender (non-string).
        - Raises ValueError for invalid height values (non-numeric).
        - Returns a DataFrame with the correct structure when valid inputs are used.
    """
    movie_data = MovieData()
    
    # Test invalid gender type
    with pytest.raises(ValueError):
        movie_data.actor_distributions(123, 180, 160)  # Gender should be a string
    
    # Test invalid height values
    with pytest.raises(ValueError):
        movie_data.actor_distributions("Male", "invalid", 160)  # Height should be numeric
    
    # Test valid input returns a non-empty DataFrame
    try:
        df = movie_data.actor_distributions("M", 200, 150)
        assert not df.empty, "actor_distributions() returned an empty DataFrame"
        assert "Actor_Name" in df.columns, "Column 'Actor_Name' missing"
        assert "Height_cm" in df.columns, "Column 'Height_cm' missing"
        assert "Gender" in df.columns, "Column 'Gender' missing"
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

