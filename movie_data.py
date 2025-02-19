import os
from matplotlib import pyplot as plt
import pandas as pd
import requests
import tarfile
from pathlib import Path
from typing import ClassVar
from pydantic import BaseModel, ConfigDict, PositiveInt
import ast


class MovieData(BaseModel):
    """Class for downloading, extracting, and processing the CMU MovieSummaries dataset."""

    # URL for dataset download
    DATA_URL: ClassVar[str] = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"

    # Define MovieSummaries as the main storage directory
    EXTRACT_DIR: ClassVar[Path] = Path(__file__).resolve().parent / "MovieSummaries"
    ARCHIVE_PATH: ClassVar[Path] = EXTRACT_DIR / "MovieSummaries.tar.gz"  # Store the archive inside MovieSummaries

    # Pydantic configuration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # File paths within MovieSummaries/
    movie_metadata_path: Path = EXTRACT_DIR / "movie.metadata.tsv"
    character_metadata_path: Path = EXTRACT_DIR / "character.metadata.tsv"

    def __init__(self, **data):
        super().__init__(**data)
        
        object.__setattr__(self, "movies_df", None)
        object.__setattr__(self, "actors_df", None)
        
        self._ensure_data()
        self._load_data()
    
    def _ensure_data(self):
        """Checks if the dataset exists; downloads and extracts it if missing."""
        self.EXTRACT_DIR.mkdir(exist_ok=True)  # Ensure MovieSummaries folder exists
        
        if not self.movie_metadata_path.exists() or not self.character_metadata_path.exists():
            if not self.ARCHIVE_PATH.exists():
                print("Downloading dataset directly into MovieSummaries/...")
                self._download_data()
            
            print("Extracting dataset...")
            self._extract_data()

    def _download_data(self):
        """Downloads the MovieSummaries dataset directly into MovieSummaries/."""
        response = requests.get(self.DATA_URL, stream=True)
        if response.status_code == 200:
            with open(self.ARCHIVE_PATH, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise RuntimeError(f"Download error: Status {response.status_code}")

    def _extract_data(self):
        """Extracts the downloaded TAR file inside the MovieSummaries directory."""
        if self.ARCHIVE_PATH.exists():
            with tarfile.open(self.ARCHIVE_PATH, "r:gz") as tar:
                tar.extractall(self.EXTRACT_DIR)

            # Move extracted files if they are inside a subfolder
            extracted_subfolder = self.EXTRACT_DIR / "MovieSummaries"
            if extracted_subfolder.exists():
                for file in extracted_subfolder.iterdir():
                    file.rename(self.EXTRACT_DIR / file.name)  # Move files up one level
                extracted_subfolder.rmdir()  # Remove empty folder

        else:
            raise FileNotFoundError(f"Archive file {self.ARCHIVE_PATH} not found. Ensure the download was successful.")


    def _load_data(self):
        """Checks file existence and loads them as Pandas DataFrames."""
        print(f"Checking: {self.movie_metadata_path}")
        print(f"Checking: {self.character_metadata_path}")

        if not self.movie_metadata_path.exists() or not self.character_metadata_path.exists():
            raise FileNotFoundError(
                f"Missing dataset files:\n"
                f"Expected: {self.movie_metadata_path}\n"
                f"Expected: {self.character_metadata_path}\n"
                f"Please ensure the dataset is properly extracted."
            )

        print("Files found. Loading into DataFrames...")

        object.__setattr__(self, "movies_df", pd.read_csv(self.movie_metadata_path, sep="\t", header=None))
        object.__setattr__(self, "actors_df", pd.read_csv(self.character_metadata_path, sep="\t", header=None))

        print("Data successfully loaded.")


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
            
    def movie_type(self, N: PositiveInt = 10) -> pd.DataFrame:
            """
            Returns the top N most common movie genres.
    
            Args:
            N (int): Number of top movie genres to return.
    
            Returns:
            pd.DataFrame: A DataFrame with columns ["Movie_Type", "Count"].
            """
            if not isinstance(N, int):
                raise ValueError("N must be an integer.")
    
            print("Checking movies_df columns:", self.movies_df.head())  # Debugging output
    
            # Ensure column 8 exists
            if 8 not in self.movies_df.columns:
                raise KeyError("Column index 8 (Genres) not found in dataset.")
    
            # Function to safely parse genre dictionary
            def safe_parse_dict(x):
                try:
                    if isinstance(x, str):
                        parsed = ast.literal_eval(x)
                        return parsed if isinstance(parsed, dict) else {}
                    return {}
                except (ValueError, SyntaxError):
                    return {}
    
            # Apply safe parsing to column 8
            self.movies_df[8] = self.movies_df[8].apply(safe_parse_dict)
    
            # Flatten and count occurrences of all genres
            all_genres = [genre for genre_dict in self.movies_df[8] for genre in genre_dict.values()]
            genre_counts = pd.Series(all_genres).value_counts().head(N).reset_index()
            genre_counts.columns = ["Movie_Type", "Count"]
    
            print("movie_type() Data Sample:")
            print(genre_counts.head())  # Debugging output
    
            return genre_counts
   
    def actor_count(self) -> pd.DataFrame:
        """
        Returns a histogram of movie counts based on the number of actors.
 
        Returns:
            pd.DataFrame: A DataFrame with columns ["Number_of_Actors", "Movie_Count"].
        """
        # Ensure the correct column exists
        if 8 not in self.actors_df.columns:
            raise KeyError("Column index 8 (Actors) not found in dataset.")
 
        # Count number of actors per movie (splitting by comma if multiple actors are listed)
        df = self.actors_df.groupby(0)[8].apply(lambda x: len(set(x))).value_counts().reset_index()
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
   
        return filtered_df[[7, 6, 5]]  # Return Actor Name, Height, Gender

# movie_data = MovieData()

# # Check if data is loaded
# print(movie_data.movies_df.head())  # First 5 rows of movie dataset
# print(movie_data.actors_df.head())  # First 5 rows of actor dataset

