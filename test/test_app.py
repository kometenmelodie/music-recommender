from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from litestar.testing import TestClient


def test_index(test_client: TestClient) -> None:
    with test_client as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK


def test_random(test_client: TestClient) -> None:
    with test_client as client:
        response = client.get("/random")
        assert response.status_code == HTTP_200_OK


def test_recommend(test_client: TestClient) -> None:
    with test_client as client:
        # successful response
        response = client.post(
            "/recommend", json={"track_name": "The Chain - 2004 Remaster"}
        )
        assert response.status_code == HTTP_201_CREATED

        # track name that does not exist
        response = client.post("/recommend", json={"track_name": "abc"})
        assert response.status_code == HTTP_404_NOT_FOUND
