## jual-bola-DLL

Tautan menuju aplikasi PWS yang sudah di-deploy: 
https://gibran-tegar-jualboladll.pbp.cs.ui.ac.id/

# Step-by-step cara mengimplementasikan checklist:
1. Membuat sebuah repositori lokal dengan nama jual-bola-DLL, membuat dokumen requirements.txt untuk menginstall dependencies dari project ini.
2. Menyalakan virtual environment dengan command dibawah untuk membuat virtual environment
python -m venv env
Dan menyalakan virtual environment dengan command dibawah
env\Scripts\activate
3. Menginstall seluruh library pada requirements di dalam virtual environment.
4. Membuat sebuah project Django baru pada repository lokal baru yang sudah dibuat dengan nama jual-bola-DLL.
django-admin startproject jual_bola_DLL .
5. membuat dua file .env yaitu untuk dev di lokal yaitu .env dan untuk deployment .env.prod yang diisi kredensial DB.
6. mengubah konfigurasi-konfigurasi pada settings.py
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "gibran-tegar-jualboladll.pbp.cs.ui.ac.id"]

menambahkan
import os
from dotenv import load_dotenv
load_dotenv()
untuk loading kredensial yang ada di env

mengubah konfigurasi database menjadi dibawah agar dapat fleksibel jika dalam lokal menggunakan sqllite3 dan kalau dideploy di PWS menggunakan postgreSQL:
if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
            'OPTIONS': {
                'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
            }
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

7. Membuat aplikasi 'main'
python manage.py startapp main
dan menambahkan 'main' pada INSTALLED_APPS di settings.py

8. mengubah models.py menjadi berikut sesuai keterangan tugas
class Product(models.Model):
    name = models.CharField()
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField()
    is_featured = models.BooleanField(default = False)

9. melakukan migrasi model agar django membuat necessary SQL commands untuk mengubah database
python manage.py makemigrations
untuk membuat file migrasi yang berisi changes yang baru
python manage.py migrate
mengubah database sesuai dengan yang ada di file migrasi.

10. mengubah file views.py yang ada di app main menjadi:
def show_main(request):
    context = {
        'nama_toko' : 'Jual Bola DLL',
        'nama_pembuat' : 'Gibran Tegar Ramadhan Putra Lynardi',
        'kelas_pbp' : 'PBP D'
    }

    return render(request, "main.html", context)

11. Melakukan Routing dari client request ke urls.py di level project untuk ditujukan pada
path('', include('main.urls')), lalu masuk ke urls.py di level app main dan menemukan pola path('', show_main, name='show_main'), agar masuk ke views.py fungsi show_main.

12. Membuat repo github dengan nama yang sama. Menambahkan .gitignore Melakukan git add, commit, dan push pada repo remote. Dengan branch main dan master.

13. Deploy ke PWS dan menjalankan command yang tertera pada laman PWS.


# Bagan request client dan responsenya
![Bagan alur django](bagan_alur.svg)

Pengguna meminta halaman, urls.py bertindak seperti peta yang mengarahkan permintaan ke fungsi yang benar di views.py. Views.py akan menggunakan models.py untuk mengambil data dari database. Setelah data didapat, view memasukkannya ke dalam sebuah templat HTML untuk membuat halaman web final yang dikirim kembali ke pengguna.

# Peran settings.py di Django
Pada tugas_individu ini so far, settings.py sudah berguna untuk mengubah konfigurasi database sesuai penggunaan entah dalam production atau tidak. Kita juga mendaftarkan aplikasi pada INSTALLED_APPS agar aplikasi tersebut dikenali oleh django. Ada juga ALLOWED_HOSTS untuk menentukan domain yang boleh menjalankan app ini.
Terdapat juga fungsi-fungsi lain yaitu konfigurasi middleware dan template. Jadi kegunaan settings.py adalah untuk menentukan konfigurasi-konfigurasi utama agar saling terhubung.

# Cara kerja migrasi database di Django
Dari tugas_individu ini, singkatnya kita akan melakukan perubahan pada models.py dulu di mana ini adalah representasi struktur database yang terlihat. Lalu kita menjalankan python manage.py makemigrations untuk membuat file migrasi apa saja yang harus diubah. Setelah itu menjalankan python manage.py migrate untuk benar-benar mengaplikasikan perubahan tersebut ke database ini dengan translating file migrasi itu menjadi perintah-perintah SQL yang diperlukan.

# Alasan Django digunakan sebagai permulaan
Menurut saya, Django digunakan karena menggunakan bahasa python yang memang tergolong lebih mudah untuk digunakan dibandingkan bahasa-bahasa lain. Struktur project nya juga benar-benar terdefine dari awal dan memang harus diikuti agar tidak berantakan. 

# Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?
Tidak ada, sudah sangat komprehensif sehingga jika belajar dari tutorial 1 sudah dapat mengaplikasikannya sendiri. Terima kasih banyakk kakak kakak asdoss! Mungkin jika memungkinkan beberapa tambahan troubleshooting disediakan juga jika memungkinkan.