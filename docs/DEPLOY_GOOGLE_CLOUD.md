# 🌥️ Deploy ke Google Cloud

## Overview

Project ini di-deploy menggunakan:
- **Backend (FastAPI):** Google Cloud Run
- **Frontend (Next.js):** Firebase Hosting atau Cloud Run

---

## 📋 Prerequisites

1. **Google Cloud Account** dengan billing enabled
   - Daftar: https://cloud.google.com/free
   - Free tier: $300 credit + always free tier

2. **gcloud CLI installed**
   - Download: https://cloud.google.com/sdk/docs/install
   - Verify: `gcloud --version`

---

## 🚀 Deployment Steps

### Step 1: Setup Google Cloud Project

```bash
# Login ke Google Cloud
gcloud auth login

# Buat project baru
gcloud projects create phishing-detection-web --name="Phishing Detection"

# Set project aktif
gcloud config set project phishing-detection-web

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 2: Deploy Backend ke Cloud Run

```bash
# Masuk ke folder backend
cd backend

# Deploy (Cloud Run akan auto-build dari Dockerfile)
gcloud run deploy phishing-api \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300s \
  --max-instances 10

# Output akan kasih URL, contoh:
# https://phishing-api-xxx-as.a.run.app
```

**Copy URL backend ini!** Akan dipakai di frontend.

### Step 3: Deploy Frontend

#### Option A: Firebase Hosting (Recommended)

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Init Firebase di project
firebase init hosting

# Pilih:
# - Create new project atau use existing
# - Public directory: out
# - Single-page app: Yes
# - GitHub integration: No (optional)

# Build Next.js untuk static export
npm run build

# Deploy
firebase deploy --only hosting
```

#### Option B: Cloud Run (Next.js SSR)

```bash
# Di root project
gcloud run deploy phishing-web \
  --source . \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated \
  --set-env-vars NEXT_PUBLIC_API_URL=https://phishing-api-xxx-as.a.run.app
```

### Step 4: Set Environment Variables

Jika deploy frontend di Cloud Run, set environment variable:

```bash
gcloud run services update phishing-web \
  --set-env-vars NEXT_PUBLIC_API_URL=https://phishing-api-xxx-as.a.run.app \
  --region asia-southeast1
```

---

## 💰 Pricing (Free Tier)

### Cloud Run Free Tier (Per Month):
- ✅ 2 million requests
- ✅ 360,000 GB-seconds compute time
- ✅ 180,000 vCPU-seconds
- ✅ 1 GB network egress to North America

### Firebase Hosting Free Tier:
- ✅ 10 GB storage
- ✅ 360 MB/day transfer
- ✅ Unlimited custom domains

**App kamu masih dalam free tier kalau traffic nya wajar!**

---

## 🔧 Configuration Files

### backend/Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY ../model.h5 ./model.h5
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### .gcloudignore (create this)
```
.git
.gitignore
node_modules/
__pycache__/
*.pyc
.env
.env.local
README.md
docs/
test/
dataset/
scripts/
```

---

## 🎯 Custom Domain (Optional)

### Backend:
```bash
gcloud run services update phishing-api \
  --add-custom-domain api.yourdomain.com \
  --region asia-southeast1
```

### Frontend (Firebase):
```bash
firebase hosting:channel:create live
firebase hosting:custom-domain add yourdomain.com
```

---

## 📊 Monitoring

### View Logs:
```bash
# Backend logs
gcloud run services logs read phishing-api --region asia-southeast1

# Follow logs real-time
gcloud run services logs tail phishing-api --region asia-southeast1
```

### Cloud Console:
- Dashboard: https://console.cloud.google.com
- Cloud Run: https://console.cloud.google.com/run
- Monitoring: https://console.cloud.google.com/monitoring

---

## 🐛 Troubleshooting

### Error: "Billing must be enabled"
1. Go to: https://console.cloud.google.com/billing
2. Link a billing account (credit card required, tapi tetap free tier)

### Error: "Permission denied"
```bash
# Set permissions
gcloud projects add-iam-policy-binding phishing-detection-web \
  --member="user:your-email@gmail.com" \
  --role="roles/run.admin"
```

### Cold Start Lambat
Cloud Run akan "sleep" kalau tidak ada traffic. Solusi:
- Set minimum instances: `--min-instances 1` (tapi kena charge)
- Atau biarkan aja, cold start ~10 detik wajar

### Model File Terlalu Besar
Jika model.h5 > 100MB, upload ke Cloud Storage:
```bash
gsutil cp model.h5 gs://your-bucket/model.h5
```

Update backend untuk download dari Cloud Storage.

---

## 🔄 CI/CD dengan GitHub Actions

Auto-deploy setiap push ke main branch.

### Setup:
1. Create service account:
```bash
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions"

gcloud projects add-iam-policy-binding phishing-detection-web \
  --member="serviceAccount:github-actions@phishing-detection-web.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

2. Download key dan simpan di GitHub Secrets

File `.github/workflows/deploy.yml` sudah disediakan di repo.

---

## ✅ Checklist

- [ ] gcloud CLI installed
- [ ] Google Cloud project created
- [ ] Billing enabled (for free tier)
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to Firebase/Cloud Run
- [ ] Environment variables set
- [ ] Custom domain (optional)
- [ ] CI/CD setup (optional)

---

## 🆘 Need Help?

- Google Cloud Docs: https://cloud.google.com/run/docs
- Firebase Docs: https://firebase.google.com/docs/hosting
- Community: https://stackoverflow.com/questions/tagged/google-cloud-run

---

Selamat deploy! ☁️

