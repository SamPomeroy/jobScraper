"use client";

import { useState, useEffect } from "react";

interface ChatHistory {
  role: string;
  message: string;
  timestamp: string;
}

export default function ChatSidebar({ userId, onSelectConversation }: { userId: string; onSelectConversation: (msg: string) => void }) {
  const [history, setHistory] = useState<ChatHistory[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
  const fetchHistory = async () => {
    try {
      const response = await fetch(`/api/history?user_id=${userId}`);
      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      setHistory(data.history || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };
  
  if (userId) {
    fetchHistory();
  }
}, [userId]);

  return (

  <div className={`absolute top-0 left-0 h-full w-64 bg-gray-800 text-white p-4 transform transition-transform duration-300 z-50 ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
      <button onClick={() => setIsOpen(!isOpen)} className="absolute right-[-50px] top-4 bg-gray-700 px-3 py-2 rounded-md text-white hover:bg-gray-600">
        {isOpen ? "❌ Close" : "📜 Open History"}
      </button>

      {isOpen && (
        <ul className="mt-4 space-y-2">
          {history.map((item, index) => (
            <li key={index} className="cursor-pointer hover:bg-gray-700 p-2 rounded-md" onClick={() => onSelectConversation(item.message)}>
              {item.message.slice(0, 40)}...
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}