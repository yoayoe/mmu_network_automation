# MMU Network Automation

Aplikasi web berbasis Django untuk menginventarisasi perangkat jaringan Mikrotik dan Cisco, menjalankan konfigurasi massal melalui SSH, serta mencatat hasilnya dalam bentuk log terpusat. Proyek ini dikembangkan untuk mendukung unit-unit di lingkungan UIW Maluku dan Maluku Utara.

## Fitur Utama
- **Dashboard ringkas** menampilkan jumlah perangkat per vendor dan 10 aktivitas terakhir.
- **Inventaris perangkat** lengkap dengan hierarki Unit Induk → Unit Pelaksana → Unit Layanan.
- **Penambahan perangkat** melalui formulir dengan validasi Django ModelForm.
- **Otomasi konfigurasi**: kirim perintah konfig ke banyak perangkat sekaligus, otomatis membedakan sintaks Mikrotik (perintah `exec_command`) dan Cisco (mode `conf t` via shell).
- **Verifikasi konfigurasi**: jalankan perintah cek, tampilkan output gabungan di halaman hasil.
- **Log aktivitas** tersimpan di tabel `Log`, mencatat target, aksi, status, waktu, serta pesan kesalahan bila ada.

## Tumpukan Teknologi
- **Backend**: Django 3.x, SQLite (`db.sqlite3`).
- **SSH Automation**: [Paramiko](https://www.paramiko.org/).
- **Frontend**: Template SB Admin 2 dengan Bootstrap, Font Awesome, dan aset statis lokal pada direktori `static/`.

## Struktur Data Penting
| Model | Deskripsi Singkat |
| --- | --- |
| `UnitInduk` | Daftar unit induk (contoh: `UIW MMU`, `UIP MALUKU`). |
| `UnitPelaksana` | Unit pelaksana yang mereferensikan `UnitInduk`. |
| `UnitLayanan` | Unit layanan yang mereferensikan `UnitInduk` dan `UnitPelaksana`. |
| `Device` | Perangkat beserta kredensial SSH, vendor (`mikrotik`/`cisco`), dan penempatan unit. |
| `Log` | Riwayat tindakan otomatisasi (konfigurasi dan verifikasi). |

> **Catatan:** Untuk memastikan referensi antar unit valid, pastikan data `UnitInduk`, `UnitPelaksana`, dan `UnitLayanan` dimasukkan terlebih dahulu melalui Django admin atau shell.

## Prasyarat
- Python 3.7 atau lebih baru.
- Pipenv, venv, atau alat manajemen virtual environment lain (opsional tapi direkomendasikan).
- Akses ke repositori GitHub proyek ini.
- Docker Desktop atau engine kompatibel (opsional, hanya bila ingin menggunakan kontainer).

## Instalasi Lokal (Tanpa Docker)
```bash
git clone <URL-repo-anda>
cd mmu_network_automation
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Tambahkan dependensi lain yang dibutuhkan oleh lingkungan Anda (mis. `python-dotenv` bila ingin menyembunyikan kredensial melalui env var).

## Menyiapkan Basis Data
Jalankan migrasi Django untuk membuat seluruh tabel:
```bash
python manage.py migrate
```

Buat akun admin untuk mengakses /admin dan login ke aplikasi:
```bash
python manage.py createsuperuser
```

Isi data referensi (`UnitInduk`, `UnitPelaksana`, `UnitLayanan`) dan perangkat (`Device`) via admin panel atau melalui shell:
```bash
python manage.py shell
```

## Menjalankan Tanpa Docker
```bash
python manage.py runserver
```

Aplikasi dapat diakses pada `http://127.0.0.1:8000/`. Semua halaman (kecuali login) memerlukan autentikasi; setelah login Anda akan dialihkan ke dashboard.

## Menjalankan Dengan Docker
1. Build image:
   ```bash
   docker build -t mmu-network-automation .
   ```
2. Jalankan migrasi (opsional `createsuperuser` menggunakan pola yang sama):
   ```bash
   docker run --rm -it mmu-network-automation python manage.py migrate
   docker run --rm -it mmu-network-automation python manage.py createsuperuser
   ```
3. Start aplikasi:
   ```bash
   docker run --rm -it -p 8000:8000 mmu-network-automation
   ```

Aplikasi tersedia di `http://127.0.0.1:8000/`. Gunakan `CTRL+C` untuk menghentikan kontainer saat menjalankan mode interaktif.

> **Catatan:** Basis data SQLite berada di dalam kontainer. Gunakan volume (`-v $(pwd)/db.sqlite3:/app/db.sqlite3`) jika ingin mempertahankan data antar container run.

## Alur Otomasi
1. **Tambah perangkat** di menu *Add Device*. Pastikan informasi vendor, IP, dan kredensial SSH benar.
2. **Konfigurasi massal** melalui menu *Add Configuration*:
   - Pilih satu atau beberapa perangkat.
   - Masukkan daftar perintah Mikrotik dan/atau Cisco (setiap baris dianggap satu perintah).
   - Sistem akan:
     - Membuka koneksi SSH menggunakan Paramiko.
     - Mengirim `conf t` dan setiap perintah untuk perangkat Cisco.
     - Menjalankan perintah satu per satu dengan `exec_command` untuk Mikrotik.
   - Hasil akan dicatat di model `Log` dengan status sukses atau error.
3. **Verifikasi konfigurasi** pada menu *Verify Configuration*:
   - Mekanismenya mirip dengan konfigurasi, tetapi output perintah dikumpulkan dan ditampilkan di halaman hasil (`verify_result.html`).
   - Semua percobaan verifikasi juga dicatat pada log.
4. **Pantau log** melalui menu *Log* yang menampilkan seluruh riwayat tindakan otomatisasi.

## Struktur Direktori
```
mmu_network_automation/
├─ manage.py
├─ mmu_network_automation/          # Konfigurasi proyek Django
├─ network_automation/              # Aplikasi utama (models, views, forms, urls)
├─ templates/                       # Template HTML (dashboard, devices, form konfigurasi, dsb.)
├─ static/                          # Asset SB Admin 2 (CSS, JS, gambar, vendor)
├─ requirements.txt                 # Daftar dependensi Python
├─ Dockerfile                       # Definisi image Docker
└─ db.sqlite3                       # Basis data default (SQLite)
```

## Otentikasi & Keamanan
- Login menggunakan mekanisme standar Django (`django.contrib.auth`).
- `LOGIN_URL` mengarah ke `login` (template tersedia pada `templates/registration/login.html`).
- Kredensial perangkat disimpan dalam basis data; untuk lingkungan produksi, pertimbangkan enkripsi dan pemisahan kredensial sensitif.
- Pastikan trafik web diamankan dengan HTTPS jika aplikasi diakses di jaringan luas.

## Pengujian
- Berkas `network_automation/tests.py` belum berisi pengujian otomatis. Tambahkan tes unit/functional sesuai kebutuhan sebelum menerapkan ke produksi.

## Pengembangan Lebih Lanjut
- Implementasi manajemen user dan peran (mis. operator vs admin).
- Penjadwalan tugas otomatis (menggunakan Celery atau Django-Q).
- Integrasi dengan repositori konfigurasi Git atau REST API perangkat.
- Penyimpanan rahasia (credentials) melalui layanan seperti HashiCorp Vault atau Django-Environ.

## Lisensi
Belum ditentukan. Tambahkan ketentuan lisensi sesuai kebijakan organisasi Anda.
