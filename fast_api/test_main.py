from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

TEST_FILE_PATH = "../test_files/1000.csv"


def test_get_sum_csv():
    response = client.get("/sum_csv")
    assert response.status_code == 405


def test_post_sum_csv_empty():
    response = client.post("/sum_csv", data={})
    assert response.status_code == 422


def test_post_sum_csv():
    response = client.post("/sum_csv", files={"file":open(TEST_FILE_PATH, "rb")})
    assert response.status_code == 200
