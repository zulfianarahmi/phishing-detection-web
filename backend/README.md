# Backend API - Phishing Detection

Backend FastAPI untuk deteksi phishing menggunakan model H5.

## Setup Lokal

```bash
# Install dependencies
pip install -r requirements.txt

# Pastikan model.h5 ada di root project (satu level di atas backend/)
# Struktur:
#   project/
#     backend/
#       main.py
#     model.h5

# Run server
cd backend
python main.py

# Atau dengan uvicorn langsung
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API akan berjalan di `http://localhost:8000`

## Endpoints

### GET `/`
Health check endpoint

### POST `/predict`
Upload gambar untuk prediksi

**Request:**
- `file`: File gambar (multipart/form-data)

**Response:**
```json
{
  "label": "phishing",
  "phishing_prob": 0.87,
  "genuine_prob": 0.13
}
```

### POST `/api/collect`
Endpoint untuk data collection (opt-in)

## Deploy ke Render/Railway

### Render
1. Buat account di render.com
2. New → Web Service
3. Connect GitHub repo
4. Settings:
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3
5. Add Environment Variable jika perlu

### Railway
1. Buat account di railway.app
2. New Project → Deploy from GitHub
3. Select repo
4. Add Service → Python
5. Settings:
   - Root Directory: `backend`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy

## Catatan

- Pastikan `model.h5` ada di repo atau upload ke cloud storage
- Untuk production, update CORS origins di `main.py` dengan domain Vercel kamu
- Pertimbangkan rate limiting untuk production

