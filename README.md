# Trading Tenang

Website pribadi tentang perjalanan crypto sejak 2017, untuk [tradingtenang.fun](https://tradingtenang.fun).

## Isi repo

- `deploy/`: website siap tayang. `index.html` sudah berisi font, foto, dan favicon, jadi tidak perlu build di server. Vercel menyajikan folder ini (lihat `vercel.json`).
- `src/index.src.html`: sumber halaman. Edit teks di sini.
- `build.mjs`: menanam font dan foto ke halaman, lalu menulis `site/index.html` untuk localhost.
- `assets/web/`: foto versi web. Sumber dan lisensinya ada di `assets/credits.json` dan di footer website.
- `logo/final/`: logo dan favicon final (SVG, PNG, ICO).
- `logo/`: skrip pembuat logo dan arah logo yang sempat dijajaki.

## Mengubah isi website

1. Edit `src/index.src.html`.
2. Jalankan build (butuh font Switzer di folder `fonts/`, lihat di bawah):

   ```bash
   node build.mjs
   ```

3. Salin hasilnya ke folder deploy, lalu commit dan push:

   ```bash
   cp site/index.html deploy/index.html
   ```

## Font

Font Switzer dari [Fontshare](https://www.fontshare.com/fonts/switzer) tidak ikut di repo karena lisensinya tidak mengizinkan file font disebar ulang. Untuk build, unduh Switzer (400, 500, 600, 700) dalam format woff2 ke `fonts/` dengan nama `switzer-1.woff2` sampai `switzer-4.woff2`.

## Catatan

Bukan nasihat keuangan. Semua angka adalah pengalaman pribadi.
