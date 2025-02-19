import os
import pandas as pd
import matplotlib.pyplot as plt
from pydantic import BaseModel, PositiveInt, ConfigDict

class MovieData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    movie_metadata_path: str = r"C:\Users\Marti\Desktop\Nova SBE\T3 2025\AP\Group Assignment\MovieSummaries\movie.metadata.tsv"
    character_metadata_path: str = r"C:\Users\Marti\Desktop\Nova SBE\T3 2025\AP\Group Assignment\MovieSummaries\character.metadata.tsv"

    def __init__(self, **data):
        super().__init__(**data)
        
        object.__setattr__(self, "movies_df", None)
        object.__setattr__(self, "actors_df", None)
        
        self._load_data()
    
    def _load_data(self):
        print(f"Checking: {self.movie_metadata_path}")
        print(f"Checking: {self.character_metadata_path}")

        if not os.path.exists(self.movie_metadata_path) or not os.path.exists(self.character_metadata_path):
            raise FileNotFoundError(f"Missing dataset files.\n"
                                    f"Expected: {self.movie_metadata_path}\n"
                                    f"Expected: {self.character_metadata_path}\n"
                                    f"Please extract the dataset properly.")
        
        object.__setattr__(self, "movies_df", pd.read_csv(self.movie_metadata_path, sep="\t", header=None))
        object.__setattr__(self, "actors_df", pd.read_csv(self.character_metadata_path, sep="\t", header=None))

    def movie_type(self, N: PositiveInt = 10) -> pd.DataFrame:
        if not isinstance(N, int):
            raise ValueError("N must be an integer.")
        
        df = self.movies_df[3].value_counts().head(N).reset_index()
        df.columns = ["Movie_Type", "Count"]
        
        print("🔍 movie_type() DataFrame Sample:")
        print(df.head())
        print("Columns:", df.columns)
        
        return df
    
    def actor_count(self) -> pd.DataFrame:
        df = self.movies_df[8].apply(lambda x: len(str(x).split(','))).value_counts().reset_index()
        df.columns = ["Number_of_Actors", "Movie_Count"]
        return df
    
    def actor_distributions(self, gender: str, max_height: float, min_height: float, plot: bool = False) -> pd.DataFrame:
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
