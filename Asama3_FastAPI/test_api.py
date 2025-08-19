import pytest
from fastapi.testclient import TestClient
import os
import time
from api import app, library 

#Test Ortamı Kurulumu
@pytest.fixture
def client():
    db_file = library.db_name
    if os.path.exists(db_file):
        for _ in range(3):
            try:
                os.remove(db_file)
                break
            except PermissionError:
                time.sleep(0.1)
    library.__init__(db_name=db_file)
    with TestClient(app) as c:
        yield c
    if os.path.exists(db_file):
        for _ in range(3):
            try:
                os.remove(db_file)
                break
            except PermissionError:
                time.sleep(0.1)

#Test Fonksiyonları
# Artık testlerimiz, 'library' metotlarını doğrudan değil,API endpoint'lerini çağırarak çalışacak.

# Kütüphane boşken kitapları listeleme testi
def test_get_all_books_empty(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == []

# Kitap ekleme testi
def test_add_book_success(client, mocker):
    fake_isbn = "978-0451524935"
    fake_response_json = {
        "title": "1984",
        "authors": [{"key": "/authors/OL22927A"}]
    }
    fake_author_json = {"name": "George Orwell"}

    def fake_httpx_get(url, *args, **kwargs):
        if "isbn" in url:
            mock_resp = mocker.Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = fake_response_json
            return mock_resp
        elif "/authors/" in url:
            mock_resp = mocker.Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = fake_author_json
            return mock_resp
        else:
            raise RuntimeError("Beklenmeyen URL: " + url)

    mocker.patch("library.httpx.get", side_effect=fake_httpx_get)

    response = client.post("/books", json={"isbn": fake_isbn})
    assert response.status_code == 201
    data = response.json()
    assert data["kitap_ismi"] == "1984"
    assert data["isbn"] == fake_isbn
    assert "George Orwell" in data["yazar"]

# Kitap ekleme API'si başarısız olursa testi
def test_add_book_api_fails(client, mocker):
    # Hazırlık: API'nin 404 döndüğü durumu taklit etme
    fake_isbn = "0000000000000"
    mock_response = mocker.Mock(status_code=404)
    mocker.patch("library.httpx.get", return_value=mock_response)

    # Eylem
    response = client.post("/books", json={"isbn": fake_isbn})
    
    # Doğrulama
    assert response.status_code == 400
    assert "bulunamadı" in response.json()["detail"]

#Full test akışı(kitap ekleme,listeleme,tek tek bulma ve silme)
def test_full_api_lifecycle(client, mocker):
    # 1. KİTAP EKLEME
    fake_response_json = {"title": "Dune", "authors": [{"key": "/authors/FrankHerbert"}]}
    fake_author_json = {"name": "Frank Herbert"}

    def fake_httpx_get(url, *args, **kwargs):
        if "isbn" in url:
            mock_resp = mocker.Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = fake_response_json
            return mock_resp
        elif "/authors/FrankHerbert" in url:
            mock_resp = mocker.Mock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = fake_author_json
            return mock_resp
        else:
            raise RuntimeError("Beklenmeyen URL: " + url)

    mocker.patch("library.httpx.get", side_effect=fake_httpx_get)

    add_response = client.post("/books", json={"isbn": "978-0441013593"})
    assert add_response.status_code == 201

    list_response = client.get("/books")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["kitap_ismi"] == "Dune"

    single_response = client.get("/books/978-0441013593")
    assert single_response.status_code == 200
    assert single_response.json()["kitap_ismi"] == "Dune"

    delete_response = client.delete("/books/978-0441013593")
    assert delete_response.status_code in (200, 204)
    if delete_response.status_code == 200:
        deleted = delete_response.json()
        assert deleted["kitap_ismi"] == "Dune"

    final_list_response = client.get("/books")
    assert len(final_list_response.json()) == 0