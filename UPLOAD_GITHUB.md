# 🚀 Cara Upload ke GitHub

## Step 1: Buat Repository Baru di GitHub

1. Buka https://github.com/new
2. Isi form:
   - **Repository name**: `phishing-detection-web` (atau nama sesukamu)
   - **Description**: `AI-powered phishing detection using screenshot analysis`
   - **Public** atau **Private** (terserah kamu)
   - ❌ **JANGAN** centang "Add a README file"
   - ❌ **JANGAN** centang ".gitignore" 
   - ❌ **JANGAN** pilih license (udah ada di code)
3. Klik **Create repository**

## Step 2: Copy URL Repository

Setelah repo dibuat, kamu akan lihat halaman dengan command. Copy URL nya, contoh:
```
https://github.com/username/phishing-detection-web.git
```

## Step 3: Upload dari Terminal

Buka terminal di folder project ini, jalankan command berikut:

### A. Add semua file ke git
```bash
git add .
```

### B. Commit dengan message
```bash
git commit -m "Initial commit: Phishing detection web app with playful design"
```

### C. Tambahkan remote (ganti URL dengan punya kamu!)
```bash
git remote add origin https://github.com/username/phishing-detection-web.git
```

### D. Push ke GitHub
```bash
git branch -M main
git push -u origin main
```

## Step 4: Cek di GitHub

Buka browser dan cek repo kamu di GitHub. Semua file harusnya sudah ada!

---

## 📝 Notes:

### File yang AKAN di-upload:
- ✅ Semua source code (app/, components/, dll)
- ✅ package.json & dependencies config
- ✅ README.md & dokumentasi
- ✅ Backend code (Python FastAPI)

### File yang TIDAK akan di-upload (sudah di .gitignore):
- ❌ node_modules/ (terlalu besar)
- ❌ .next/ (build files)
- ❌ __pycache__/ (Python cache)
- ❌ .env.local (environment variables)

### Dataset & Model:
- **model.h5** (76 MB) akan di-upload ke GitHub (masih bisa)
- Kalau repo kamu jadi terlalu besar, bisa upload model ke:
  - Google Drive
  - Hugging Face
  - GitHub Releases

---

## 🎯 One-Liner Command (Copy-Paste Aja!)

Setelah buat repo di GitHub dan dapat URL nya, jalankan ini:

```bash
git add . && git commit -m "Initial commit: Phishing detection web app" && git remote add origin https://github.com/USERNAME/REPO-NAME.git && git branch -M main && git push -u origin main
```

**Jangan lupa ganti `USERNAME` dan `REPO-NAME` dengan punya kamu!**

---

## ❓ Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/username/repo.git
```

### Error: Authentication failed
Kalau diminta username/password tapi error:
1. Buat Personal Access Token di GitHub Settings → Developer Settings
2. Atau gunakan GitHub Desktop (lebih gampang!)

---

## 🔗 Setelah Upload

Repository structure yang akan terlihat di GitHub:
```
phishing-detection-web/
├── app/                    # Next.js pages
├── components/             # React components
├── backend/               # FastAPI backend
├── dataset/               # Training dataset
├── public/                # Static assets
├── model.h5              # Trained model
├── package.json          # Dependencies
├── README.md             # Documentation
├── RUNNING.md            # How to run
└── ... (other files)
```

Sukses! 🎉

