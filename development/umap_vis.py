import pandas as pd
import plotly.express as px

embedding = pd.read_csv("../.data/umap_embedding.csv")
data = pd.read_csv("../.data/tracks_features.csv")

embedding["Song-Key"] = data["key"].astype(str)
umap_embedding = px.scatter(
    embedding,
    x="First-Dimension",
    y="Second-Dimension",
    color="Song-Key",
    opacity=0.7,
    category_orders={
        "Song-Key": [str(key) for key in sorted(data["key"].unique().tolist())]
    },
    custom_data=[data["artists"], data["name"], data["album"]],
    title="1.2 Million Songs (Spotify data set)<br>"
    "<sup>UMAP 2D embedding - colored by song key</sup>",
)
umap_embedding.update_traces(
    hovertemplate="Artist: <b>%{customdata[0]}</b><br>"
    "Song title: <b>%{customdata[1]}</b><br>"
    "Album: %{customdata[2]}<br>"
)
umap_embedding.update_layout(
    plot_bgcolor="black", paper_bgcolor="black", font_color="white"
)
umap_embedding.write_html("../.data/plots/umap.html")
