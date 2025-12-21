import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Deteksi Phishing',
  description: 'Alat bantu untuk mendeteksi indikasi phishing dari screenshot',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  )
}

