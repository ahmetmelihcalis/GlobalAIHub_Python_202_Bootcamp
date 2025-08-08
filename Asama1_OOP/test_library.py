import pytest
import os
from library import Book, Library

TEST_DB_NAME = "test_library.db"

import time

@pytest.fixture
def library():
    # Windows'ta SQLite veritabanı dosyası bazen testler sırasında hemen serbest bırakılmıyor (dosya kilidi hatası oluşabiliyor).
    # Bu yüzden dosya silme işlemini birkaç kez denedim ve arada kısa bir süre bekleyici bir metod koydum.
    # Böylece PermissionError hatası önlendi ve testler sorunsuz çalıştı.
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

#TEST FONKSİYONLARI

#Bir Kitabın Eklenmesi, Bulunması ve Silinmesinin Testi
def test_full_book_lifecycle(library):

    #KİTAP OLUŞTURMA
    my_book = Book("Sefiller", "Victor Hugo", "978-605332-843-8")
    
    #KİTAP EKLEME
    library.add_book(my_book)
    
    #EKLENEN KİTABI BULMA VE DOĞRULAMA
    found_book = library.find_book("978-605332-843-8")
    assert found_book is not None
    assert found_book.title == "Sefiller"

    #KİTABI SİLME
    library.remove_book("978-605332-843-8")
    
    #SİLİNEN KİTABIN ARTIK BULUNAMADIĞINI DOĞRULA
    not_found_book = library.find_book("978-605332-843-8")
    assert not_found_book is None

#Boş Bilgiyle Kitap Oluşturma Testi
def test_invalid_book_creation():
    with pytest.raises(ValueError):
        Book("  ", "Geçerli Yazar", "12345")

# Aynı ISBN'li kitabı tekrar eklemeye çalışınca reddedilmesi testi
def test_duplicate_isbn_rejection(library, capsys):
    book1 = Book("1984", "George Orwell", "978-975071-855-3")
    library.add_book(book1)
    
    # Aynı kitabı tekrar eklemeyi deneme
    library.add_book(book1)
    
    captured = capsys.readouterr() 
    assert "zaten kütüphanede mevcut" in captured.out

#List_books fonksiyonun doğru çıktıyı ekrana bastığını kontrol testi
def test_list_books_output(library, capsys):

    #Hazırlık
    book1 = Book("Yerdeniz Büyücüsü", "Ursula K. Le Guin", "978-605314-258-3")
    book2 = Book("Dune", "Frank Herbert", "978-605792-273-3")
    library.add_book(book1)
    library.add_book(book2)
    
    #Kitapları listeleme
    library.list_books()
    
    #Çıktıyı yakalama ve içeriğini kontrol etme
    captured = capsys.readouterr().out
    
    assert "Yerdeniz Büyücüsü" in captured
    assert "Ursula K. Le Guin" in captured
    assert "978-605314-258-3" in captured
    assert "Dune" in captured
    assert "Frank Herbert" in captured
    assert "978-605792-273-3" in captured