# -*- coding: utf-8 -*-
"""
Script untuk menyimpan model yang sudah di-train
Jalankan setelah train_and_export.py selesai (jika save gagal)
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

# Load model architecture dan weights dari checkpoint jika ada
# Atau kita perlu retrain dengan epochs=0 untuk load weights

# Alternatif: Load dari checkpoint terakhir jika ada
checkpoint_dir = 'checkpoints'
if os.path.exists(checkpoint_dir):
    print(f"Loading dari checkpoint: {checkpoint_dir}")
    # Load latest checkpoint
    model = keras.models.load_model(checkpoint_dir)
else:
    print("Checkpoint tidak ditemukan. Perlu retrain atau load dari file lain.")
    print("Solusi: Jalankan train_and_export.py lagi dengan fix yang sudah dibuat")
    exit(1)

# Simpan sebagai H5
model_h5_path = 'model.h5'
print(f"\nMenyimpan model sebagai H5 ke: {model_h5_path}...")
try:
    model.save(model_h5_path)
    print(f"[OK] Model H5 berhasil disimpan di: {os.path.abspath(model_h5_path)}")
except Exception as e:
    print(f"[ERROR] Gagal menyimpan H5: {e}")

# Simpan sebagai SavedModel
model_save_path = 'model'
print(f"\nMenyimpan model sebagai SavedModel ke: {model_save_path}...")
try:
    model.save(model_save_path, save_format='tf')
    print(f"[OK] Model SavedModel berhasil disimpan di: {os.path.abspath(model_save_path)}")
except Exception as e:
    print(f"[WARNING] Gagal menyimpan SavedModel: {e}")
    print("Menggunakan H5 format sebagai alternatif...")

