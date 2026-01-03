# Panduan Setup Lengkap

## Langkah 1: Training Model (Python)

### Prerequisites
```bash
pip install tensorflow tensorflowjs scikit-learn matplotlib numpy pillow
```

### Training
1. Edit `train_and_export.py`:
   - Ganti `dataset_dir` dengan path dataset kamu
   - Sesuaikan `epochs` jika perlu

2. Jalankan training:
```bash
python train_and_export.py
```

Ini akan menghasilkan:
- `model/` (SavedModel format)
- `model.h5` (backup)
- `training_history.png` (grafik training)

### Convert ke TensorFlow.js
```bash
pip install tensorflowjs
python convert_to_tfjs.py
```

Ini akan menghasilkan file di `public/model/`:
- `model.json`
- `model.weights.bin` (atau beberapa shard files)

**Penting:** Pastikan folder `public/model/` berisi file model sebelum deploy!

## Langkah 2: Setup Web App (Next.js)

### Install Dependencies
```bash
npm install
```

### Development
```bash
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000)

### Build untuk Production
```bash
npm run build
npm start
```

## Langkah 3: Deploy ke Vercel

### Opsi 1: Via Vercel CLI
```bash
npm i -g vercel
vercel
```

### Opsi 2: Via GitHub
1. Push code ke GitHub
2. Connect repo ke Vercel dashboard
3. Deploy otomatis

### Catatan Penting untuk Vercel:
- Pastikan `public/model/` sudah commit ke repo (atau gunakan Vercel Blob Storage untuk file besar)
- Model file bisa besar (>50MB), pertimbangkan:
  - Git LFS untuk file besar
  - Atau upload model ke CDN dan load dari URL external
  - Atau gunakan Vercel Blob Storage

## Struktur File yang Dihasilkan

```
web-phising/
├── model/                    # Model SavedModel (dari training)
├── model.h5                  # Backup model
├── public/
│   └── model/               # Model TFJS (untuk web)
│       ├── model.json
│       └── model.weights.bin
├── app/                     # Next.js app
├── components/              # React components
└── ...
```

## Troubleshooting

### Model tidak load di browser
- Pastikan `public/model/model.json` ada
- Cek console browser untuk error
- Pastikan path di `Predictor.tsx` benar: `/model/model.json`

### Error "Failed to load model"
- Pastikan semua file model (json + weights) ada di `public/model/`
- Cek CORS jika load dari external URL
- Pastikan ukuran file tidak melebihi limit Vercel

### Preprocessing error
- Pastikan gambar format valid (PNG, JPG, dll)
- Cek ukuran file (max 10MB di code, bisa disesuaikan)

## Next Steps (Opsional)

1. **Data Collection Endpoint**: Implementasi penyimpanan data di `/app/api/collect/route.ts`
   - Bisa pakai Vercel Blob Storage
   - Atau external service (S3, Cloudinary, dll)

2. **Dataset Publik**: Upload dataset ke GitHub/Kaggle dan update link di `app/about/page.tsx`

3. **Metrik Model**: Setelah training, update metrik di halaman About

4. **Optimasi Model**: 
   - Quantization untuk reduce size
   - Model pruning
   - Lazy loading untuk improve initial load






