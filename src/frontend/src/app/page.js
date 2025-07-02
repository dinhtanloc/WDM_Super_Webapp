'use client';
import { useState, useEffect, useRef } from 'react';
// import {LeftSidebar} from '@components/LeftSidebar';
import RightSideBar from '@/components/RightSideBar';
import LeftSideBar from '@/components/LeftSideBar';
import {
  FiPaperclip,
} from 'react-icons/fi';
import './globals.css';

export default function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLeftOpen, setIsLeftOpen] = useState(true);
  const [isRightOpen, setIsRightOpen] = useState(true);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [contextMenu, setContextMenu] = useState({ visible: false, x: 0, y: 0, convId: null });
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(1);

  const [conversations, setConversations] = useState([
    { id: 1, title: 'Cuộc trò chuyện 1', createdAt: '2025-07-02' },
    { id: 2, title: 'Cuộc trò chuyện 2', createdAt: '2025-07-01' }
  ]);

  const [documents] = useState([
    { id: 1, type: 'text', content: 'Nội dung tài liệu 1', source: 'Doc1.pdf' },
    { id: 2, type: 'image', content: '/sample-image.jpg', source: 'Image1.jpg' },
    { id: 3, type: 'table', content: [['Cột 1', 'Cột 2'], ['Dữ liệu 1', 'Dữ liệu 2']], source: 'Table1.xlsx' }
  ]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    setIsLoading(true);
    const userMessage = { text: input, sender: 'user', references: [documents[0]] };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input }),
    });

    if (!response.ok) {
      setIsLoading(false);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let botMessage = { text: '', sender: 'bot', references: [documents[0]] };

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const chunk = decoder.decode(value);
      botMessage.text += chunk;
      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        if (lastMessage && lastMessage.sender === 'bot') {
          newMessages[newMessages.length - 1] = botMessage;
        } else {
          newMessages.push(botMessage);
        }
        return newMessages;
      });
    }

    setIsLoading(false);
  };

  const handleNewConversation = () => {
    const newConv = {
      id: conversations.length + 1,
      title: `Cuộc trò chuyện ${conversations.length + 1}`,
      createdAt: new Date().toISOString().split('T')[0]
    };
    setConversations([newConv, ...conversations]);
    setSelectedConversation(newConv.id);
    setMessages([]);
  };

  const handleContextMenu = (e, convId) => {
    e.preventDefault();
    setContextMenu({ visible: true, x: e.pageX, y: e.pageY, convId });
  };

  const handleRename = (convId) => {
    const newTitle = prompt('Nhập tên mới:', conversations.find(c => c.id === convId)?.title);
    if (newTitle) {
      setConversations(conversations.map(c => c.id === convId ? { ...c, title: newTitle } : c));
    }
    setContextMenu({ ...contextMenu, visible: false });
  };

  const handleDelete = (convId) => {
    if (confirm('Xoá cuộc trò chuyện này?')) {
      setConversations(conversations.filter(c => c.id !== convId));
      if (selectedConversation === convId) {
        setSelectedConversation(null);
        setMessages([]);
      }
    }
    setContextMenu({ ...contextMenu, visible: false });
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLeftOpen(isLeftOpen);
    }, 10);
    return () => clearTimeout(timer);
  }, [isLeftOpen]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsRightOpen(isRightOpen);
    }, 10);
    return () => clearTimeout(timer);
  }, [isRightOpen]);

  const ragContent = messages.length > 0 && messages[messages.length - 1].sender === 'bot'
    ? `Nội dung RAG liên quan: Đoạn trích từ Doc1.pdf - ${messages[messages.length - 1].text.slice(0, 20)}...`
    : 'Chưa có nội dung RAG.';

  return (
    <div className="flex flex-col min-h-screen">
      <header className="h-16 bg-red-600 text-white flex items-center px-4">
        <h1 className="text-lg font-semibold">Chatbot App</h1>
      </header>
      <main className="flex flex-1 overflow-hidden">
        <LeftSideBar
          isOpen={isLeftOpen}
          setIsOpen={setIsLeftOpen}
          conversations={conversations}
          selectedConversation={selectedConversation}
          setSelectedConversation={setSelectedConversation}
          contextMenu={contextMenu}
          setContextMenu={setContextMenu}
          handleNewConversation={handleNewConversation}
          handleRename={handleRename}
          handleDelete={handleDelete}
        />
        <section className="flex-1 flex flex-col bg-red-50 p-4">
          <div className="flex-1 bg-white rounded-xl shadow p-4 flex flex-col">
            <div className="flex-1 overflow-y-auto space-y-4">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs p-3 rounded-lg ${msg.sender === 'user' ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-800'}`}>
                    {msg.text}
                    {msg.references && (
                      <div className="mt-2 text-xs italic">
                        Dẫn chứng: {msg.references.map(ref => ref.source).join(', ')}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <form onSubmit={handleSend} className="mt-4 flex items-center gap-2">
              <label className="p-2 bg-gray-100 rounded cursor-pointer">
                <FiPaperclip />
                <input type="file" className="hidden" />
              </label>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 p-3 border rounded-lg focus:outline-none"
                placeholder="Nhập tin nhắn..."
                disabled={isLoading}
              />
              <button type="submit" className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700" disabled={isLoading}>
                Gửi
              </button>
            </form>
          </div>
        </section>
        <RightSideBar
          isOpen={isRightOpen}
          setIsOpen={setIsRightOpen}
          documents={documents}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          ragContent={ragContent}
        />
      </main>
      {contextMenu.visible && (
        <div
          className="fixed bg-white shadow-lg rounded-lg p-2 border z-50"
          style={{ top: contextMenu.y, left: contextMenu.x }}
        >
          <button onClick={() => handleRename(contextMenu.convId)} className="flex items-center gap-2 p-2 hover:bg-gray-100 w-full text-left">
            <FiEdit /> Đổi tên
          </button>
          <button onClick={() => handleDelete(contextMenu.convId)} className="flex items-center gap-2 p-2 hover:bg-gray-100 w-full text-left text-red-600">
            <FiTrash /> Xoá
          </button>
        </div>
      )}
    </div>
  );
}