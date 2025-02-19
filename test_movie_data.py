import pytest
from movie_data import MovieData

def test_movie_type():
    movie_data = MovieData()
    with pytest.raises(ValueError):
        movie_data.movie_type("invalid")

def test_actor_distributions():
    movie_data = MovieData()
    with pytest.raises(ValueError):
        movie_data.actor_distributions(123, 180, 160)
    with pytest.raises(ValueError):
        movie_data.actor_distributions("Male", "invalid", 160)

