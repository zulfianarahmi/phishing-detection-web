import { NextRequest, NextResponse } from 'next/server'

// Endpoint untuk mengumpulkan data dari user (opt-in)
// Forward ke backend API

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    
    // Forward ke backend API
    const response = await fetch(`${API_URL}/api/collect`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('Backend API error')
    }

    const data = await response.json()
    return NextResponse.json(data, { status: 200 })
  } catch (error) {
    console.error('Collection error:', error)
    return NextResponse.json(
      { error: 'Failed to collect data' },
      { status: 500 }
    )
  }
}

