'use client';
import { useState } from 'react';
import Link from 'next/link';

export default function LoginPage() {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="w-full max-w-md p-8 bg-white rounded-2xl shadow-xl transform transition-all duration-500">
      <div className="flex justify-center mb-6">
        <button
          onClick={() => setIsLogin(true)}
          className={`px-4 py-2 text-lg font-semibold ${isLogin ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
        >
          Đăng nhập
        </button>
        <button
          onClick={() => setIsLogin(false)}
          className={`px-4 py-2 text-lg font-semibold ${!isLogin ? 'text-blue-600 border-b-2 border-blue-600' : 'text-gray-500'}`}
        >
          Đăng ký
        </button>
      </div>

      {isLogin ? (
        <div className="animate-fadeIn">
          <h2 className="text-2xl font-bold text-center mb-6">Đăng nhập</h2>
          <form>
            <div className="mb-4">
              <label className="block text-gray-700">Email</label>
              <input
                type="email"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập email của bạn"
              />
            </div>
            <div className="mb-6">
              <label className="block text-gray-700">Mật khẩu</label>
              <input
                type="password"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập mật khẩu"
              />
            </div>
            <button
              type="submit"
              className="w-full p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Đăng nhập
            </button>
          </form>
        </div>
      ) : (
        <div className="animate-fadeIn">
          <h2 className="text-2xl font-bold text-center mb-6">Đăng ký</h2>
          <form>
            <div className="mb-4">
              <label className="block text-gray-700">Họ và tên</label>
              <input
                type="text"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập họ và tên"
              />
            </div>
            <div className="mb-4">
              <label className="block text-gray-700">Email</label>
              <input
                type="email"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập email của bạn"
              />
            </div>
            <div className="mb-6">
              <label className="block text-gray-700">Mật khẩu</label>
              <input
                type="password"
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Nhập mật khẩu"
              />
            </div>
            <button
              type="submit"
              className="w-full p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Đăng ký
            </button>
          </form>
        </div>
      )}
      <p className="mt-4 text-center text-gray-600">
        {isLogin ? 'Chưa có tài khoản?' : 'Đã có tài khoản?'}{' '}
        <button
          onClick={() => setIsLogin(!isLogin)}
          className="text-blue-600 hover:underline"
        >
          {isLogin ? 'Đăng ký ngay' : 'Đăng nhập'}
        </button>
      </p>
    </div>
  );
}