'use client'

import styles from './LoadingState.module.css'

interface LoadingStateProps {
  message: string
}

export function LoadingState({ message }: LoadingStateProps) {
  return (
    <div className={styles.loading}>
      <div className={styles.spinner}></div>
      <p className={styles.message}>{message}</p>
    </div>
  )
}






