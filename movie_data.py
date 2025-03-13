import os
import pandas as pd
import requests
import tarfile
from pathlib import Path
from typing import ClassVar
from pydantic import BaseModel, PositiveInt, ConfigDict
import ast
import streamlit as st

class MovieData(BaseModel):
    """Class for downloading, extracting, and processing the CMU MovieSummaries dataset."""

    # Dataset URL
    DATA_URL: ClassVar[str] = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"

    EXTRACT_DIR: ClassVar[Path] = Path(__file__).resolve().parent / "MovieSummaries"
    ARCHIVE_PATH: ClassVar[Path] = EXTRACT_DIR / "MovieSummaries.tar.gz"

    model_config = ConfigDict(arbitrary_types_allowed=True)

    movie_metadata_path: Path = EXTRACT_DIR / "movie.metadata.tsv"
    character_metadata_path: Path = EXTRACT_DIR / "character.metadata.tsv"
    summary_path: Path = EXTRACT_DIR / "plot_summaries.txt"

    def __init__(self, **data):
        """Initializes the MovieData class, ensuring the dataset is available and loaded."""
        super().__init__(**data)
        
        object.__setattr__(self, "movies_df", None)
        object.__setattr__(self, "actors_df", None)
        
        self._ensure_data()
        self._load_data()
    
    def _ensure_data(self):
        """Checks if the dataset exists; downloads and extracts it if missing."""
        self.EXTRACT_DIR.mkdir(exist_ok=True)

        if not self.movie_metadata_path.exists() or not self.character_metadata_path.exists() or not self.summary_path.exists():
            if not self.ARCHIVE_PATH.exists():
                print("Downloading dataset directly into MovieSummaries/...")
                self._download_data()
            
            print("Extracting dataset...")
            self._extract_data()

    def _download_data(self):
        """Downloads the MovieSummaries dataset directly into the MovieSummaries directory."""
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

            extracted_subfolder = self.EXTRACT_DIR / "MovieSummaries"
            if extracted_subfolder.exists():
                for file in extracted_subfolder.iterdir():
                    file.rename(self.EXTRACT_DIR / file.name)
                extracted_subfolder.rmdir()

        else:
            raise FileNotFoundError(f"Archive file {self.ARCHIVE_PATH} not found. Ensure the download was successful.")

    def _load_data(self):
        """Loads movie and character metadata into Pandas DataFrames."""
        print(f"Checking: {self.movie_metadata_path}")
        print(f"Checking: {self.character_metadata_path}")
        print(f"Checking: {self.summary_path}")

        if not self.movie_metadata_path.exists() or not self.character_metadata_path.exists() or not self.summary_path.exists():
            raise FileNotFoundError("Some dataset files are missing. Ensure they are extracted correctly.")

        print("Files found. Loading into DataFrames...")

        # Load movies metadata
        movies_df = pd.read_csv(self.movie_metadata_path, sep="\t", header=None)

        # Load summaries (Assuming format: "movie_id<TAB>summary")
        summaries_df = pd.read_csv(self.summary_path, sep="\t", header=None, names=["movie_id", "summary"], dtype={"movie_id": str})

        # Convert movie ID to string (to avoid mismatches)
        movies_df[0] = movies_df[0].astype(str)
        summaries_df["movie_id"] = summaries_df["movie_id"].astype(str)

        # Merge summaries into movies_df
        movies_df = movies_df.merge(summaries_df, left_on=0, right_on="movie_id", how="left")
        print("✅ Movie summaries successfully loaded and merged!")

        # Load character metadata
        actors_df = pd.read_csv(self.character_metadata_path, sep="\t", header=None)

        # Assign DataFrames to class attributes
        object.__setattr__(self, "movies_df", movies_df.dropna())
        object.__setattr__(self, "actors_df", actors_df.dropna())

        print("Data successfully loaded.")

    def movie_type(self, N: PositiveInt = 10) -> pd.DataFrame:
        """Returns the top N most common movie genres."""
        if not isinstance(N, int):
            raise ValueError("N must be an integer.")

        if 8 not in self.movies_df.columns:
            raise KeyError("Column index 8 (Genres) not found in dataset.")

        def safe_parse_dict(x):
            try:
                if isinstance(x, str):
                    parsed = ast.literal_eval(x)
                    return parsed if isinstance(parsed, dict) else {}
                return {}
            except (ValueError, SyntaxError):
                return {}

        self.movies_df[8] = self.movies_df[8].apply(safe_parse_dict)

        all_genres = [genre for genre_dict in self.movies_df[8] for genre in genre_dict.values()]
        genre_counts = pd.Series(all_genres).value_counts().head(N).reset_index()
        genre_counts.columns = ["Movie_Type", "Count"]

        return genre_counts
    
    def actor_count(self) -> pd.DataFrame:
        """Returns a histogram of movie counts based on the number of actors."""
        if 0 not in self.actors_df.columns:
            raise KeyError("Column index 0 (Movie ID) not found in dataset.")

        actor_counts = self.actors_df.groupby(0).size().value_counts().reset_index()
        actor_counts.columns = ["Number_of_Actors", "Movie_Count"]

        return actor_counts
    
    def releases(self, genre: str = None) -> pd.DataFrame:
        """Returns a DataFrame counting the number of movies released per year."""
        df = self.movies_df.copy()
        try:
            df["Year"] = pd.to_datetime(df[3], errors="coerce").dt.year
        except Exception:
            df["Year"] = df[3].astype(str).str[:4].astype(float)

        if genre is not None:
            df = df[df[8].apply(lambda g: genre in list(g.values()) if isinstance(g, dict) else False)]

        releases_df = df.groupby("Year").size().reset_index(name="Count").dropna()
        releases_df["Year"] = releases_df["Year"].astype(int)

        return releases_df

    def ages(self, period: str = "Y") -> pd.DataFrame:
        """Returns a DataFrame counting how many actors were born per year (or per month)."""
        period = period.upper()
        if period not in ["Y", "M"]:
            period = "Y"

        df = self.actors_df.copy()
        df["BirthDate"] = pd.to_datetime(df[4], errors="coerce")

        if period == "Y":
            df["BirthYear"] = df["BirthDate"].dt.year
            result = df.groupby("BirthYear").size().reset_index(name="Count").dropna()
            result["BirthYear"] = result["BirthYear"].astype(int)
            return result
        else:
            df["BirthMonth"] = df["BirthDate"].dt.month
            result = df.groupby("BirthMonth").size().reset_index(name="Count").dropna()
            result["BirthMonth"] = result["BirthMonth"].astype(int)
            return result
