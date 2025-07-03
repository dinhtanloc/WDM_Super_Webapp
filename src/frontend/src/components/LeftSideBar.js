'use client';
import { FiPlus, FiChevronLeft, FiMoreVertical, FiEdit, FiTrash, FiChevronRight } from 'react-icons/fi';

export default function LeftSideBar({
  isOpen,
  setIsOpen,
  conversations,
  selectedConversation,
  setSelectedConversation,
  contextMenu,
  setContextMenu,
  handleNewConversation,
  handleRename,
  handleDelete,
}) {
  const handleContextMenu = (e, convId) => {
    e.preventDefault();
    setContextMenu({ visible: true, x: e.pageX, y: e.pageY, convId });
  };

  return isOpen ? (
    <aside className={`w-64 bg-white p-4 border-r ${isOpen ? 'animate-fadeIn slide-in-left' : 'animate-fadeOut slide-out-left'}`}>
      <div className="flex justify-between mb-4">
        <button
          onClick={handleNewConversation}
          className="flex items-center gap-2 px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700"
        >
          <FiPlus /> Mới
        </button>
        <button onClick={() => setIsOpen(false)} className="text-red-600 hover:text-red-800">
          <FiChevronLeft />
        </button>
      </div>
      {conversations.map((c) => (
        <div
          key={c.id}
          onClick={() => setSelectedConversation(c.id)}
          onContextMenu={(e) => handleContextMenu(e, c.id)}
          className={`p-2 mb-2 rounded-lg cursor-pointer flex justify-between items-center ${
            selectedConversation === c.id ? 'bg-red-100' : 'hover:bg-gray-100'
          }`}
        >
          <div>
            <p className="font-semibold">{c.title}</p>
            <p className="text-sm text-gray-500">{c.createdAt}</p>
          </div>
          <button onClick={(e) => { e.stopPropagation(); handleContextMenu(e, c.id); }}>
            <FiMoreVertical />
          </button>
        </div>
      ))}
    </aside>
  ) : (
    <button onClick={() => setIsOpen(true)} className="w-6 bg-white text-red-600 hover:bg-gray-100 flex items-center justify-center">
      <FiChevronRight />
    </button>
  );
}