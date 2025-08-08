import sqlite3

#Book Sınıfı (Validasyon ile)
class Book:
    def __init__(self, title, author, isbn):
        if not title.strip() or not author.strip() or not isbn.strip():
            raise ValueError("Title, author ve ISBN boş olamaz.")
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = isbn.strip()

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


#Library Sınıfı
class Library:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    title TEXT,
                    author TEXT,
                    isbn TEXT PRIMARY KEY
                )
            ''')

#Kütüphane Kitap Ekleme,Silme,Listeleme,Bulma İşlemleri
    def add_book(self, book):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (isbn, title, author) VALUES (?, ?, ?)",
                    (book.isbn, book.title, book.author)
                )
            print(f"Başarılı: {book} kütüphaneye eklendi.")
        except sqlite3.IntegrityError:
            print(f"Hata: Bu ISBN ({book.isbn}) zaten kütüphanede mevcut.")

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
            print("Kütüphanede hiç kitap yok.")
            return
        
        print("--- Kütüphanedeki Kitaplar ---")
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
