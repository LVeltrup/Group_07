import os
import tarfile
import pandas as pd
import matplotlib.pyplot as plt
import requests
from pydantic import BaseModel, PositiveInt, ConfigDict

class MovieData(BaseModel):
    """
    A class for loading and analyzing movie dataset.

    Attributes:
        movie_metadata_path (str): Path to the movie metadata file.
        character_metadata_path (str): Path to the character metadata file.
        movies_df (pd.DataFrame): DataFrame holding movie metadata.
        actors_df (pd.DataFrame): DataFrame holding character metadata.
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    dataset_url: str = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
    dataset_path: str = "downloads/MovieSummaries.tar.gz"
    extract_dir: str = "downloads/MovieSummaries"

    def __init__(self, **data):
        super().__init__(**data)
        
        # Ensure dataset is downloaded and extracted
        self._download_and_extract_data()

        # Define file paths after extraction
        self.movie_metadata_path = os.path.join(self.extract_dir, "movie.metadata.tsv")
        self.character_metadata_path = os.path.join(self.extract_dir, "character.metadata.tsv")

        object.__setattr__(self, "movies_df", None)
        object.__setattr__(self, "actors_df", None)

        self._load_data()

    def _download_and_extract_data(self):
        """Downloads and extracts dataset if not present."""
        if not os.path.exists(self.extract_dir):
            os.makedirs("downloads", exist_ok=True)
            print("Downloading dataset...")
            response = requests.get(self.dataset_url, stream=True)
            with open(self.dataset_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("Download complete. Extracting files...")

            with tarfile.open(self.dataset_path, "r:gz") as tar:
                tar.extractall(path=self.extract_dir)

            print("Extraction complete.")

    def _load_data(self):
        """Loads the dataset into Pandas DataFrames."""
        print(f"Checking: {self.movie_metadata_path}")
        print(f"Checking: {self.character_metadata_path}")

        if not os.path.exists(self.movie_metadata_path) or not os.path.exists(self.character_metadata_path):
            raise FileNotFoundError("Dataset files not found. Please ensure they are properly extracted.")

        object.__setattr__(self, "movies_df", pd.read_csv(self.movie_metadata_path, sep="\t", header=None))
        object.__setattr__(self, "actors_df", pd.read_csv(self.character_metadata_path, sep="\t", header=None))

    def movie_type(self, N: PositiveInt = 10) -> pd.DataFrame:
        """
        Returns the top N most common movie types.

        Args:
            N (int): Number of top movie types to return.

        Returns:
            pd.DataFrame: A DataFrame with columns ["Movie_Type", "Count"].
        """
        if not isinstance(N, int):
            raise ValueError("N must be an integer.")
        
        df = self.movies_df[3].value_counts().head(N).reset_index()
        df.columns = ["Movie_Type", "Count"]

        return df
    
    def actor_count(self) -> pd.DataFrame:
        """
        Returns a histogram of movie counts based on the number of actors.

        Returns:
            pd.DataFrame: A DataFrame with columns ["Number_of_Actors", "Movie_Count"].
        """
        df = self.movies_df[8].apply(lambda x: len(str(x).split(','))).value_counts().reset_index()
        df.columns = ["Number_of_Actors", "Movie_Count"]
        return df
    
    def actor_distributions(self, gender: str, max_height: float, min_height: float, plot: bool = False) -> pd.DataFrame:
        """
        Filters actors based on gender and height range. Optionally plots a histogram.

        Args:
            gender (str): "All" or a specific gender value.
            max_height (float): Maximum height threshold.
            min_height (float): Minimum height threshold.
            plot (bool): Whether to plot the height distribution.

        Returns:
            pd.DataFrame: A filtered DataFrame with actor attributes.
        """
        if not isinstance(gender, str):
            raise ValueError("Gender must be a string.")
        try:
            max_height = float(max_height)
            min_height = float(min_height)
        except ValueError:
            raise ValueError("max_height and min_height must be numeric values.")
        
        if max_height <= 0 or min_height <= 0:
            raise ValueError("max_height and min_height must be positive numbers.")
        
        if gender != "All":
            filtered_df = self.actors_df[self.actors_df[5] == gender]
        else:
            filtered_df = self.actors_df
        
        filtered_df = filtered_df[(filtered_df[6] >= min_height) & (filtered_df[6] <= max_height)]
        
        if plot:
            plt.hist(filtered_df[6], bins=20, alpha=0.7)
            plt.xlabel("Height")
            plt.ylabel("Frequency")
            plt.title(f"Height Distribution for {gender} actors")
            plt.show()
        
        return filtered_df[[7, 6, 5]]
