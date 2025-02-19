import os
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel, PositiveInt, ConfigDict
from pathlib import Path
import requests
import tarfile
from typing import ClassVar


class MovieData(BaseModel):
    """ Klasse zum Laden und Verarbeiten der MovieSummaries-Daten. """

    # Auto-Download Einstellungen als `ClassVar`
    DATA_URL: ClassVar[str] = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
    DOWNLOAD_DIR: ClassVar[Path] = Path(__file__).resolve().parent / "downloads"
    ARCHIVE_PATH: ClassVar[Path] = DOWNLOAD_DIR / "MovieSummaries.tar.gz"
    EXTRACT_DIR: ClassVar[Path] = DOWNLOAD_DIR / "MovieSummaries"

    # Pydantic Konfiguration
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Dynamische Datei-Pfade
    base_path: Path = Path(__file__).resolve().parent / "MovieSummaries"
    movie_metadata_path: Path = base_path / "movie.metadata.tsv"
    character_metadata_path: Path = base_path / "character.metadata.tsv"

    def __init__(self, **data):
        super().__init__(**data)
        
        object.__setattr__(self, "movies_df", None)
        object.__setattr__(self, "actors_df", None)
        
        self._ensure_data()
        self._load_data()
    
    def _ensure_data(self):
        """ Überprüft, ob die Daten vorhanden sind, lädt und entpackt sie falls nötig. """
        self.DOWNLOAD_DIR.mkdir(exist_ok=True)  # downloads/ Ordner erstellen, falls nicht vorhanden
        
        if not self.EXTRACT_DIR.exists():  # Falls Daten nicht existieren → herunterladen und entpacken
            print("🔽 Daten werden heruntergeladen...")
            self._download_data()
            print("📦 Daten werden entpackt...")
            self._extract_data()

    def _download_data(self):
        """ Lädt die MovieSummaries-Daten herunter. """
        response = requests.get(self.DATA_URL, stream=True)
        if response.status_code == 200:
            with open(self.ARCHIVE_PATH, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            raise RuntimeError(f"❌ Fehler beim Download: Status {response.status_code}")

    def _extract_data(self):
        """ Entpackt die heruntergeladene TAR-Datei. """
        with tarfile.open(self.ARCHIVE_PATH, "r:gz") as tar:
            tar.extractall(self.EXTRACT_DIR)

    def _load_data(self):
        """ Überprüft die Existenz der Daten und lädt sie als Pandas DataFrames. """
        print(f"🔍 Überprüfe: {self.movie_metadata_path}")
        print(f"🔍 Überprüfe: {self.character_metadata_path}")

        if not self.movie_metadata_path.exists() or not self.character_metadata_path.exists():
            raise FileNotFoundError(
                f"❌ Fehlende Datensätze!\n"
                f"🔴 Erwartet: {self.movie_metadata_path}\n"
                f"🔴 Erwartet: {self.character_metadata_path}\n"
                f"⚠ Bitte stelle sicher, dass das Dataset richtig extrahiert wurde."
            )

        print("📂 Dateien gefunden! Lade in DataFrames...")

        object.__setattr__(self, "movies_df", pd.read_csv(self.movie_metadata_path, sep="\t", header=None))
        object.__setattr__(self, "actors_df", pd.read_csv(self.character_metadata_path, sep="\t", header=None))

        print("✅ Daten erfolgreich geladen!")
