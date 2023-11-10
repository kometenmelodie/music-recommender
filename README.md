# Music recommender system 🎸

... uses
[this](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs)
Spotify data set with 1.2 million songs with features such as danceability,
energy, key, acousticness, etc.

The data set was reduced to two dimensions using an unsupervised UMAP.
This embedding is the backbone for the `TrackRecommender`. The inner workings
of the recommender are pretty simple. Based on an input song, the track 
with the lowest euclidian distance to the input is found. The distance is 
calculated using the embedding.

To use the recommender, a `Dockerfile` is provided, which will set up a 
[`litestar`](https://litestar.dev/) API.

## Usage

### Docker

To build and run the image, use the following commands:

````bash
docker build -t rec-api .
docker run -d -p 8001:8001 rec-api
````

The API is now available at `localhost:8001`. To visit the 
(`swagger`) documentation, head to `localhost:8001/schema/swagger`.

The endpoint `/recommend` requires a request body which contains a track for
which the recommendation should be based on.

Following `json` is a valid request body:
````json
{
  "track": "The Chain - 2004 Remaster"
}
````

Which leads to this response (the recommendation):

````json
{
	"track_id": "4o6yLK8SOQ2RdfosVaaBBv",
	"name": "Let's Eat",
	"album": "A Certain Distance",
	"artists": "['Dave Nachmanoff']"
}
````

### Python

Alternatively, with `Python3.11` installed run:

````bash
python -m pip install poetry
poetry install
````

to set up the environment.

Here's a small example on how to use the `TrackRecommender`, without 
spinning up the API:

````python
from recommender import TrackRecommender

rec = TrackRecommender()

# get the Spotify id for Fleetwood Mac's - The Chain 
the_chain = rec.resolve_song_name_to_id(song_name="The Chain - 2004 Remaster")

# >>> the_chain
# '5e9TFTbltYBg2xThimr0rU'

# get a recommendation
rec_track = rec.recommend(song_id=the_chain)

# >>> rec_track
# {
#     "id": "4o6yLK8SOQ2RdfosVaaBBv",
#     "name": "Let's Eat",
#     "album": "A Certain Distance",
#     "artists": "['Dave Nachmanoff']",
# }
````

### UMAP visualization

The below plot visualizes the above-mentioned embedding used for 
recommending tracks.

![](.data/plots/umap.png)