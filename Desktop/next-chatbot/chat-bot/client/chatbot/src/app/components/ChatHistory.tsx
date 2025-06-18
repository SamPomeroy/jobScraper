import { useState, useEffect } from "react";

interface ChatHistory {
  role: string;
  message: string;
  timestamp: string;
}

export default function ChatSidebar({ userId, onSelectConversation }: { userId: string; onSelectConversation: (msg: string) => void }) {
  const [history, setHistory] = useState<ChatHistory[]>([]);
  const [isOpen, setIsOpen] = useState(false); // ✅ Toggle state

  useEffect(() => {
    const fetchHistory = async () => {
      const response = await fetch(`/chat-history?user_id=${userId}`, {
        headers: { Authorization: `Bearer YOUR_AUTH_TOKEN` },
      });
      const data = await response.json();
      setHistory(data.history);
    };
    fetchHistory();
  }, [userId]);

  return (
    <div className={`fixed top-0 left-0 h-screen w-64 bg-gray-800 text-white p-4 transform transition-transform duration-300 ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
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