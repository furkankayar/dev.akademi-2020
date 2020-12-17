# furkankayar27 - dev.akademi2020

### Kurulum

PostgreSQL kurulu olmalı ve Devakademi/settings.py dosyasında DATABASES isimli dictionary üzerinde gerekli ayarlamalar yapılmalı.
Veritabanı backup dosyası yüklenmeli:

> sudo su - postgres <br/>
> psql db_name < backup.sql 

### Veritabanının oluşturulması için bir yol daha (Ama uzun sürecektir). Migration işleminden sonra yapılmalı

> python3 manage.py runscript load_db

### Eğer PostgreSQL ile uğraşmak istemezseniz Devakademi/settings.py dosyasında PostgreSQL'in tanımlı olduğu dictionary'yi yoruma alın (99. satır) ve SQLite'ın tanımlı olduğu dictionary'den (90. satır) yorumu kaldırın. Bütün veri repository'de bulunan db.sqlite3 dosyasının içine de yazıldı. Oradan okuyacaktır.

### Projenin Çalıştırılması

> git clone https://gitlab.com/dev.akademi2020/furkankayar27-dev-akademi2020.git <br/>
> cd furkankayar27-dev-akademi2020/ <br/>
> python3 -m venv env <br/>
> source env/bin/activate <br/>
> pip install -r requirements.txt <br/>
> python3 manage.py migrate <br/>
> python3 manage.py runserver

### Runserver komutuyla herhangi bir port belirtmeden çalıştırınca otomatik olarak 8000 portunda çalışacaktır. Bu yüzden bu portta çalışan başka bir uygulama olmamalı.

### Endpointler (Test ederken GET, POST, PUT istekleri yanlış seçilirse exception alınabilir. Hata kontrolü için çok zaman ayıramadım.)


* [POST] /api/auth 
    * Request Body: { "username": "username", "password": "password" }
    * Endpoint daha önce kullanılmamış bir username ile kullanıldığında yeni kullanıcı oluşturulur.
    * Daha önceden kullanılmış bir username ile kullanıldığında doğru şifre girilmelidir.
    * Geriye token bilgisi döner ve authentication gerekli olan endpointler için token Authorization isimli bir headerda gönderilmelidir.
        * Örnek kullanım: Authorization: Token f63f688e5c8bb5f422ee20a82a8050f4efffcd21 (Tokenin başına token kelimesi eklenmeli)
<hr/>

* [POST] /api/classified/myList/?page=1&size=2   (myList keywordünden sonraki slash önemli, koyulmazsa exception verecektir)
    * Page ve size parametre olarak verilmeli. Eğer page 50 den yüksek olursa 50 olarak kabul edilir.
    * Authorization token header olarak ayarlanmalı.
    * Bu endpoint sonuç olarak tokene sahip olan kullanıcının atandığı ilanları getirecektir. (Kullanıcının ID'si kayıt olduğunda mevcuttaki ilanların adminID'leri içerisinden rastgele seçilir.)
<hr/>

* [GET] /api/classified/load?id=92475536 
    * id parametre olarak verilmeli.
    * Eğer idye sahip bir ilan varsa bilgileri getirilir.
<hr/>

* [POST] /api/classified/post
    * Request Body: {"sellerID": "gkgCBkn", "title": "test", "description": "test", "price" : 1000, "date" : 12317, "expiryDate": 213223}
    * Bu endpoint sisteme yeni bir ilan eklemek için kullanılabilir. Yeni eklenen ilanlarda status otomatik olarak "WAITING_APPROVAL" ve adminID "0" olarak atanır.
    * Request body'de eksik parametre olması kabul edilmez.  
<hr/>

* [GET] /api/classified/list?page=1&size=2 
    * Page ve size parametre olarak verilmeli. Eğer page 50 den yüksek olursa 50 olarak kabul edilir.
    * Belirtilen sayfa sayısındaki belirtilen kadar ilan getirilir.
 <hr/>

* [POST] /api/post/category 
    * Authorization token header olarak ayarlanmalı.
    * Request Body: { "post_id": 92475536, "category_id": 16465 }
    * İstenen ilana istenen kategoriyi ekler. İlan 7 kategoriye sahipse eklenmez.
<hr/>

* [DELETE] /api/post/category 
    * Authorization token header olarak ayarlanmalı.
    * Request Body: { "post_id": 92475536, "category_id": 16465 }
    * İstenen ilandan istenen kategoriyi çıkartır. Eğer kategori ilanda zaten yoksa uygun cevap verir.
<hr/>

* [POST] /api/post/status 
    * Authorization token header olarak ayarlanmalı.
    * Request Body: { "post_id": 503820207, "status": "ACTIVE" }
    * İstenen ilan eğer "WAITING_APPROVAL" durumundaysa admin tarafından "ACTIVE" veya "REJECTED" durumuna geçirilebilir.
    * Bu işlemin sonucunda ilandaki adminID değeri işlemi yapan adminin id'si olarak atanır.
<hr/>

* [GET] /api/category/?page=1&size=20 
    * Page ve size parametre olarak verilmeli. Eğer page 50 den yüksek olursa 50 olarak kabul edilir.
    * Authorization token header olarak ayarlanmalı.
    * Bu endpoint sistemde kayıtlı olan kategorileri liste halinde getirir.
<hr/>

* [POST] /api/category/  (Sondaki slash bu endpointe de önemli.)
    * Authorization token header olarak ayarlanmalı.
    * Request Body: { "id": 22, "title": "test" }
    * Bu endpoint sisteme yeni bir kategori eklenmesini sağlar.
<hr/>

* [PUT] /api/category/  (Sondaki slash bu endpointe de önemli.)
    * Authorization token header olarak ayarlanmalı.
    * Request Body: { "id": 22, "title": "test_updated" }
    * Bu endpoint sistemde bulunan bir kategorinin güncellenmesini sağlar. Eğer sistemde verilen id ile oluşturulmuş bir category yoksa olumsuz yanıt döner.
<hr/>

### Eğer daha fazla zamanım olsaydı...

* Güvenlik konusunda JWT ve refresh tokenleri kullanıp daha kapsamlı bir güvenlik mekanizması kurardım.
* Kullanıcılar için kullanıcı grupları oluşturup bu gruplara özel izinler atardım. Kullanıcılar izinli olmadıkları endpointlerden işlem yapamazlardı.
* Kullanıcılardan aldığımız veriler için daha çok validation uygulardım.
* Endpointlerde daha ayrıntılı bilgi verirdim. Özellikle hata oluşması veya yanlış işlem yapılması sonucu gönderilecek bilgiyi daha ayrıntılı bir hale getirirdim.
* Geliştirmeye başlamadan önce yapacağım tasarıma göre endpointler için test caseler yazardım.
* Projeyi dockerize ederdim ve veri tabanı ile ilgili problemi ortadan kaldırırdım.
