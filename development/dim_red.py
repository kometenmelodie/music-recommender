import pandas as pd
import umap
from sklearn.preprocessing import StandardScaler

# data set can be downloaded here:
# https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs
data = pd.read_csv("../.data/tracks_features.csv")

# pick desired features
feature_columns = [
    "danceability",
    "energy",
    "key",
    "mode",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
    "time_signature",
]
data = data[feature_columns]

# scale data
scaler = StandardScaler()
data = scaler.fit_transform(data)

reducer = umap.UMAP(n_components=2, random_state=135)
embedding = reducer.fit_transform(data)
