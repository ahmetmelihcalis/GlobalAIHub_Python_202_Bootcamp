#library.py (Aşama 2'ye Uyarlanmış)
import sqlite3
import httpx #Yeni kütüphane

# Book Sınıfı (Validasyon ile) - BU KISIM HİÇ DEĞİŞMEDİ
class Book:
    def __init__(self, title, author, isbn):
        if not title.strip() or not author.strip() or not isbn.strip():
            raise ValueError("Title, author ve ISBN boş olamaz.")
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()

    def __str__(self):
        return f'"{self.title}" by {self.author} (ISBN: {self.isbn})'


# Library Sınıfı
class Library:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        # Bu metot hiç değişmedi.
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT,
                    author TEXT,
                    isbn TEXT PRIMARY KEY
                )
            ''')

    #YENİ add_book METODU
    def add_book(self, isbn: str):
        print(f"\n{isbn} ISBN'li kitap için internetten bilgi aranıyor...")
        api_url = f"https://openlibrary.org/isbn/{isbn}.json"
        
        try:
            # 1. API'den veriyi alma
            response = httpx.get(api_url, follow_redirects=True, timeout=10.0)
            
            if response.status_code == 404:
                print("Hata: Bu ISBN ile Open Library'de bir kitap bulunamadı.")
                return
            
            response.raise_for_status() # Diğer HTTP hatalarını kontrol etme

            # 2. JSON verisini işleme
            data = response.json()
            title = data.get("title", "Başlık Bilgisi Yok")
            
            authors_data = data.get("authors", [])
            author_names = []
            for author in authors_data:
                key = author.get("key")
                if key:
                    author_url = f"https://openlibrary.org{key}.json"
                    try:
                        author_resp = httpx.get(author_url, timeout=5.0)
                        if author_resp.status_code == 200:
                            author_json = author_resp.json()
                            name = author_json.get("name")
                            if name:
                                author_names.append(name)
                    except Exception:
                        continue
            author = ", ".join(author_names) if author_names else "Yazar Bilgisi Yok"
            
            # 3. Yeni bir Book nesnesi oluşturma
            new_book = Book(title, author, isbn)
            
            # 4. Veritabanına ekleme
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                        (new_book.isbn, new_book.title, new_book.author)
                    )
                print(f"Başarılı: {new_book} kütüphaneye eklendi.")
            except sqlite3.IntegrityError:
                print(f"Hata: Bu ISBN ({new_book.isbn}) zaten kütüphanede mevcut.")

        except httpx.RequestError as e:
            print(f"Hata: API'ye bağlanırken bir sorun oluştu. İnternetinizi kontrol edin. Detay: {e}")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")


    # --- BU METOTLARI HİÇ DEĞİŞTİRMEDİM ---
    def remove_book(self, isbn):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE isbn = ?", (isbn,))
            if cursor.rowcount == 0:
                print(f"Hata: Bu ISBN ({isbn}) ile eşleşen bir kitap bulunamadı.")
            else:
                print(f"Başarılı: {isbn} ISBN'li kitap silindi.")

    def list_books(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            books_data = cursor.fetchall()

        if not books_data:
            print("\nKütüphanede hiç kitap yok.")
            return
        
        print("\n--- Kütüphanedeki Kitaplar ---")
        for row in books_data:
            book = Book(title=row['title'], author=row['author'], isbn=row['isbn'])
            print(book)
        print("----------------------------")

    def find_book(self, isbn):
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE isbn = ?", (isbn,))
            row = cursor.fetchone()
        
        if row:
            return Book(isbn=row['isbn'], title=row['title'], author=row['author'])
        else:
            return None