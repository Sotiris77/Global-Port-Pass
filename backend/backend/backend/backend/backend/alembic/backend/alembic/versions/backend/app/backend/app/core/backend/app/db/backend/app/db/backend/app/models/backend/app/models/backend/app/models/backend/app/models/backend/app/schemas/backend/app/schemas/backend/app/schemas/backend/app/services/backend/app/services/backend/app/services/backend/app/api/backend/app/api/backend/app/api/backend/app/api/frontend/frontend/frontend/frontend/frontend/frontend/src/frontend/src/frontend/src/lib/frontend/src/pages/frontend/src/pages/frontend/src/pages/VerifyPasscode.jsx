import React, { useState } from 'react'
import { api } from '../lib/api'

export default function VerifyPasscode() {
  const [docId, setDocId] = useState('')
  const [code, setCode] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const verify = async () => {
    setError(''); setResult(null)
    try {
      const { data } = await api.post(`/documents/${docId}/passcode/verify`, { code })
      setResult(data.download_url)
    } catch (e) {
      setError(e?.response?.data?.detail || 'Verification failed')
    }
  }

  return (
    <div>
      <h2>Passcode Verify</h2>
      <div style={{display:'grid', gap:12}}>
        <input placeholder="Document ID" value={docId} onChange={e=>setDocId(e.target.value)} />
        <input placeholder="Passcode" value={code} onChange={e=>setCode(e.target.value)} />
        <button onClick={verify}>Verify & Get Link</button>
        {result && <div>One-time download URL: <a href={result} target="_blank" rel="noreferrer">{result}</a></div>}
        {error && <div style={{color:'crimson'}}>{error}</div>}
      </div>
    </div>
  )
}
