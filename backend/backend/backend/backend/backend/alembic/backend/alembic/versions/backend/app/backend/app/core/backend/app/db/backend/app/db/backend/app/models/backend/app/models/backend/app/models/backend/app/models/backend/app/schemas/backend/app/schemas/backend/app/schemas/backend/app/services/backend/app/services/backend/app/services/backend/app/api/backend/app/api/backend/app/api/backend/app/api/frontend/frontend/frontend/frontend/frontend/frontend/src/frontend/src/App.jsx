import React, { useState, useEffect } from 'react'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import VerifyPasscode from './pages/VerifyPasscode'

export default function App() {
  const [route, setRoute] = useState(window.location.hash.replace('#','') || 'login')

  useEffect(() => {
    const onHash = () => setRoute(window.location.hash.replace('#','') || 'login')
    window.addEventListener('hashchange', onHash)
    return () => window.removeEventListener('hashchange', onHash)
  }, [])

  const routes = {
    login: <Login onLoggedIn={() => window.location.hash = 'dashboard'} />,
    dashboard: <Dashboard />,
    verify: <VerifyPasscode />,
  }

  return (
    <div style={{maxWidth: 720, margin: '40px auto', fontFamily: 'system-ui, sans-serif'}}>
      <header style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 24}}>
        <h1 style={{margin:0}}>Global Port Pass</h1>
        <nav style={{display:'flex', gap:12}}>
          <a href="#login">Login</a>
          <a href="#dashboard">Dashboard</a>
          <a href="#verify">Passcode Verify</a>
        </nav>
      </header>
      <div style={{border:'1px solid #ddd', borderRadius:8, padding:16}}>
        {routes[route] || routes.login}
      </div>
      <footer style={{marginTop:24, fontSize:12, color:'#666'}}>MVP preview</footer>
    </div>
  )
}
