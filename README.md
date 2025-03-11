# Instagram Scraper dengan Waktu Posting dan Waktu Scraping

Script ini memungkinkan Anda untuk melakukan scraping post Instagram dari akun publik dan menyimpan hasilnya dalam format CSV atau Excel. Hasil scraping akan mencakup waktu posting asli dan waktu scraping.

## Fitur

- Scraping post Instagram dari akun publik
- Menyimpan waktu posting asli dan waktu scraping
- Menyimpan data dalam format CSV atau Excel
- Opsi untuk membatasi jumlah post yang di-scrape
- Menyimpan informasi penting seperti caption, jumlah likes, jumlah komentar, hashtag, dll.
- **Fitur login** untuk menghindari batasan rate limiting
- **Pengaturan delay** antara permintaan untuk menghindari pemblokiran

## Persyaratan

Pastikan Anda telah menginstal semua dependensi yang diperlukan:

```bash
pip install -r instagram_scraper_requirements.txt
```

## Cara Penggunaan

### 1. Instalasi

```bash
# Clone repository (jika ada) atau download file
# Kemudian install dependensi
pip install -r instagram_scraper_requirements.txt
```

### 2. Menjalankan Scraper dari Command Line

```bash
# Format dasar
python instagram_scraper.py USERNAME [--limit LIMIT] [--format {csv,excel}] [--login LOGIN_USERNAME] [--delay DELAY_SECONDS]

# Contoh: Scrape 10 post terakhir dari akun natgeo dan simpan dalam format CSV
python instagram_scraper.py natgeo --limit 10 --format csv

# Contoh: Scrape dengan login untuk menghindari batasan rate limiting
python instagram_scraper.py natgeo --login your_instagram_username --delay 3

# Contoh: Scrape semua post dari akun natgeo dan simpan dalam format Excel
python instagram_scraper.py natgeo --format excel
```

### 3. Menggunakan sebagai Modul dalam Script Python Lain

```python
from instagram_scraper import scrape_instagram_posts

# Scrape 20 post terakhir dari akun natgeo dan simpan dalam format CSV (default)
output_path = scrape_instagram_posts(username="natgeo", limit=20)

# Scrape dengan login untuk menghindari batasan rate limiting
output_path = scrape_instagram_posts(username="natgeo", limit=20, login_user="your_instagram_username", delay=3)

# Scrape 50 post terakhir dari akun natgeo dan simpan dalam format Excel
output_path = scrape_instagram_posts(username="natgeo", limit=50, output_format="excel")
```

## Mengatasi Error Rate Limiting

Jika Anda mendapatkan error "401 Unauthorized" atau pesan "Please wait a few minutes before you try again", ini berarti Instagram telah menerapkan rate limiting pada IP Anda. Berikut beberapa cara untuk mengatasinya:

1. **Gunakan fitur login**: Login dengan akun Instagram Anda untuk mendapatkan batas rate yang lebih tinggi
   ```bash
   python instagram_scraper.py USERNAME --login YOUR_INSTAGRAM_USERNAME
   ```

2. **Tambahkan delay lebih lama**: Tingkatkan waktu tunggu antara permintaan
   ```bash
   python instagram_scraper.py USERNAME --delay 5
   ```

3. **Tunggu beberapa menit**: Jika masih mendapatkan error, tunggu 10-15 menit sebelum mencoba lagi

4. **Gunakan VPN**: Mengubah IP Anda dapat membantu mengatasi pembatasan

## Catatan Penting

1. **Batasan Instagram**: Instagram memiliki batasan untuk scraping. Terlalu banyak permintaan dalam waktu singkat dapat menyebabkan IP Anda diblokir sementara.

2. **Akun Publik**: Script ini hanya berfungsi untuk akun Instagram publik. Akun privat tidak dapat di-scrape tanpa login.

3. **Login (Opsional)**: Untuk menghindari batasan rate limit, Anda dapat login dengan akun Instagram Anda menggunakan parameter `--login`.

4. **Penggunaan yang Bertanggung Jawab**: Gunakan script ini dengan bertanggung jawab dan hormati kebijakan penggunaan Instagram.

## Output

Data akan disimpan dalam folder `instagram_data` dengan format nama file:
`{username}_posts_{timestamp}.csv` atau `{username}_posts_{timestamp}.xlsx`

Kolom yang disimpan meliputi:
- post_id: ID unik post
- post_url: URL lengkap post
- caption: Teks caption post
- likes: Jumlah likes
- comments: Jumlah komentar
- posting_time: Waktu post dibuat (waktu lokal)
- scraping_time: Waktu scraping dilakukan
- is_video: Apakah post berupa video
- location: Lokasi post (jika ada)
- hashtags: Hashtag yang digunakan dalam caption 
