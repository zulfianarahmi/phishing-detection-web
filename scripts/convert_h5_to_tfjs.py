# -*- coding: utf-8 -*-
"""
Convert model H5 langsung ke TensorFlow.js menggunakan Python API
Workaround untuk bug TF 2.20 + Python 3.12
"""

import os
import tensorflow as tf
import tensorflowjs as tfjs

def convert_h5_to_tfjs():
    model_h5_path = 'model.h5'
    output_path = 'public/model'
    
    if not os.path.exists(model_h5_path):
        print(f"[ERROR] Model H5 tidak ditemukan: {model_h5_path}")
        print("Jalankan train_and_export.py terlebih dahulu")
        return
    
    print(f"Loading model dari {model_h5_path}...")
    try:
        model = tf.keras.models.load_model(model_h5_path)
        print("[OK] Model berhasil di-load")
    except Exception as e:
        print(f"[ERROR] Gagal load model: {e}")
        return
    
    print(f"\nMengkonversi ke TensorFlow.js format...")
    print(f"Output: {output_path}")
    
    # Pastikan output directory ada
    os.makedirs(output_path, exist_ok=True)
    
    try:
        # Convert menggunakan tfjs API
        tfjs.converters.save_keras_model(model, output_path)
        print("[OK] Konversi berhasil!")
        print(f"Model TensorFlow.js tersimpan di: {os.path.abspath(output_path)}")
        print("\nFile yang dihasilkan:")
        for file in os.listdir(output_path):
            file_path = os.path.join(output_path, file)
            size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            print(f"  - {file} ({size:.2f} MB)")
    except Exception as e:
        print(f"[ERROR] Gagal konversi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    convert_h5_to_tfjs()






