# Panduan Deploy ke Vercel

## Persiapan Sebelum Deploy

1. **Pastikan model sudah dikonversi ke TFJS**
   ```bash
   python convert_to_tfjs.py
   ```
   File harus ada di `public/model/model.json` dan `public/model/model.weights.bin`

2. **Test lokal dulu**
   ```bash
   npm run build
   npm start
   ```
   Pastikan tidak ada error dan model bisa di-load.

## Deploy ke Vercel

### Opsi 1: Via Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel

# Untuk production
vercel --prod
```

### Opsi 2: Via GitHub Integration

1. Push code ke GitHub
2. Login ke [vercel.com](https://vercel.com)
3. Klik "Add New Project"
4. Import repository kamu
5. Vercel akan auto-detect Next.js
6. Klik "Deploy"

## Konfigurasi Vercel

File `vercel.json` sudah dikonfigurasi untuk:
- Timeout API route `/api/collect` (10 detik)

### Environment Variables (Opsional)

Jika kamu perlu environment variables:
1. Di Vercel dashboard → Project Settings → Environment Variables
2. Tambahkan variabel yang diperlukan

## Catatan Penting

### Ukuran Model
- Model TensorFlow.js bisa besar (>50MB)
- Vercel free tier limit: 100MB per deployment
- Jika model terlalu besar:
  - Gunakan Git LFS untuk file besar
  - Atau upload model ke CDN (Cloudflare R2, AWS S3, dll) dan load dari URL
  - Atau gunakan Vercel Blob Storage

### Optimasi
- Model akan di-load saat pertama kali user buka app
- Pertimbangkan lazy-loading atau code splitting
- Gunakan compression (gzip/brotli) - Vercel otomatis handle ini

### Troubleshooting

**Error: Model tidak ditemukan**
- Pastikan `public/model/` sudah commit ke repo
- Cek path di `components/Predictor.tsx` (harus `/model/model.json`)

**Error: Build failed**
- Cek log di Vercel dashboard
- Pastikan semua dependencies di `package.json` valid
- Pastikan Node.js version compatible (Vercel auto-detect)

**Error: Function timeout**
- Cek `vercel.json` untuk timeout settings
- Untuk API routes, max 10 detik di free tier

## Post-Deploy

1. Test aplikasi di production URL
2. Cek console browser untuk error
3. Test upload gambar dan prediksi
4. Monitor di Vercel dashboard untuk error/analytics






