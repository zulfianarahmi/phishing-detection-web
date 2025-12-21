# -*- coding: utf-8 -*-
"""
Script untuk mempersiapkan struktur dataset
Memindahkan atau membuat symlink folder genuine_site_0 dan phishing_site_1 ke folder dataset/
"""

import os
import shutil

def prepare_dataset():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_dir = os.path.join(script_dir, 'dataset')
    
    # Buat folder dataset jika belum ada
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Path folder asli
    genuine_source = os.path.join(script_dir, 'genuine_site_0')
    phishing_source = os.path.join(script_dir, 'phishing_site_1')
    
    # Path folder tujuan
    genuine_dest = os.path.join(dataset_dir, 'genuine_site_0')
    phishing_dest = os.path.join(dataset_dir, 'phishing_site_1')
    
    # Cek apakah folder sudah ada di dataset/
    if not os.path.exists(genuine_dest):
        if os.path.exists(genuine_source):
            print(f"Memindahkan {genuine_source} ke {genuine_dest}...")
            # Gunakan symlink di Windows jika memungkinkan, atau copy
            try:
                # Coba buat symlink dulu (lebih cepat)
                if os.name == 'nt':  # Windows
                    import subprocess
                    subprocess.run(['mklink', '/D', genuine_dest, genuine_source], 
                                 shell=True, check=False)
                else:  # Unix/Linux/Mac
                    os.symlink(genuine_source, genuine_dest)
                print("[OK] Symlink dibuat untuk genuine_site_0")
            except:
                # Jika symlink gagal, copy folder
                print("Symlink gagal, menggunakan copy...")
                shutil.copytree(genuine_source, genuine_dest)
                print("[OK] Folder genuine_site_0 di-copy ke dataset/")
        else:
            print(f"⚠️  Folder {genuine_source} tidak ditemukan!")
    else:
        print(f"✅ Folder genuine_site_0 sudah ada di dataset/")
    
    if not os.path.exists(phishing_dest):
        if os.path.exists(phishing_source):
            print(f"Memindahkan {phishing_source} ke {phishing_dest}...")
            try:
                if os.name == 'nt':  # Windows
                    import subprocess
                    subprocess.run(['mklink', '/D', phishing_dest, phishing_source], 
                                 shell=True, check=False)
                else:
                    os.symlink(phishing_source, phishing_dest)
                print("[OK] Symlink dibuat untuk phishing_site_1")
            except:
                print("Symlink gagal, menggunakan copy...")
                shutil.copytree(phishing_source, phishing_dest)
                print("[OK] Folder phishing_site_1 di-copy ke dataset/")
        else:
            print(f"⚠️  Folder {phishing_source} tidak ditemukan!")
    else:
        print(f"✅ Folder phishing_site_1 sudah ada di dataset/")
    
    print(f"\n[OK] Dataset siap di: {dataset_dir}")
    print("   Struktur:")
    print(f"   dataset/")
    print(f"     ├── genuine_site_0/")
    print(f"     └── phishing_site_1/")

if __name__ == '__main__':
    prepare_dataset()

