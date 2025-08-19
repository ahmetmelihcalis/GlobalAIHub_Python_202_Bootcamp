
# Global AI Hub Python 202 Bootcamp Projesi

## Genel Bakış
Bu proje, Global AI Hub Python 202 Bootcamp kapsamında öğretilen üç konuyu (OOP, harici API kullanımı ve FastAPI) pekiştirmek amaçlı oluşturulmuştur. Proje birbiri üzerine inşa edilen üç aşamadan oluşur:

**Aşama 1:** OOP ile terminalde çalışan kütüphane uygulaması

**Aşama 2:** Harici API (Open Library) ile kitap bilgilerini çekme

**Aşama 3:** FastAPI ile web tabanlı kütüphane API'si

---
## Kurulum
1. **Projeyi klonlayın:**
	 ```bash
	 git clone https://github.com/ahmetmelihcalis/GlobalAIHub_Python_202_Bootcamp.git
	 ```

2. **Klonladıktan sonra ilgili konumuna gidin:**
	 ```bash
	 cd GlobalAIHub_Python_202_Bootcamp
	 ```


3. **Gerekli paketleri yükleyin:**

	 - pip ile klasik kurulum:
		 ```bash
		 pip install -r Asama2_API/requirements.txt
		 pip install -r Asama3_FastAPI/requirements.txt
		 ```

	 - uv ile hızlı kurulum:
		 ```bash
		 pip install uv  # Eğer yüklü değilse
		 uv pip install -r Asama2_API/requirements.txt
		 uv pip install -r Asama3_FastAPI/requirements.txt
		 ```
---

## Kullanım

### Aşama 1 (OOP Terminal Uygulaması)
- Terminalden çalıştırmak için:
	```bash
	cd Asama1_OOP
	python main.py
	```
- Menüden kitap ekleyebilir, silebilir, arayabilir ve listeleyebilirsiniz.
- Kitap eklerken tüm bilgileri (başlık, yazar, yıl, ISBN) manuel girmeniz gerekir.

### Aşama 2 (API Destekli Terminal Uygulaması)
- Terminalden çalıştırmak için:
	```bash
	cd Asama2_API
	python main.py
	```
- Menüden kitap ekleyebilir, silebilir, arayabilir ve listeleyebilirsiniz.
- Kitap eklerken sadece ISBN girmeniz yeterlidir, başlık ve yazar bilgileri otomatik olarak Open Library API'den çekilir.

### Aşama 3 (Web API)
- API sunucusunu başlatmak için:
	```bash
	cd Asama3_FastAPI
	uvicorn api:app --reload
	```
- Tarayıcıdan [http://localhost:8000/docs](http://localhost:8000/docs) adresine giderek interaktif API dokümantasyonunu kullanabilirsiniz.

#### API Endpointleri

- **GET /books**: Tüm kitapları listeler.
- **POST /books**: ISBN ile kitap ekler. (Body: `{ "isbn": "..." }`)
- **GET /books/{isbn}**: Belirli ISBN'li kitabı getirir.
- **DELETE /books/{isbn}**: Belirli ISBN'li kitabı siler.

---

## Testler
- Tüm aşamalarda pytest ile testler yazılmıştır. Testler, hem temel işlevleri hem de hata durumlarını kapsar.

- Testleri çalıştırmak için ilgili klasörde:
	```bash
	pytest
	```
	veya
	```bash
	pytest -v
	```

- **Aşama 1 (OOP):**
	- Kitap ekleme, silme, arama ve listeleme fonksiyonlarının testi

- **Aşama 2 (API Entegrasyonu):**
	- API'den veri çekerek kitap ekleme testi
	- API başarısız olursa mock ile hata yönetimi testi

- **Aşama 3 (FastAPI):**
	- API endpoint'leri üzerinden kitap ekleme, silme, listeleme ve hata durumları testi
	- Dış API çağrılarının mock'lanarak izole test edilmesi

---


## Notlar
- **Veri Saklama:**
	- Aşama 1, 2 ve 3'te tüm kitap verileri yerel bir SQLite veritabanında saklanır. Programı veya API sunucusunu tekrar başlattığınızda verileriniz kaybolmaz.
	- Her aşamanın kendi veritabanı dosyası vardır (ör. `library.db`).

- **API Kullanımı:**
	- Aşama 2'de kitap eklerken sadece ISBN girmeniz yeterlidir; başlık ve yazar bilgileri otomatik olarak Open Library API'den çekilir.
	- API bağlantı hatalarında kullanıcıya bilgilendirici hata mesajı gösterilir.

- **Web API (Aşama 3):**
	- FastAPI ile RESTful bir web servisi sunulmuştur.
	- `/docs` ve `/redoc` ile otomatik API dokümantasyonu sağlanır.
	- API üzerinden kitap ekleme, silme ve listeleme işlemleri yapılabilir.

- **Testler ve Mocklama:**
	- Dış API çağrıları testlerde mock'lanmıştır, böylece testler hızlı ve dış servislere bağımlı değildir.

- **Kurulum:**
	- Kurulumda pip veya uv kullanılabilir.

