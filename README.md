# Web Phishing Detection

Aplikasi web untuk deteksi phishing dari screenshot menggunakan backend Python API.

## Architecture

- **Frontend**: Next.js (deploy di Vercel)
- **Backend**: FastAPI (deploy di Render/Railway)
- **Model**: TensorFlow/Keras (H5 format)

## Setup

### 1. Training Model (Python)

```bash
# Install dependencies
pip install tensorflow scikit-learn matplotlib numpy pillow

# Training model
python train_and_export.py
```

Model akan tersimpan sebagai `model.h5`.

### 2. Setup Backend (FastAPI)

```bash
cd backend
pip install -r requirements.txt

# Run backend (pastikan model.h5 ada di root project)
python main.py
```

Backend akan berjalan di `http://localhost:8000`

### 3. Setup Frontend (Next.js)

```bash
# Install dependencies
npm install

# Setup environment variable
cp .env.example .env.local
# Edit .env.local dan set NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

Buka [http://localhost:3000](http://localhost:3000)

### 4. Deploy

**Backend** (Render/Railway):
- Lihat `DEPLOY_BACKEND.md` untuk panduan lengkap

**Frontend** (Vercel):
```bash
# Install Vercel CLI (optional)
npm i -g vercel

# Deploy
vercel
```

Atau connect repo GitHub ke Vercel dashboard.
- **Penting**: Set environment variable `NEXT_PUBLIC_API_URL` dengan URL backend kamu

## Struktur Project

```
web-phising/
├── train_and_export.py      # Script training & export model
├── convert_to_tfjs.py       # Script convert ke TFJS
├── public/
│   └── model/               # Model TensorFlow.js (dihasilkan dari convert)
├── app/                     # Next.js app directory
│   ├── page.tsx            # Home page (upload & predict)
│   ├── about/page.tsx      # Model Card / About page
│   └── layout.tsx          # Root layout
└── components/             # React components
```

## Catatan

- Backend API harus di-deploy terlebih dahulu sebelum deploy frontend
- Pastikan `NEXT_PUBLIC_API_URL` di-set dengan benar di Vercel environment variables
- Model H5 harus ada di backend atau di cloud storage yang bisa diakses
- Untuk production, pertimbangkan rate limiting dan CORS yang lebih ketat

