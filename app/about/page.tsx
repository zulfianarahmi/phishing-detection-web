'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ProjectModal } from '@/components/ProjectModal'
import styles from './page.module.css'

export default function AboutPage() {
  const [isModalOpen, setIsModalOpen] = useState(false)

  return (
    <div>
      <div className={styles.container}>
        <header className={styles.header}>
          <Link href="/" className={styles.backLink}>← Kembali</Link>
          <h1 className={styles.title}>Tentang Model</h1>
          <button 
            onClick={() => setIsModalOpen(true)}
            className={styles.detailButton}
          >
            📋 Detail Project
          </button>
        </header>

        <main className={styles.main}>
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Tujuan Model</h2>
          <p>
            Model ini dirancang untuk membantu mendeteksi indikasi phishing dari screenshot halaman web.
            Model menganalisis karakteristik visual seperti layout, warna, tipografi, dan elemen UI
            yang umum ditemukan pada situs phishing.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Dataset</h2>
          <p>
            Model dilatih menggunakan dataset yang terdiri dari screenshot situs phishing dan situs genuine.
            Dataset ini dikumpulkan dari berbagai sumber dan telah melalui proses labeling manual.
          </p>
          <ul className={styles.list}>
            <li><strong>Total gambar:</strong> 1,497 (1,047 genuine + 450 phishing)</li>
            <li><strong>Split:</strong> 80% training (1,198), 20% validation (299)</li>
            <li><strong>Resolusi:</strong> 180x180 pixels, RGB</li>
            <li><strong>Format:</strong> PNG screenshots</li>
          </ul>
          <p className={styles.note}>
            Dataset dan notebook training dapat diakses melalui link di bagian &quot;Detail Project&quot;.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Arsitektur Model</h2>
          <p>Model menggunakan arsitektur CNN sederhana:</p>
          <ul className={styles.list}>
            <li>Input: Gambar RGB 180x180 pixels</li>
            <li>Rescaling layer: Normalisasi pixel values (0-255 → 0-1)</li>
            <li>Convolutional layers: 3 layer dengan filter 16, 32, 64</li>
            <li>MaxPooling: Reduksi dimensi</li>
            <li>Dropout: 0.2 untuk regularisasi</li>
            <li>Dense layers: 128 units + output layer (binary classification)</li>
            <li>Loss function: Binary Cross-Entropy (dengan logits)</li>
            <li>Optimizer: Adam</li>
          </ul>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Metrik Performa</h2>
          <ul className={styles.list}>
            <li><strong>Training Accuracy:</strong> ~86%</li>
            <li><strong>Validation Accuracy:</strong> ~74.25%</li>
            <li><strong>Validation Loss:</strong> 0.7637</li>
            <li><strong>Epochs:</strong> 10</li>
          </ul>
          <p className={styles.note}>
            Training history dan detail lengkap dapat dilihat di notebook Colab. 
            Klik tombol &quot;Detail Project&quot; di atas untuk informasi lebih lengkap.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Batasan Model</h2>
          <p>
            Model ini memiliki beberapa batasan yang perlu dipahami:
          </p>
          <ul className={styles.list}>
            <li>
              <strong>Domain shift:</strong> Model dilatih pada dataset tertentu dan mungkin tidak
              perform dengan baik pada jenis phishing baru yang belum pernah dilihat.
            </li>
            <li>
              <strong>Kualitas screenshot:</strong> Kualitas gambar yang buruk, resolusi rendah,
              atau kompresi berlebihan dapat mempengaruhi akurasi.
            </li>
            <li>
              <strong>UI baru:</strong> Desain UI yang sangat berbeda dari data training mungkin
              menghasilkan prediksi yang kurang akurat.
            </li>
            <li>
              <strong>Bahasa:</strong> Model fokus pada karakteristik visual, bukan teks. Prediksi
              tidak bergantung pada bahasa yang digunakan.
            </li>
            <li>
              <strong>Dark mode:</strong> Model mungkin perlu adaptasi untuk screenshot dark mode.
            </li>
            <li>
              <strong>False positives/negatives:</strong> Model tidak sempurna dan dapat menghasilkan
              prediksi yang salah.
            </li>
          </ul>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Cara Pakai yang Aman</h2>
          <div className={styles.warningBox}>
            <p><strong>Penting:</strong> Hasil prediksi ini adalah <strong>indikasi</strong>, bukan keputusan final.</p>
            <p>Sebelum memasukkan informasi sensitif atau melakukan login, selalu:</p>
            <ul className={styles.list}>
              <li>Periksa URL dengan teliti (typosquatting, domain mencurigakan)</li>
              <li>Verifikasi sertifikat SSL (HTTPS, valid certificate)</li>
              <li>Cek domain dan subdomain</li>
              <li>Waspada terhadap permintaan informasi yang tidak biasa</li>
              <li>Jika ragu, jangan lanjutkan</li>
            </ul>
          </div>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Privasi</h2>
          <p>
            <strong>Prediksi default:</strong> Semua proses prediksi berjalan di browser Anda (client-side).
            Gambar yang Anda upload tidak dikirim ke server kecuali Anda memberikan persetujuan eksplisit.
          </p>
          <p>
            <strong>Data collection (opt-in):</strong> Jika Anda memilih untuk berpartisipasi dalam
            pengumpulan data, gambar dan metadata prediksi akan dikirim ke server untuk tujuan riset
            dan peningkatan model. Data ini akan digunakan secara bertanggung jawab dan sesuai dengan
            kebijakan privasi.
          </p>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Notebook & Training</h2>
          <p>
            Proses training lengkap dapat dilihat di Google Colab notebook:
          </p>
          <a 
            href="https://colab.research.google.com/drive/1fNftxDWd0zVc6cpSPfUllp4ZrknrzWbd?usp=sharing" 
            target="_blank" 
            rel="noopener noreferrer"
            className={styles.externalLink}
          >
            📓 Buka Notebook di Google Colab →
          </a>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Creator</h2>
          <p>
            Project ini dibuat oleh:
          </p>
          <a 
            href="https://www.zulfianarahmi.tech/" 
            target="_blank" 
            rel="noopener noreferrer"
            className={styles.externalLink}
          >
            👤 Zulfiana Rahmi - Cyber Security Engineer →
          </a>
        </section>

        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Lisensi & Repositori</h2>
          <p>
            Model, dataset, dan kode akan dipublikasikan dengan lisensi open source.
            Link ke repository GitHub akan ditambahkan setelah project selesai.
          </p>
        </section>
        </main>

        <footer className={styles.footer}>
          <Link href="/">Kembali ke Home</Link>
        </footer>
      </div>
      
      <ProjectModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
      />
    </div>
  )
}

