'use client'

import { useEffect } from 'react'
import styles from './ProjectModal.module.css'

interface ProjectModalProps {
  isOpen: boolean
  onClose: () => void
}

export function ProjectModal({ isOpen, onClose }: ProjectModalProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
      
      // ESC key handler
      const handleEsc = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose()
        }
      }
      document.addEventListener('keydown', handleEsc)
      
      return () => {
        document.body.style.overflow = 'unset'
        document.removeEventListener('keydown', handleEsc)
      }
    } else {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeButton} onClick={onClose}>
          ×
        </button>
        
        <div className={styles.content}>
          <h2 className={styles.title}>Detail Project</h2>
          
          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Notebook & Training</h3>
            <p>
              Model ini dilatih menggunakan Google Colab. Anda dapat melihat notebook lengkap 
              untuk proses training, evaluasi, dan eksperimen di:
            </p>
            <a 
              href="https://colab.research.google.com/drive/1fNftxDWd0zVc6cpSPfUllp4ZrknrzWbd?usp=sharing" 
              target="_blank" 
              rel="noopener noreferrer"
              className={styles.link}
            >
              📓 Buka Notebook di Google Colab →
            </a>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Dataset</h3>
            <ul className={styles.list}>
              <li><strong>Total gambar:</strong> 1,497 (1,047 genuine + 450 phishing)</li>
              <li><strong>Split:</strong> 80% training (1,198), 20% validation (299)</li>
              <li><strong>Resolusi:</strong> 180x180 pixels, RGB</li>
              <li><strong>Format:</strong> PNG screenshots</li>
            </ul>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Metrik Performa</h3>
            <ul className={styles.list}>
              <li><strong>Training Accuracy:</strong> ~86%</li>
              <li><strong>Validation Accuracy:</strong> ~74.25%</li>
              <li><strong>Validation Loss:</strong> 0.7637</li>
              <li><strong>Epochs:</strong> 10</li>
            </ul>
            <p className={styles.note}>
              Model menunjukkan performa yang baik dengan akurasi validasi 74.25%. 
              Training history dapat dilihat di notebook Colab.
            </p>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Teknologi</h3>
            <ul className={styles.list}>
              <li><strong>Backend:</strong> FastAPI (Python)</li>
              <li><strong>Frontend:</strong> Next.js 14 (React, TypeScript)</li>
              <li><strong>ML Framework:</strong> TensorFlow/Keras</li>
              <li><strong>Model Format:</strong> H5 (Keras SavedModel)</li>
              <li><strong>Deployment:</strong> Vercel (Frontend) + Render/Railway (Backend)</li>
            </ul>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Creator</h3>
            <p>
              Project ini dibuat oleh:
            </p>
            <a 
              href="https://www.zulfianarahmi.tech/" 
              target="_blank" 
              rel="noopener noreferrer"
              className={styles.link}
            >
              👤 Zulfiana Rahmi - Cyber Security Engineer →
            </a>
          </section>

          <section className={styles.section}>
            <h3 className={styles.sectionTitle}>Repository</h3>
            <p>
              Kode source, dokumentasi, dan dataset akan dipublikasikan di GitHub repository.
              Link akan ditambahkan setelah project selesai.
            </p>
          </section>
        </div>
      </div>
    </div>
  )
}

