# Panduan Deploy Backend

## Deploy ke Render

### 1. Persiapan
- Pastikan `model.h5` ada di root project (satu level dengan `backend/`)
- Commit semua file ke GitHub

### 2. Setup di Render
1. Login ke [render.com](https://render.com)
2. Klik **New** → **Web Service**
3. Connect GitHub repository kamu
4. Configure:
   - **Name**: `phishing-detection-api` (atau nama lain)
   - **Region**: Pilih yang terdekat
   - **Branch**: `main` (atau branch kamu)
   - **Root Directory**: `backend` (atau kosongkan jika struktur berbeda)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type**: Free tier (atau upgrade jika perlu)

5. **Environment Variables** (opsional):
   - Tidak perlu untuk basic setup

6. Klik **Create Web Service**

### 3. Update Model Path
Jika struktur berbeda, edit `backend/main.py`:
```python
model_path = os.path.join(os.path.dirname(__file__), "..", "model.h5")
```

### 4. Setelah Deploy
- Copy URL backend (contoh: `https://phishing-api.onrender.com`)
- Update `.env.local` di frontend:
  ```
  NEXT_PUBLIC_API_URL=https://phishing-api.onrender.com
  ```

---

## Deploy ke Railway

### 1. Persiapan
- Pastikan `model.h5` ada di root project
- Commit semua file ke GitHub

### 2. Setup di Railway
1. Login ke [railway.app](https://railway.app)
2. Klik **New Project** → **Deploy from GitHub repo**
3. Select repository kamu
4. Railway akan auto-detect Python
5. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: 
     ```bash
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```
6. Klik **Deploy**

### 3. Setelah Deploy
- Railway akan generate URL otomatis
- Copy URL dan update `.env.local` di frontend

---

## Catatan Penting

### Model File
- `model.h5` harus ada di repo atau upload ke cloud storage
- Jika file besar (>100MB), pertimbangkan:
  - Git LFS
  - Cloud storage (S3, Cloudinary) dan load dari URL
  - Upload manual setelah deploy

### CORS
- Backend sudah dikonfigurasi untuk allow semua origin (`allow_origins=["*"]`)
- Untuk production, update di `backend/main.py`:
  ```python
  allow_origins=["https://your-vercel-app.vercel.app"]
  ```

### Environment Variables
- Di Render/Railway, tambahkan jika perlu:
  - `MODEL_PATH`: Path ke model (default: `../model.h5`)

### Monitoring
- Render: Dashboard → Logs
- Railway: Deployments → View Logs

### Troubleshooting
- **Model not found**: Pastikan `model.h5` ada di repo atau path benar
- **Port error**: Gunakan `$PORT` environment variable
- **Build failed**: Cek requirements.txt dan Python version

