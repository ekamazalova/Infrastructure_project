
from fastapi.testclient import TestClient
from app_final import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == "1.1.0"


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 4


def test_book_by_id():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Мастер и Маргарита"


def test_book_not_found():
    response = client.get("/books/999")
    assert response.status_code == 404


def test_search_by_author():
    response = client.get(
        "/books/search",
        params={"query": "Булгаков"}
    )
    assert response.status_code == 200
    assert len(response.json()["books"]) == 1


def test_search_missing_query():
    response = client.get("/books/search")
    assert response.status_code == 422


def test_filter_by_genre():
    response = client.get("/books/genre/фантастика")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 2


def test_genre_not_found():
    response = client.get("/books/genre/вестерн")
    assert response.status_code == 404


def test_library_info():
    response = client.get("/library-info")
    assert response.status_code == 200
    assert response.json()["total_books"] == 4
    assert "library_name" in response.json()