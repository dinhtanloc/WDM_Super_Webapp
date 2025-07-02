'use client';
  import { useEffect, useState } from 'react';
  import { FiChevronRight, FiFileText, FiChevronLeft } from 'react-icons/fi'; // Thêm FiChevronLeft
  import ReactFlow, { MiniMap, Controls, Background } from 'react-flow-renderer';

  export default function RightSideBar({
    isOpen,
    setIsOpen,
    documents,
    activeTab,
    setActiveTab,
    ragContent,
  }) {
    useEffect(() => {
      const timer = setTimeout(() => {
        setIsOpen(isOpen);
      }, 10);
      return () => clearTimeout(timer);
    }, [isOpen, setIsOpen]);

    // Dữ liệu mẫu cho graph (trực quan hơn)
    const [elements, setElements] = useState([
      {
        id: 'doc1',
        type: 'input',
        data: { label: 'Doc1.pdf' },
        position: { x: 250, y: 50 },
        style: { background: '#ff6b6b', color: 'white', padding: 10, borderRadius: 5 },
      },
      {
        id: 'doc2',
        data: { label: 'Doc2.pdf' },
        position: { x: 100, y: 200 },
        style: { background: '#4ecdc4', color: 'white', padding: 10, borderRadius: 5 },
      },
      {
        id: 'doc3',
        data: { label: 'Doc3.pdf' },
        position: { x: 400, y: 200 },
        style: { background: '#45b7d1', color: 'white', padding: 10, borderRadius: 5 },
      },
      {
        id: 'rag',
        data: { label: 'RAG Content' },
        position: { x: 250, y: 350 },
        style: { background: '#96ceb4', color: 'white', padding: 10, borderRadius: 5 },
      },
      { id: 'e1-2', source: 'doc1', target: 'doc2', animated: true, style: { stroke: '#ff6b6b' } },
      { id: 'e1-3', source: 'doc1', target: 'doc3', animated: true, style: { stroke: '#ff6b6b' } },
      { id: 'e1-rag', source: 'doc1', target: 'rag', animated: true, style: { stroke: '#96ceb4' } },
    ]);

    return isOpen ? (
      <aside className={`w-164 bg-white p-4 border-l ${isOpen ? 'animate-fadeIn slide-in-right' : 'animate-fadeOut slide-out-right'}`}>
        <div className="flex justify-between mb-4">
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveTab(1)}
              className={`px-2 py-1 rounded ${activeTab === 1 ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-800'} hover:bg-red-700`}
            >
              PDF
            </button>
            <button
              onClick={() => setActiveTab(2)}
              className={`px-2 py-1 rounded ${activeTab === 2 ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-800'} hover:bg-red-700`}
            >
              RAG
            </button>
            <button
              onClick={() => setActiveTab(3)}
              className={`px-2 py-1 rounded ${activeTab === 3 ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-800'} hover:bg-red-700`}
            >
              Graph
            </button>
          </div>
          <button onClick={() => setIsOpen(false)} className="text-red-600 hover:text-red-800">
            <FiChevronRight />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {activeTab === 1 && (
            <div>
              <h3 className="font-bold mb-2">Danh sách PDF</h3>
              {documents
                .filter(doc => doc.type === 'text')
                .map((doc) => (
                  <div key={doc.id} className="mb-2">
                    <p className="flex items-center gap-2">
                      <FiFileText /> {doc.source}
                    </p>
                  </div>
                ))}
            </div>
          )}
          {activeTab === 2 && (
            <div>
              <h3 className="font-bold mb-2">Nội dung RAG</h3>
              <p>{ragContent}</p>
            </div>
          )}
          {activeTab === 3 && (
            <div>
              <h3 className="font-bold mb-2">Graph Thông tin</h3>
              <div style={{ height: '300px' }}>
                <ReactFlow elements={elements}>
                  <MiniMap />
                  <Controls />
                  <Background />
                </ReactFlow>
              </div>
            </div>
          )}
        </div>
      </aside>
    ) : (
      <button onClick={() => setIsOpen(true)} className="w-6 bg-white text-red-600 hover:bg-gray-100 flex items-center justify-center">
        <FiChevronLeft />
      </button>
    );
  }