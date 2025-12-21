# Cara Menjalankan Aplikasi

Panduan lengkap untuk menjalankan aplikasi deteksi phishing secara lokal.

## Prerequisites

Pastikan sudah terinstall:
- **Python 3.10+** (cek dengan `python --version`)
- **Node.js 18+** (cek dengan `node --version`)
- **npm** atau **yarn** (cek dengan `npm --version`)

## Langkah 1: Setup Backend (FastAPI)

### 1.1 Install Dependencies Python

```bash
cd backend
pip install -r requirements.txt
```

Atau jika menggunakan virtual environment (disarankan):

```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 1.2 Pastikan Model Ada

Pastikan file `model.h5` ada di root project (satu level di atas folder `backend/`).

```bash
# Dari root project
ls model.h5  # Linux/Mac
dir model.h5  # Windows
```

Jika belum ada, jalankan training terlebih dahulu:
```bash
python train_and_export.py
```

### 1.3 Jalankan Backend

Dari folder `backend/`:

```bash
python main.py
```

Atau menggunakan uvicorn langsung:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend akan berjalan di: **http://localhost:8000**

✅ **Cek apakah backend berjalan:**
- Buka browser: http://localhost:8000/docs (Swagger UI)
- Atau: http://localhost:8000 (akan muncul JSON response)

---

## Langkah 2: Setup Frontend (Next.js)

### 2.1 Install Dependencies Node.js

Dari **root project** (bukan folder backend):

```bash
npm install
```

### 2.2 Setup Environment Variable (Opsional)

Buat file `.env.local` di root project jika ingin mengubah URL backend:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Jika tidak dibuat, default akan menggunakan `http://localhost:8000`.

### 2.3 Jalankan Frontend

Dari **root project**:

```bash
npm run dev
```

Frontend akan berjalan di: **http://localhost:3000**

✅ **Cek apakah frontend berjalan:**
- Buka browser: http://localhost:3000
- Halaman utama aplikasi akan muncul

---

## Langkah 3: Testing

### 3.1 Test Backend API Langsung

```bash
# Test endpoint health
curl http://localhost:8000/

# Test prediction (dengan file gambar)
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.png"
```

Atau gunakan Swagger UI di http://localhost:8000/docs untuk test interaktif.

### 3.2 Test Frontend

1. Buka http://localhost:3000 di browser
2. Upload gambar screenshot website
3. Klik "Analisis Gambar"
4. Lihat hasil prediksi dan penjelasan

---

## Troubleshooting

### Backend tidak bisa start

**Error: `ModuleNotFoundError: No module named 'tensorflow'`**
```bash
cd backend
pip install -r requirements.txt
```

**Error: `FileNotFoundError: Model tidak ditemukan`**
- Pastikan `model.h5` ada di root project (satu level di atas `backend/`)
- Atau jalankan `python train_and_export.py` untuk generate model

**Error: Port 8000 sudah digunakan**
- Ganti port di `backend/main.py` atau tutup aplikasi lain yang menggunakan port 8000

### Frontend tidak bisa start

**Error: `Port 3000 already in use`**
```bash
# Gunakan port lain
npm run dev -- -p 3001
```

**Error: `Cannot connect to backend`**
- Pastikan backend sudah running di http://localhost:8000
- Cek file `.env.local` jika ada, pastikan `NEXT_PUBLIC_API_URL` benar

**Error: `Module not found`**
```bash
# Hapus node_modules dan install ulang
rm -rf node_modules package-lock.json
npm install
```

### CORS Error

Jika muncul error CORS di browser console:
- Pastikan backend `ALLOWED_ORIGINS` di `backend/config.py` sudah include `http://localhost:3000`
- Restart backend setelah mengubah config

---

## Quick Start (Semua Langkah Sekaligus)

```bash
# Terminal 1: Backend
cd backend
pip install -r requirements.txt
python main.py

# Terminal 2: Frontend (buka terminal baru)
cd ..  # kembali ke root
npm install
npm run dev
```

Kemudian buka browser: **http://localhost:3000**

---

## Production Build

### Frontend Production Build

```bash
npm run build
npm start  # atau deploy ke Vercel
```

### Backend Production

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Atau deploy ke Render/Railway sesuai dokumentasi di `DEPLOY_BACKEND.md`.

