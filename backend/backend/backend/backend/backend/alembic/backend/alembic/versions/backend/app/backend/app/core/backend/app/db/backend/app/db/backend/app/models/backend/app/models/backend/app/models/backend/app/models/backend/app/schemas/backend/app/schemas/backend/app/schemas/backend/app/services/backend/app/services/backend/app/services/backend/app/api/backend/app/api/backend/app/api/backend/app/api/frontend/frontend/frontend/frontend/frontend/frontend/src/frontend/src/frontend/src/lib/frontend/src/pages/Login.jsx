import React, { useState } from 'react'
import { api, setToken } from '../lib/api'

export default function Login({ onLoggedIn }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [role, setRole] = useState('vessel')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const doRegister = async () => {
    setError(''); setLoading(true)
    try {
      await api.post('/auth/register', { email, password, role })
      await doLogin()
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to register')
    } finally { setLoading(false) }
  }

  const doLogin = async () => {
    setError(''); setLoading(true)
    try {
      const form = new URLSearchParams({ username: email, password })
      const { data } = await api.post('/auth/login', form)
      setToken(data.access_token)
      onLoggedIn && onLoggedIn()
    } catch (e) {
      setError(e?.response?.data?.detail || 'Failed to login')
    } finally { setLoading(false) }
  }

  return (
    <div>
      <h2>Login / Register</h2>
      <div style={{display:'grid', gap:12}}>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <div>
          <label>Role:&nbsp;</label>
          <select value={role} onChange={e=>setRole(e.target.value)}>
            <option value="vessel">Vessel</option>
            <option value="port">Port</option>
          </select>
        </div>
        <div style={{display:'flex', gap:8}}>
          <button onClick={doLogin} disabled={loading}>Login</button>
          <button onClick={doRegister} disabled={loading}>Register</button>
        </div>
        {error && <div style={{color:'crimson'}}>{error}</div>}
      </div>
    </div>
  )
}
