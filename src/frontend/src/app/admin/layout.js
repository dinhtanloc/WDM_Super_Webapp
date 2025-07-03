export default function AdminLayout({ children }) {
  return (
    <div>
      <nav style={{ background: '#eee', padding: 10 }}>
        <strong>Admin Panel</strong> | <a href="/">Home</a>
      </nav>
      <div style={{ padding: 20 }}>{children}</div>
    </div>
  )
}
