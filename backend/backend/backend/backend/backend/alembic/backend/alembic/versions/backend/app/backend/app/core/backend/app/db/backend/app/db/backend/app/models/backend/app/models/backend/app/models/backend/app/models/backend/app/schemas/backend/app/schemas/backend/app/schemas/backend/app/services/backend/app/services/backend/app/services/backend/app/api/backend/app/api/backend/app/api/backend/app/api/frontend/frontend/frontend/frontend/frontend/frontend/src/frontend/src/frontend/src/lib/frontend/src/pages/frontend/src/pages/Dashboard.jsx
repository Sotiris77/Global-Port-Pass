import React, { useEffect, useState } from 'react'
import { api, loadToken } from '../lib/api'

export default function Dashboard() {
  const [docs, setDocs] = useState([])
  const [file, setFile] = useState(null)
  const [pcMap, setPcMap] = useState({})
  const [message, setMessage] = useState('')

  const refresh = async () => {
    try {
      const { data } = await api.get('/documents/')
      setDocs(data)
    } catch (e) {
      setMessage('Please login first (token missing).')
    }
  }

  useEffect(() => { loadToken(); refresh(); }, [])

  const upload = async () => {
    if (!file) return
    const fd = new FormData()
    fd.append('file', file)
    await api.post('/documents/upload', fd)
    setFile(null)
    await refresh()
  }

  const makePasscode = async (docId) => {
    const { data } = await api.post(`/documents/${docId}/passcode`, { expires_minutes: 10 })
    setPcMap({ ...pcMap, [docId]: data.code })
  }

  return (
    <div>
      <h2>My Documents</h2>
      <div style={{display:'flex', gap:8, alignItems:'center', marginBottom:12}}>
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button onClick={upload}>Upload</button>
      </div>
      {message && <div>{message}</div>}
      <ul>
        {docs.map(d => (
          <li key={d.id} style={{marginBottom:8}}>
            <b>{d.filename}</b> <small>({d.content_type})</small>
            <div>
              <button onClick={() => makePasscode(d.id)}>Create one-time passcode</button>
              {pcMap[d.id] && <span style={{marginLeft:8}}>Passcode: <code>{pcMap[d.id]}</code></span>}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
