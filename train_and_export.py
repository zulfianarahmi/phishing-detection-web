# -*- coding: utf-8 -*-
"""
Script untuk training dan export model deteksi phishing
Urutan: Load Data → Build Model → Train → Evaluate → Export
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.utils.class_weight import compute_class_weight

# =================================================================
# 1. PERSIAPAN DATA (LOAD & PREPROCESS)
# =================================================================
# Path dataset - folder yang berisi subfolder genuine_site_0 dan phishing_site_1
# Struktur yang diharapkan:
#   dataset_dir/
#     genuine_site_0/  (folder dengan gambar genuine)
#     phishing_site_1/ (folder dengan gambar phishing)

# Cek apakah folder dataset ada
script_dir = os.path.dirname(os.path.abspath(__file__))

# Prioritas: cek folder dataset/ terlebih dahulu (lebih aman)
dataset_folder = os.path.join(script_dir, 'dataset')
genuine_in_dataset = os.path.join(dataset_folder, 'genuine_site_0')
phishing_in_dataset = os.path.join(dataset_folder, 'phishing_site_1')

# Cek apakah folder dataset/ sudah ada dan berisi folder yang diperlukan
if os.path.exists(genuine_in_dataset) and os.path.exists(phishing_in_dataset):
    dataset_dir = dataset_folder
    print(f"[OK] Dataset ditemukan di: {dataset_dir}")
    print(f"   - Genuine: {genuine_in_dataset}")
    print(f"   - Phishing: {phishing_in_dataset}")
elif os.path.exists(os.path.join(script_dir, 'genuine_site_0')) and os.path.exists(os.path.join(script_dir, 'phishing_site_1')):
    # Jika folder ada di root, gunakan root (TAPI ini akan membaca semua folder!)
    dataset_dir = script_dir
    print(f"[WARNING] Dataset ditemukan di root: {dataset_dir}")
    print(f"   [ERROR] Ini akan membaca SEMUA folder di root sebagai kelas!")
    print(f"   [SOLUSI] Pindahkan dataset ke folder 'dataset/' dengan menjalankan:")
    print(f"            python prepare_dataset.py")
    print(f"   Atau buat folder dataset/ secara manual dan copy folder genuine_site_0 dan phishing_site_1 ke sana")
    raise ValueError("Dataset tidak boleh di root project karena akan membaca semua folder. Pindahkan ke folder 'dataset/'")
else:
    # Fallback ke path default (untuk Colab atau struktur lain)
    dataset_dir = '/content/phishing-dataset'
    print(f"[WARNING] Folder dataset tidak ditemukan. Menggunakan: {dataset_dir}")
    print("   Pastikan folder 'genuine_site_0' dan 'phishing_site_1' ada di folder 'dataset/'")

batch_size = 32
img_height = 180
img_width = 180

print("Loading dataset...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    dataset_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

class_names = train_ds.class_names
print(f"Kelas yang terdeteksi: {class_names}")

# Optimasi dataset
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# =================================================================
# 2. MEMBUAT MODEL (ARSITEKTUR CNN SEDERHANA)
# =================================================================
num_classes = len(class_names)

model = keras.Sequential([
    layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    
    layers.Dropout(0.2),
    
    layers.Flatten(),
    
    layers.Dense(128, activation='relu'),
    
    layers.Dense(1)  # Binary classification dengan logits
])

# =================================================================
# 3. COMPILE MODEL
# =================================================================
model.compile(
    optimizer='adam',
    loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics=['accuracy']
)

model.summary()

# =================================================================
# 4. TRAINING MODEL
# =================================================================
# Hitung class weights untuk handle imbalance
labels = []
for _, l in train_ds.unbatch():
    labels.append(l.numpy())
labels = np.array(labels)

class_weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
class_weight_dict = dict(enumerate(class_weights))

print(f"Bobot Kelas yang akan digunakan: {class_weight_dict}")
print("----------------------------------------------------")

epochs = 10
print(f"Training model untuk {epochs} epochs...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs,
    class_weight=class_weight_dict
)

# =================================================================
# 5. EVALUASI MODEL
# =================================================================
print("\nEvaluasi model...")
val_loss, val_acc = model.evaluate(val_ds)
print(f"Validation Accuracy: {val_acc:.4f}")
print(f"Validation Loss: {val_loss:.4f}")

# Plot training history
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.savefig('training_history.png')
print("Training history saved to training_history.png")

# =================================================================
# 6. EXPORT MODEL
# =================================================================
# Simpan sebagai H5 dulu (lebih reliable, terutama untuk TF 2.20 + Python 3.12)
model_h5_path = 'model.h5'
print(f"\nMenyimpan model sebagai H5 ke: {model_h5_path}...")
try:
    model.save(model_h5_path)
    print(f"[OK] Model H5 berhasil disimpan di: {os.path.abspath(model_h5_path)}")
except Exception as e:
    print(f"[ERROR] Gagal menyimpan H5: {e}")

# Simpan sebagai SavedModel (format yang direkomendasikan untuk TFJS)
model_save_path = 'model'
print(f"\nMenyimpan model sebagai SavedModel ke: {model_save_path}...")
try:
    # Untuk Keras 3/TF 2.20+, gunakan tf.saved_model.save() langsung
    # Tapi jika error, gunakan workaround: load dari H5 lalu save
    if os.path.exists(model_h5_path):
        # Load dari H5 lalu save sebagai SavedModel
        print("   Loading dari H5 untuk convert ke SavedModel...")
        model_for_save = keras.models.load_model(model_h5_path)
        tf.saved_model.save(model_for_save, model_save_path)
        print(f"[OK] Model SavedModel berhasil disimpan di: {os.path.abspath(model_save_path)}")
    else:
        # Langsung save (mungkin gagal di TF 2.20 + Python 3.12)
        tf.saved_model.save(model, model_save_path)
        print(f"[OK] Model SavedModel berhasil disimpan di: {os.path.abspath(model_save_path)}")
except Exception as e:
    print(f"[WARNING] Gagal menyimpan SavedModel: {e}")
    print("Menggunakan H5 format sebagai alternatif...")
    if os.path.exists(model_h5_path):
        print(f"[OK] Model H5 tersedia di: {model_h5_path}")
        print("   Catatan: Untuk convert ke TFJS, kita bisa load H5 dulu lalu save sebagai SavedModel")

print("\n[OK] Export selesai! Model siap untuk dikonversi ke TensorFlow.js")

