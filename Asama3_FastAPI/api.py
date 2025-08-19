
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

from library import Library, Book

app = FastAPI(
    title="Kütüphane Yönetim Sistemi",
    description="Global AI Hub Python 202 Bootcamp Kütüphane Yönetim Sistemi Projesi"
)

library = Library(db_name="api_library.db")

#Pydantic Veri Modelleri
# Bu model, API'den dışarıya bir kitap verisi döndürürken kullanılacak.
class BookModel(BaseModel):
    kitap_ismi: str
    yazar: str
    isbn: str

# Bu model, API'ye yeni bir kitap eklemek için dışarıdan veri alırken kullanılacak.
class ISBNModel(BaseModel):
    isbn: str = Field(..., description="Eklenecek kitabın 10 veya 13 haneli ISBN numarası")


#API Endpoint'leri
@app.get("/")
def home():
    """
    http://127.0.0.1:8000 sayfasındaki ana ekran mesajını gösterir.
    """
    return {"Merhaba! Kütüphane API'sine hoş geldiniz."}

@app.get("/books", response_model=List[BookModel])
def kütüphanedeki_tüm_kitapları__getirme():
    """
    Kütüphanedeki tüm kitapların bir listesini JSON formatında döndürür.
    """
    all_books = library.list_books_for_api()
    return all_books

@app.get("/books/{isbn}", response_model=BookModel)
def tek_kitap_getirme(isbn: str):
    """
    Verilen ISBN'e sahip tek bir kitabı döndürür.
    Eğer kitap bulunamazsa 404 hatası verir.
    """
    book = library.find_book_for_api(isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Bu ISBN ile bir kitap bulunamadı.")
    return book

@app.post("/books", response_model=BookModel, status_code=201)
def yeni_kitap_ekleme(isbn_data: ISBNModel):
    """
    POST request'in body'sinden bir ISBN alır, 
    Open Library'den verileri çeker ve kitabı kütüphaneye ekler.
    """
    added_book = library.add_book_from_api(isbn_data.isbn)
    
    if added_book is None:
        raise HTTPException(
            status_code=400, 
            detail="Kitap bu ISBN ile Open Library'de bulunamadı, zaten mevcut veya başka bir hata oluştu."
        )
    
    return added_book

@app.delete("/books/{isbn}", status_code=204)
def kitap_silme(isbn: str):
    """
    Belirtilen ISBN'e sahip kitabı kütüphaneden siler.
    Başarılı silme işleminde (204 No Content) bir body döndürmez.
    """
    success = library.remove_book_for_api(isbn)

    # library.py'den False döndüğünde, kitabın bulunamadığını anlarız.
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Bu ISBN ile eşleşen bir kitap kütüphanede bulunamadı."
        )
    # Başarılı olunca FastAPI otomatik olarak 204 status kodu ve boş body döndürecek.
    return 