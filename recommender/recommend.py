import tarfile

import numpy as np
import pandas as pd


class TrackRecommender:
    def __init__(self):
        with tarfile.open(".data/data.tar.gz", mode="r:gz") as tar:
            print("Reading data...")
            self.song_data = pd.read_json(tar.extractfile("data.json"))

    @staticmethod
    def calc_euclidian_distance(query: np.ndarray, array: np.ndarray) -> float:
        return np.linalg.norm(query - array)

    def resolve_song_id(self, song_id: str) -> dict[str, str]:
        """Get information about song based on the id."""
        song = pd.DataFrame(self.song_data[self.song_data["id"] == song_id])
        song = song[["id", "name", "album", "artists"]]
        return song.to_dict(orient="records")[0]

    def resolve_song_name_to_id(self, song_name: str) -> str:
        """Get id based on a song's name."""
        song_id = self.song_data[self.song_data["name"] == song_name]["id"]
        return song_id.to_string(index=False)

    def _get_query_array(self, song_id: str) -> np.ndarray:
        """Get the embedding for an id."""
        query_array = self.song_data[self.song_data["id"] == song_id]
        query_array = query_array[["First-Dimension", "Second-Dimension"]].to_numpy()
        return query_array

    def _calc_distances(self, query_array: np.ndarray) -> list[float]:
        distances = []

        for array in self.song_data[["First-Dimension", "Second-Dimension"]].to_numpy():
            dist = self.calc_euclidian_distance(query=query_array, array=array)

            # if euclidian distances was calculated between query song and itself
            if dist == 0.0:
                dist = np.nan
            distances.append(dist)

        return distances

    def recommend(self, song_id: str) -> dict[str, str]:
        """Recommend another song for a given id."""
        distances = self._calc_distances(query_array=self._get_query_array(song_id))

        # get index of id with minimal Euclidean distance
        # ignore the one missing value
        rec_index = np.nanargmin(distances)
        recommendation = self.song_data.loc[rec_index, "id"]
        # get additional info (album name, artist name, etc.)
        recommendation = self.resolve_song_id(song_id=recommendation)

        return recommendation
