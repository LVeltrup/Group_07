import os
import pandas as pd
import requests
import tarfile
from pathlib import Path
from typing import ClassVar
from pydantic import BaseModel, ConfigDict


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

movie_data = MovieData()

# Check if data is loaded
print(movie_data.movies_df.head())  # First 5 rows of movie dataset
print(movie_data.actors_df.head())  # First 5 rows of actor dataset

