'use client'

import { useRef, useState } from 'react'
import styles from './UploadZone.module.css'

interface UploadZoneProps {
  onImageSelect: (file: File) => void
}

export function UploadZone({ onImageSelect }: UploadZoneProps) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [isDragging, setIsDragging] = useState(false)

  const handleFile = (file: File) => {
    // Validasi file
    if (!file.type.startsWith('image/')) {
      alert('File harus berupa gambar (PNG, JPG, SVG)')
      return
    }

    if (file.size > 10 * 1024 * 1024) {
      alert('Ukuran file maksimal 10MB')
      return
    }

    onImageSelect(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)

    const file = e.dataTransfer.files[0]
    if (file) {
      handleFile(file)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      handleFile(file)
    }
  }

  return (
    <div
      className={`${styles.uploadZone} ${isDragging ? styles.dragging : ''}`}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onClick={() => fileInputRef.current?.click()}
    >
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleInputChange}
        className={styles.hiddenInput}
      />
      <div className={styles.content}>
        <div className={styles.icon}>📸</div>
        <p className={styles.text}>
          Drop screenshot atau <strong>pilih file</strong>
        </p>
        <p className={styles.hint}>
          Format: JPG, PNG & SVG · Max 10MB
        </p>
      </div>
    </div>
  )
}






