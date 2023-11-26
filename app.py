from typing import Annotated

from litestar import Litestar, get, post
from litestar.exceptions import NotFoundException
from litestar.params import Body
from pydantic import BaseModel, Field

from recommender import TrackRecommender


class Track(BaseModel):
    track_id: str = Field(alias="id")
    name: str
    album: str
    artists: str


class InputTrack(BaseModel):
    track_name: str


# load recommender
rec = TrackRecommender()


@get("/")
async def index() -> str:
    return "Welcome, to the recommender API!"


@get("/random")
async def random() -> Track:
    """Get a random track."""
    track = rec.song_data.sample(n=1)
    track = track.to_dict(orient="records")[0]
    track = Track.model_validate(track)

    return track


@post("/recommend")
async def recommend(
    data: Annotated[
        InputTrack,
        Body(
            title="Get recommendation",
            examples=[InputTrack(track_name="The Chain - 2004 Remaster")],
        ),
    ],
) -> Track:
    """Get a recommendation based on a given track."""
    track_id = rec.resolve_song_name_to_id(song_name=data.track_name)

    if track_id is None:
        raise NotFoundException(f"Track {data.track_name} was not found.")

    track = rec.recommend(song_id=track_id)
    track = Track.model_validate(track)

    return track


app = Litestar([index, random, recommend])
