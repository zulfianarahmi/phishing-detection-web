'use client'

import styles from './ResultDisplay.module.css'

interface ResultDisplayProps {
  result: {
    label: 'phishing' | 'genuine'
    phishingProb: number
    genuineProb: number
    confidenceLevel?: string
    mainReason?: string
    details?: string[]
    recommendation?: string
  }
}

export function ResultDisplay({ result }: ResultDisplayProps) {
  const { 
    label, 
    phishingProb, 
    genuineProb, 
    confidenceLevel,
    mainReason,
    details,
    recommendation
  } = result
  const isPhishing = label === 'phishing'

  return (
    <div className={styles.result}>
      <div className={`${styles.label} ${isPhishing ? styles.phishing : styles.genuine}`}>
        <span className={styles.labelText}>
          {isPhishing ? '⚠️ Indikasi Phishing' : '✓ Terlihat Genuine'}
        </span>
        {confidenceLevel && (
          <span className={styles.confidenceBadge}>
            Kepercayaan: {confidenceLevel}
          </span>
        )}
      </div>

      <div className={styles.probabilities}>
        <div className={styles.probItem}>
          <div className={styles.probLabel}>Kemungkinan Phishing</div>
          <div className={styles.probBar}>
            <div
              className={`${styles.probFill} ${styles.phishingFill}`}
              style={{ width: `${phishingProb * 100}%` }}
            />
          </div>
          <div className={styles.probValue}>
            {(phishingProb * 100).toFixed(1)}%
          </div>
        </div>

        <div className={styles.probItem}>
          <div className={styles.probLabel}>Kemungkinan Genuine</div>
          <div className={styles.probBar}>
            <div
              className={`${styles.probFill} ${styles.genuineFill}`}
              style={{ width: `${genuineProb * 100}%` }}
            />
          </div>
          <div className={styles.probValue}>
            {(genuineProb * 100).toFixed(1)}%
          </div>
        </div>
      </div>

      {mainReason && (
        <div className={styles.explanation}>
          <h3 className={styles.explanationTitle}>Alasan Prediksi</h3>
          <p className={styles.mainReason}>{mainReason}</p>
          
          {details && details.length > 0 && (
            <ul className={styles.detailsList}>
              {details.map((detail, idx) => (
                <li key={idx}>{detail}</li>
              ))}
            </ul>
          )}
        </div>
      )}

      <div className={styles.warning}>
        <p>
          <strong>Rekomendasi:</strong> {recommendation || 'Hasil ini adalah indikasi berdasarkan analisis visual. Selalu verifikasi URL, sertifikat SSL, dan domain sebelum memasukkan informasi sensitif.'}
        </p>
      </div>
    </div>
  )
}

