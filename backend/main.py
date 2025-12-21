"""
Backend FastAPI untuk deteksi phishing
Load model H5 dan serve prediction endpoint
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import logging
from typing import Optional
from explainability import generate_explanation
from config import (
    ALLOWED_ORIGINS, IMG_HEIGHT, IMG_WIDTH, 
    MAX_FILE_SIZE, ALLOWED_IMAGE_TYPES
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Phishing Detection API")

# CORS middleware untuk allow frontend Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ✅ Fixed: tidak lagi wildcard
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load model saat startup
model = None

@app.on_event("startup")
async def load_model():
    """Load model saat aplikasi start"""
    global model
    # Model path: satu level di atas backend/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "..", "model.h5")
    model_path = os.path.normpath(model_path)  # Normalize path
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model tidak ditemukan di: {model_path}")
    
    logger.info(f"Loading model dari {model_path}...")
    try:
        model = tf.keras.models.load_model(model_path)
        logger.info("[OK] Model berhasil di-load")
    except Exception as e:
        logger.error(f"[ERROR] Gagal load model: {e}", exc_info=True)
        raise

def preprocess_image(image_bytes: bytes) -> np.ndarray:
    """Preprocess gambar untuk model"""
    # Load image dari bytes
    img = Image.open(io.BytesIO(image_bytes))
    
    # Convert ke RGB jika perlu
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Resize ke 180x180
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    
    # Convert ke numpy array dan normalize
    img_array = np.array(img).astype('float32')
    
    # Expand dims untuk batch: (1, 180, 180, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Phishing Detection API",
        "model_loaded": model is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Endpoint untuk prediksi phishing dari gambar
    
    Args:
        file: File gambar yang diupload
        
    Returns:
        JSON dengan hasil prediksi:
        {
            "label": "phishing" | "genuine",
            "phishing_prob": float (0-1),
            "genuine_prob": float (0-1)
        }
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model belum di-load")
    
    # Validasi file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        logger.warning(f"Invalid file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"File harus berupa gambar. Format yang didukung: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )
    
    # Baca file
    try:
        image_bytes = await file.read()
        
        # Validasi ukuran
        if len(image_bytes) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Ukuran file maksimal {MAX_FILE_SIZE / (1024*1024):.0f}MB"
            )
        
        # Preprocess
        img_array = preprocess_image(image_bytes)
        
        # Predict
        prediction = model.predict(img_array, verbose=0)
        
        # Convert logit ke probability dengan sigmoid
        logit = prediction[0][0]
        phishing_prob = 1 / (1 + np.exp(-logit))
        genuine_prob = 1 - phishing_prob
        
        # Determine label
        label = "phishing" if phishing_prob >= 0.5 else "genuine"
        
        # Generate explanation
        explanation = generate_explanation(label, phishing_prob, genuine_prob)
        
        return {
            "label": label,
            "phishing_prob": float(phishing_prob),
            "genuine_prob": float(genuine_prob),
            "confidence_level": explanation["confidence_level"],
            "main_reason": explanation["main_reason"],
            "details": explanation["details"],
            "recommendation": explanation["recommendation"]
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (sudah proper)
        raise
    except Exception as e:
        # Log full error untuk debugging (tidak expose ke user)
        logger.error(f"Prediction error: {e}", exc_info=True)
        
        # Return generic error message untuk user
        raise HTTPException(
            status_code=500,
            detail="Terjadi error saat memproses gambar. Silakan coba lagi atau hubungi support jika masalah berlanjut."
        )

@app.post("/api/collect")
async def collect_data(
    file: UploadFile = File(...),
    label: Optional[str] = None,
    probability: Optional[str] = None
):
    """
    Endpoint untuk mengumpulkan data (opt-in dari user)
    Untuk tujuan riset dan peningkatan model
    """
    # TODO: Implementasi penyimpanan data
    # Bisa simpan ke database, cloud storage, dll
    
    return {
        "success": True,
        "message": "Data collected successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

