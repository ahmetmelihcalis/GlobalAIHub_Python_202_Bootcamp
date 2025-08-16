# Bu dosyada mock ile test yapmayı tercih ettim. Dış API'ye bağlanmadan sadece kendi kodumun (veri işleme, hata yönetimi, veritabanı işlemleri) doğru çalışıp çalışmadığını kontrol etmeyi hedefledim.

import pytest
import os
import httpx
from library import Book, Library

TEST_DB_NAME = "test_library.db"

import time

@pytest.fixture
def library():
    for _ in range(3):
        try:
            if os.path.exists(TEST_DB_NAME):
                os.remove(TEST_DB_NAME)
            break
        except PermissionError:
            time.sleep(0.1)

    lib = Library(db_name=TEST_DB_NAME)
    yield lib

    for _ in range(3):
        try:
            if os.path.exists(TEST_DB_NAME):
                os.remove(TEST_DB_NAME)
            break
        except PermissionError:
            time.sleep(0.1)


# --- YENİ API TESTLERİ ---
#Başarılı bir API cevabıyla kitap ekleme testi
def test_add_book_from_api_success(library, mocker):
    # 1. Hazırlık: Sahte bir API cevabı oluştur ve httpx.get'i taklit etmesini söyle.
    fake_isbn = "978-0321765723"
    fake_response_json = {
        "title": "Yüzüklerin Efendisi",
        "authors": [{"key": "/authors/OL26320A"}]
    }
    # httpx.get çağrıldığında, internete gitmek yerine bu sahte cevabı döndür.
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_response_json
    mocker.patch("httpx.get", return_value=mock_response)
    
    # 2. Eylem
    library.add_book(fake_isbn)
    
    # 3. Doğrulama
    found_book = library.find_book(fake_isbn)
    assert found_book is not None
    assert found_book.title == "Yüzüklerin Efendisi"

#API'den 404 hatası alındnığında ne olduğunu test etme
def test_add_book_api_not_found(library, mocker, capsys):
    # Hazırlık: 404 durumu taklidi
    fake_isbn = "000-000000-000-0"
    mock_response = mocker.Mock(status_code=404)
    mocker.patch("httpx.get", return_value=mock_response)
    
    # Eylem
    library.add_book(fake_isbn)
    
    # Doğrulama
    captured = capsys.readouterr()
    assert "bir kitap bulunamadı" in captured.out
    assert library.find_book(fake_isbn) is None # Kitabın eklenmediğini kontrol et.

#İnternet bağlantısı hatası testi
def test_add_book_api_request_error(library, mocker, capsys):
    # Hazırlık: httpx.get'in bir hata fırlatmasını taklit et.
    fake_isbn = "111-111111-111-1"
    mocker.patch("httpx.get", side_effect=httpx.RequestError("Bağlantı Hatası"))

    # Eylem
    library.add_book(fake_isbn)

    # Doğrulama
    captured = capsys.readouterr()
    assert "API'ye bağlanırken bir sorun oluştu" in captured.out
    assert library.find_book(fake_isbn) is None

#Bu kısım değişmedi
def test_invalid_book_creation():
    with pytest.raises(ValueError):
        Book("  ", "Geçerli Yazar", "12345")