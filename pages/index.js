import { useState } from 'react'

export default function Home() {
  const [company, setCompany] = useState('')
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(false)

  async function search() {
    setLoading(true)
    const res = await fetch('/api/ubo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: company })
    })
    const result = await res.json()
    setData(result)
    setLoading(false)
  }

  return (
    <div style={{ padding: 20, maxWidth: 600, margin: 'auto' }}>
      <h1>Shtructure – Handelsregister Data</h1>
      <input
        type="text"
        placeholder="Firmenname eingeben"
        value={company}
        onChange={e => setCompany(e.target.value)}
        style={{ width: '100%', padding: 8, fontSize: 16 }}
      />
      <button
        onClick={search}
        disabled={loading || !company.trim()}
        style={{ marginTop: 10, padding: '8px 16px', fontSize: 16 }}
      >
        {loading ? 'Lädt…' : 'Suchen'}
      </button>

      {data && (
        <div style={{ marginTop: 30 }}>
          <pre style={{ whiteSpace: 'pre-wrap', fontSize: 14 }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  )
}
