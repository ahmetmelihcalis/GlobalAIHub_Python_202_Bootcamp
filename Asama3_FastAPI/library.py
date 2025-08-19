import sqlite3
import httpx
from typing import List, Optional

class Book:
    def __init__(self, title, author, isbn):
        if not title.strip() or not author.strip() or not isbn.strip():
            raise ValueError("Title, author ve ISBN boş olamaz.")
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'


# Library Sınıfı - API için yeni metotlar eklendi
class Library:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT, author TEXT, isbn TEXT PRIMARY KEY
                )
            ''')

    # --- API İÇİN YAZILMIŞ YENİ METOTLAR ---
    #Bu metotlar, ekrana bir şey printlemek yerine,FastAPI'ye veri döndürüyor.

    def add_book_from_api(self, isbn: str) -> Optional[Book]:
        """
        API için kitap ekler.
        """
        OPEN_LIBRARY_URL = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(OPEN_LIBRARY_URL, follow_redirects=True, timeout=10.0)
            if response.status_code != 200:
                return None
            
            data = response.json()
            title = data.get("title", "Başlık Bilgisi Yok")
            
            authors_data = data.get("authors", [])
            author_names = []
            for author in authors_data:
                key = author.get("key")
                if key:
                    author_url = f"https://openlibrary.org{key}.json"
                    author_resp = httpx.get(author_url, timeout=5.0)
                    if author_resp.status_code == 200:
                        name = author_resp.json().get("name")
                        if name: author_names.append(name)
            
            author = ", ".join(author_names) if author_names else "Yazar Bilgisi Yok"
            
            new_book = Book(title, author, isbn)
            
            # Veritabanına ekleme
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                    (new_book.isbn, new_book.title, new_book.author)
                )
            return {
                "kitap_ismi": new_book.title,
                "yazar": new_book.author,
                "isbn": new_book.isbn
            }
        except (httpx.RequestError, sqlite3.IntegrityError, ValueError, Exception):
            return None

    def list_books_for_api(self) -> List[dict]:
        """API için kitapları listeler.."""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books_data = cursor.fetchall()
            return [
                {
                    "kitap_ismi": row["title"],
                    "yazar": row["author"],
                    "isbn": row["isbn"]
                }
                for row in books_data
            ]

    def remove_book_for_api(self, isbn: str) -> bool:
        """API için kitap siler."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            return cursor.rowcount > 0

    def find_book_for_api(self, isbn: str) -> Optional[dict]:
        """API için kitap bulur."""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
            row = cursor.fetchone()
            if row:
                return {
                    "kitap_ismi": row["title"],
                    "yazar": row["author"],
                    "isbn": row["isbn"]
                }
            return None
