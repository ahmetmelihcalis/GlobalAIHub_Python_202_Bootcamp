# main.py (Aşama 2'ye Uyarlanmış)
from library import Library

#Yeni handle_add_book fonksiyonu
def handle_add_book(library):
    print("\--- ISBN ile Yeni Kitap Ekle ---")
    isbn = input("Lütfen kitabın ISBN numarasını girin: ")
    
    if not isbn.strip():
        print("Hata: ISBN boş olamaz.")
        return
        
    # Artık tüm işi library.add_book metodu yapıyor.
    library.add_book(isbn.strip())

# --- BU FONKSİYONLAR HİÇ DEĞİŞMEDİ ---
#Kullanıcıdan ISBN alıp kitap silme işlemini yöneten fonksiyon
def handle_remove_book(library):
    isbn = input("Silinecek kitabın ISBN'ini girin: ")
    library.remove_book(isbn)
#Kullanıcıdan ISBN alıp kitap arama işlemini yöneten fonksiyon
def handle_find_book(library):
    isbn = input("Aranacak kitabın ISBN'ini girin: ")
    book_found = library.find_book(isbn)
    if book_found:
        print("Kitap bulundu:")
        print(f"{book_found}")
    else:
        print(f"Bu ISBN ile bir kitap bulunamadı.")

# Ana fonksiyon
def main():
    my_library = Library()
    menu_actions = {
        '1': handle_add_book,
        '2': handle_remove_book,
        '3': my_library.list_books,
        '4': handle_find_book,
    }

    while True:
        print("===== Kütüphane Yönetim Sistemi =====")
        print("1. Kitap Ekle (ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")
        print("=====================================")

        choice = input("Lütfen bir seçim yapınız (1-5): ")

        if choice == '5':
            print("Programdan çıkılıyor.")
            break
        
        action = menu_actions.get(choice)
        
        if action:
            if choice in ['1', '2', '4']:
                action(my_library)
            else: 
                action()
        else:
            print("Geçersiz seçim! Lütfen 1 ile 5 arasında bir sayı girin.")


if __name__ == "__main__":
    main()