import Link from 'next/link'
import styles from './not-found.module.css'

export default function NotFound() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>404</h1>
      <p className={styles.message}>Halaman tidak ditemukan</p>
      <Link href="/" className={styles.link}>
        Kembali ke Home
      </Link>
    </div>
  )
}

