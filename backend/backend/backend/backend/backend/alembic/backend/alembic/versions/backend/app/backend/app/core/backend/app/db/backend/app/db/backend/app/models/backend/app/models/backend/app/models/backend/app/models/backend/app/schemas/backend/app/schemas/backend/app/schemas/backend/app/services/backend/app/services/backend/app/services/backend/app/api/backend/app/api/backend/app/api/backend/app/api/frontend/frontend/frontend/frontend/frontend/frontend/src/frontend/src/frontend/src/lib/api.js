import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE })

export function setToken(token) {
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  localStorage.setItem('gpp_token', token)
}

export function loadToken() {
  const t = localStorage.getItem('gpp_token')
  if (t) setToken(t)
}
