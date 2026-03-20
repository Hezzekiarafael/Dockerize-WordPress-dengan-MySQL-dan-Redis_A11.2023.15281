# Dockerize WordPress dengan MySQL dan Redis

## Deskripsi
Project ini merupakan implementasi WordPress menggunakan Docker Compose dengan MySQL sebagai database dan Redis sebagai object cache.

---

# Cara Menjalankan

1. Pastikan Docker Desktop sudah berjalan

2. Jalankan perintah berikut di terminal:

`bash
docker-compose up -d

3. Buka browser dan akses: http://localhost:8000

4. Lakukan instalasi WordPress melalui halaman web

# Screenshoots
1. WordPress Installation Page
![WordPress Installation](screenshots/1_wordpress_installation.png)

2. Dashboard
![Dashboard](screenshots/2_wordpress_dashboard.png)

# Testing & Verification

WordPress dapat diakses melalui http://localhost:8000

Berhasil membuat post sebagai bukti koneksi ke MySQL

Redis berjalan dengan baik (PING → PONG)

Redis berhasil terhubung (status: Connected)

Data tetap ada setelah container di-restart (volume berhasil)


# Jawaban Pertanyaan
1. Kenapa perlu volume untuk MySQL?

Volume digunakan agar data database tidak hilang ketika container dihentikan atau dihapus, sehingga data tetap persisten.

2. Apa fungsi depends_on?

depends_on digunakan untuk mengatur urutan startup container, sehingga WordPress akan berjalan setelah MySQL siap digunakan.

3. Bagaimana cara WordPress container connect ke MySQL?

WordPress menggunakan konfigurasi WORDPRESS_DB_HOST=mysql, dimana mysql adalah nama service di Docker Compose yang berfungsi sebagai hostname dalam network Docker.

4. Apa keuntungan pakai Redis untuk WordPress?

Redis digunakan sebagai cache untuk mempercepat performa website, mengurangi beban database, dan meningkatkan kecepatan akses halaman.
