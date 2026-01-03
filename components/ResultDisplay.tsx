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
  
  // Determine which bar should be on top (higher probability)
  const showPhishingFirst = phishingProb >= genuineProb

  return (
    <div className={styles.result}>
      <div className={`${styles.label} ${isPhishing ? styles.phishing : styles.genuine}`}>
        <span className={styles.labelIcon}>
          {isPhishing ? '⚠️' : '✓'}
        </span>
        <span className={styles.labelText}>
          {isPhishing ? 'Indikasi Phishing' : 'Terlihat Genuine'}
        </span>
        {confidenceLevel && (
          <span className={styles.confidenceBadge}>
            {confidenceLevel}
          </span>
        )}
      </div>

      <div className={styles.probabilities}>
        {showPhishingFirst ? (
          <>
            <div className={styles.probItem}>
              <div className={styles.probHeader}>
                <span className={styles.probLabel}>Phishing</span>
                <span className={styles.probValue}>
                  {(phishingProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className={styles.probBar}>
                <div
                  className={`${styles.probFill} ${styles.phishingFill}`}
                  style={{ width: `${phishingProb * 100}%` }}
                />
              </div>
            </div>

            <div className={styles.probItem}>
              <div className={styles.probHeader}>
                <span className={styles.probLabel}>Genuine</span>
                <span className={styles.probValue}>
                  {(genuineProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className={styles.probBar}>
                <div
                  className={`${styles.probFill} ${styles.genuineFill}`}
                  style={{ width: `${genuineProb * 100}%` }}
                />
              </div>
            </div>
          </>
        ) : (
          <>
            <div className={styles.probItem}>
              <div className={styles.probHeader}>
                <span className={styles.probLabel}>Genuine</span>
                <span className={styles.probValue}>
                  {(genuineProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className={styles.probBar}>
                <div
                  className={`${styles.probFill} ${styles.genuineFill}`}
                  style={{ width: `${genuineProb * 100}%` }}
                />
              </div>
            </div>

            <div className={styles.probItem}>
              <div className={styles.probHeader}>
                <span className={styles.probLabel}>Phishing</span>
                <span className={styles.probValue}>
                  {(phishingProb * 100).toFixed(1)}%
                </span>
              </div>
              <div className={styles.probBar}>
                <div
                  className={`${styles.probFill} ${styles.phishingFill}`}
                  style={{ width: `${phishingProb * 100}%` }}
                />
              </div>
            </div>
          </>
        )}
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
          <strong>⚠️ Penting:</strong> Hasil ini adalah <strong>indikasi berdasarkan analisis visual</strong> dari screenshot 
          (warna, layout, tipografi, elemen UI) menggunakan model machine learning.
        </p>
        <p>
          <strong>Model bisa salah!</strong> Ini bukan keputusan final. 
          Selalu verifikasi <strong>URL</strong>, <strong>sertifikat SSL</strong>, dan <strong>domain</strong> sebelum 
          memasukkan informasi sensitif seperti password, kartu kredit, atau data pribadi.
        </p>
      </div>
    </div>
  )
}

