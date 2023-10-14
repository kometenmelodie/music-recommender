from recommender import TrackRecommender

rec = TrackRecommender()

# get the Spotify id for the given song
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
