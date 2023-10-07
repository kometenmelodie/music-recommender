import numpy as np
import pandas as pd


class TrackRecommender:
    def __init__(self, song_data: bool = False):
        self.embedding = pd.read_csv(".data/umap_embedding.csv")
        if song_data:
            self.song_data = pd.read_csv(
                ".data/tracks_features.csv", usecols=["id", "name", "album", "artists"]
            )

    @staticmethod
    def calc_euclidian_distance(query: np.ndarray, array: np.ndarray) -> float:
        return np.linalg.norm(query - array)

    def _check_attr_song_data(self) -> None:
        if not hasattr(self, "song_data"):
            raise AttributeError(
                "Song data was not loaded. Please call TrackRecommender with"
                "song_data=True."
            )

    def resolve_song_id(self, song_id: str) -> dict[str, str]:
        """Get information about song based on the Song-ID."""
        self._check_attr_song_data()
        song = pd.DataFrame(self.song_data[self.song_data["id"] == song_id])
        return song.to_dict(orient="records")[0]

    def resolve_song_name_to_id(self, song_name: str) -> str:
        """Get Song-ID based on a song's name."""
        self._check_attr_song_data()
        song_id = self.song_data[self.song_data["name"] == song_name]["id"]
        return song_id.to_string(index=False)

    def _get_query_array(self, song_id: str) -> np.ndarray:
        """Get the embedding for a Song-ID."""
        query_array = self.embedding[self.embedding["Song-ID"] == song_id]
        query_array = query_array[["First-Dimension", "Second-Dimension"]].to_numpy()
        return query_array

    def _calc_distances(self, query_array: np.ndarray) -> list[float]:
        distances = []

        for array in self.embedding[["First-Dimension", "Second-Dimension"]].to_numpy():
            dist = TrackRecommender.calc_euclidian_distance(
                query=query_array, array=array
            )

            # if euclidian distances was calculated between query song and itself
            if dist == 0.0:
                dist = np.nan
            distances.append(dist)

        return distances

    def recommend(self, song_id: str) -> str:
        """Recommend another song for a given Song-ID."""
        distances = self._calc_distances(query_array=self._get_query_array(song_id))

        # get index of Song-ID with minimal Euclidean distance
        # ignore the one missing value
        rec_index = np.nanargmin(distances)
        recommendation = self.embedding.loc[rec_index, "Song-ID"]

        return recommendation
