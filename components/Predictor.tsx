'use client'

import { useState, useRef } from 'react'
import { UploadZone } from './UploadZone'
import { ResultDisplay } from './ResultDisplay'
import { LoadingState } from './LoadingState'
import styles from './Predictor.module.css'

interface PredictionResult {
  label: 'phishing' | 'genuine'
  phishingProb: number
  genuineProb: number
  confidenceLevel?: string
  mainReason?: string
  details?: string[]
  recommendation?: string
}

// API endpoint - ganti dengan URL backend kamu setelah deploy
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export function Predictor() {
  const [image, setImage] = useState<string | null>(null)
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [predicting, setPredicting] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [optIn, setOptIn] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)

  const handleImageSelect = (file: File) => {
    setImageFile(file)
    setError(null)
    setResult(null)
    setApiError(null)
    
    // Preview image
    const reader = new FileReader()
    reader.onload = (e) => {
      setImage(e.target?.result as string)
    }
    reader.readAsDataURL(file)
  }

  const predict = async () => {
    if (!imageFile) return

    try {
      setPredicting(true)
      setError(null)
      setApiError(null)

      // Buat FormData untuk upload
      const formData = new FormData()
      formData.append('file', imageFile)

      // Call API
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Gagal melakukan prediksi')
      }

      const data = await response.json()

      setResult({
        label: data.label,
        phishingProb: data.phishing_prob,
        genuineProb: data.genuine_prob,
      })

      // Jika user opt-in, kirim data ke endpoint collection
      if (optIn) {
        await submitToCollection(imageFile, data.label, data.phishing_prob)
      }
    } catch (err: any) {
      console.error('Prediction error:', err)
      setError(err.message || 'Gagal melakukan prediksi. Pastikan backend API berjalan.')
      setApiError('Pastikan backend API sudah di-deploy dan URL benar di environment variable NEXT_PUBLIC_API_URL')
    } finally {
      setPredicting(false)
    }
  }

  const submitToCollection = async (
    file: File,
    label: string,
    prob: number
  ) => {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('label', label)
      formData.append('probability', prob.toString())

      // Endpoint untuk collection di backend
      await fetch(`${API_URL}/api/collect`, {
        method: 'POST',
        body: formData,
      })
    } catch (err) {
      console.error('Collection error:', err)
      // Silent fail - tidak perlu ganggu user
    }
  }

  const reset = () => {
    setImage(null)
    setImageFile(null)
    setResult(null)
    setError(null)
    setOptIn(false)
  }

  return (
    <div className={styles.predictor}>
      {!image ? (
        <UploadZone onImageSelect={handleImageSelect} />
      ) : (
        <div className={styles.previewSection}>
          <div className={styles.imagePreview}>
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={image} alt="Preview" />
            <button onClick={reset} className={styles.resetButton}>
              Ganti Gambar
            </button>
          </div>

          {!result && !predicting && (
            <div className={styles.actions}>
              <label className={styles.optInLabel}>
                <input
                  type="checkbox"
                  checked={optIn}
                  onChange={(e) => setOptIn(e.target.checked)}
                />
                <span>
                  Saya setuju mengirim gambar ini untuk riset dan peningkatan model
                </span>
              </label>
              <button onClick={predict} className={styles.predictButton}>
                Analisis Gambar
              </button>
            </div>
          )}

          {predicting && <LoadingState message="Menganalisis gambar..." />}

          {result && (
            <ResultDisplay result={result} />
          )}

          {error && (
            <div className={styles.errorMessage}>
              {error}
              {apiError && (
                <div style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: '#666' }}>
                  {apiError}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

