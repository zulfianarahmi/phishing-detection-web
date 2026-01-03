# -*- coding: utf-8 -*-
"""
Script test untuk memverifikasi dataset bisa dibaca dengan benar
"""

import os
import tensorflow as tf

# Path dataset - gunakan folder dataset/ jika ada
script_dir = os.path.dirname(os.path.abspath(__file__))
dataset_folder = os.path.join(script_dir, 'dataset')

# Prioritas: gunakan folder dataset/ jika ada
if os.path.exists(os.path.join(dataset_folder, 'genuine_site_0')) and os.path.exists(os.path.join(dataset_folder, 'phishing_site_1')):
    dataset_dir = dataset_folder
else:
    dataset_dir = script_dir  # Fallback ke root

print("=" * 60)
print("TEST DATASET LOADING")
print("=" * 60)
print(f"Dataset directory: {dataset_dir}")
print()

# Cek folder yang ada
genuine_path = os.path.join(dataset_dir, 'genuine_site_0')
phishing_path = os.path.join(dataset_dir, 'phishing_site_1')

print("Folder check:")
print(f"  genuine_site_0: {os.path.exists(genuine_path)}")
if os.path.exists(genuine_path):
    genuine_files = [f for f in os.listdir(genuine_path) if f.endswith('.png')]
    print(f"    -> {len(genuine_files)} PNG files")

print(f"  phishing_site_1: {os.path.exists(phishing_path)}")
if os.path.exists(phishing_path):
    phishing_files = [f for f in os.listdir(phishing_path) if f.endswith('.png')]
    print(f"    -> {len(phishing_files)} PNG files")

print()
print("Loading dataset dengan TensorFlow...")
print()

try:
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(180, 180),
        batch_size=32
    )
    
    class_names = train_ds.class_names
    print(f"[OK] Dataset berhasil di-load!")
    print(f"Kelas yang terdeteksi: {class_names}")
    print(f"Jumlah kelas: {len(class_names)}")
    
    # Hitung jumlah sample
    num_samples = 0
    for _ in train_ds:
        num_samples += 1
    
    print(f"Jumlah batch training: {num_samples}")
    
    # Cek apakah hanya 2 kelas (genuine dan phishing)
    expected_classes = ['genuine_site_0', 'phishing_site_1']
    if set(class_names) == set(expected_classes):
        print("[OK] Kelas sesuai yang diharapkan!")
    else:
        print("[WARNING] Kelas yang terdeteksi berbeda dari yang diharapkan!")
        print(f"  Diharapkan: {expected_classes}")
        print(f"  Ditemukan: {class_names}")
        print("  Mungkin ada folder lain yang berisi gambar di root project")
    
except Exception as e:
    print(f"[ERROR] Gagal load dataset: {e}")
    import traceback
    traceback.print_exc()

