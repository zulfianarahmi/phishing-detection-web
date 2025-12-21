# -*- coding: utf-8 -*-
"""
Script untuk convert model TensorFlow/Keras ke TensorFlow.js format
Jalankan setelah train_and_export.py selesai
"""

import os
import subprocess
import sys

def convert_model_to_tfjs():
    """
    Convert model ke TensorFlow.js format menggunakan tensorflowjs_converter
    Support: H5 format (karena bug TF 2.20 + Python 3.12 dengan SavedModel)
    """
    # Path model yang akan dikonversi - cek H5 dulu (lebih reliable)
    model_h5_path = 'model.h5'
    model_savedmodel_path = 'model'  # SavedModel format (fallback)
    output_path = 'public/model'
    
    # Pastikan output directory ada
    os.makedirs(output_path, exist_ok=True)
    
    # Tentukan input format dan path
    if os.path.exists(model_h5_path):
        model_path = model_h5_path
        input_format = 'keras'
        print(f"Mengkonversi model dari H5 ({model_h5_path}) ke {output_path}...")
    elif os.path.exists(model_savedmodel_path):
        model_path = model_savedmodel_path
        input_format = 'tf_saved_model'
        print(f"Mengkonversi model dari SavedModel ({model_savedmodel_path}) ke {output_path}...")
    else:
        print("❌ Model tidak ditemukan!")
        print(f"Pastikan file {model_h5_path} atau {model_savedmodel_path} ada.")
        print("Jalankan train_and_export.py terlebih dahulu.")
        sys.exit(1)
    
    # Command untuk convert
    # Install dulu: pip install tensorflowjs
    import shutil
    converter_cmd = shutil.which('tensorflowjs_converter')
    
    if input_format == 'keras':
        # Convert dari H5/Keras
        if not converter_cmd:
            cmd = [
                sys.executable, '-m', 'tensorflowjs.converters.convert_keras',
                model_path,
                output_path
            ]
        else:
            cmd = [
                converter_cmd,
                '--input_format', 'keras',
                model_path,
                output_path
            ]
    else:
        # Convert dari SavedModel
        if not converter_cmd:
            cmd = [
                sys.executable, '-m', 'tensorflowjs.converters.convert_keras',
                '--input_format', 'tf_saved_model',
                '--output_format', 'tfjs_graph_model',
                model_path,
                output_path
            ]
        else:
            cmd = [
                converter_cmd,
                '--input_format', 'tf_saved_model',
                '--output_format', 'tfjs_graph_model',
                '--signature_name', 'serving_default',
                '--saved_model_tags', 'serve',
                model_path,
                output_path
            ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("[OK] Konversi berhasil!")
        print(f"Model TensorFlow.js tersimpan di: {os.path.abspath(output_path)}")
        print("\nFile yang dihasilkan:")
        for file in os.listdir(output_path):
            print(f"  - {file}")
    except subprocess.CalledProcessError as e:
        print("[ERROR] Error saat konversi:")
        print(e.stderr)
        print("\nPastikan tensorflowjs sudah terinstall:")
        print("  pip install tensorflowjs")
        sys.exit(1)

if __name__ == '__main__':
    convert_model_to_tfjs()

