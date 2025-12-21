"""
Configuration file untuk backend
Bisa di-override dengan environment variables
"""

import os
from typing import List

# Server config
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

# CORS config
ALLOWED_ORIGINS: List[str] = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:3001"
).split(",")

# Model config
MODEL_PATH = os.getenv("MODEL_PATH", "../model.h5")
IMG_HEIGHT = int(os.getenv("IMG_HEIGHT", "180"))
IMG_WIDTH = int(os.getenv("IMG_WIDTH", "180"))

# File upload config
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))  # 10MB
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg", "image/webp"]

# Rate limiting (untuk implementasi nanti)
RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

