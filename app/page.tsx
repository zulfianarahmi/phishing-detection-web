'use client'

import Link from 'next/link'
import { Predictor } from '@/components/Predictor'
import styles from './page.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <main className={styles.main}>
        <Predictor />
      </main>

      <footer className={styles.footer}>
        <div className={styles.footerLinks}>
          <Link href="/about">Tentang Model</Link>
          <span className={styles.separator}>•</span>
          <a 
            href="https://colab.research.google.com/drive/1fNftxDWd0zVc6cpSPfUllp4ZrknrzWbd?usp=sharing" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            Notebook
          </a>
          <span className={styles.separator}>•</span>
          <a 
            href="https://www.zulfianarahmi.tech/" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            Creator
          </a>
        </div>
      </footer>
    </div>
  )
}

