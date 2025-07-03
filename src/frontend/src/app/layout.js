import './globals.css';
import Link from 'next/link';

export const metadata = {
  title: 'My App',
  description: 'This is a demo app',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-red-50" style={{ height: '1100px', width: '100%' }}>
        <header className="bg-red-600 text-white p-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">My App</h1>
          <Link href="/auth/login">
            <button className="p-2 bg-white text-red-600 rounded-lg hover:bg-gray-100 transition-colors">
              Đăng nhập / Đăng ký
            </button>
          </Link>
        </header>
        <main>{children}</main>
        <footer className="bg-red-600 text-white p-4 text-center">
          <p>© 2025 My App</p>
        </footer>
      </body>
    </html>
  );
}