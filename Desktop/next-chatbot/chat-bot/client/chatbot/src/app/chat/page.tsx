// // Enhanced Chatbot Component
// "use client";

// import { useEffect, useState } from "react";
// import { sendMessage, getChatHistory } from "../../utils/api";
// import { createClient } from "@supabase/supabase-js";

// // 🔐 Supabase client
// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );

// export default function Chatbot() {
//   const [query, setQuery] = useState("");
//   const [isLoading, setIsLoading] = useState(false);
//   const [userId, setUserId] = useState<string | null>(null);
//   const [messages, setMessages] = useState<{ role: string; text: string }[]>([]);

//   // Get Supabase user ID on load
//   useEffect(() => {
//     const getUser = async () => {
//       const { data } = await supabase.auth.getUser();
//       setUserId(data?.user?.id ?? null);
//     };
//     getUser();
//   }, []);

//   // Load chat history from FastAPI
//   useEffect(() => {
//     if (!userId) return;
//     const fetchHistory = async () => {
//       const history = await getChatHistory(userId);
//       setMessages(history.map((msg: any) => ({
//         role: msg.role,
//         text: msg.message,
//       })));
//     };
//     fetchHistory();
//   }, [userId]);

//   // Send new message to assistant
//   const handleSend = async () => {
//     if (!query.trim() || !userId) return;
    
//     try {
//       setIsLoading(true);
//       // Add user message to state
//       setMessages((prev) => [...prev, { role: "user", text: query }]);
      
//       // Send and receive assistant reply
//       const reply = await sendMessage(query, userId);
//       setMessages((prev) => [...prev, { role: "assistant", text: reply }]);
//       setQuery("");
//     } catch (err) {
//       setMessages((prev) => [...prev, { role: "assistant", text: "Something went wrong." }]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e: React.KeyboardEvent) => {
//     if (e.key === "Enter" && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
//       <div className="max-w-4xl mx-auto">
//         {/* Header */}
//         <div className="text-center mb-8">
//           <h1 className="text-4xl font-bold text-gray-900 mb-2">
//             Learning Assistant 🤖
//           </h1>
//           <p className="text-gray-600">Ask me anything and I'll help you learn!</p>
//         </div>

//         {/* Chat Container */}
//         <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
//           {/* Chat Messages */}
//           <div className="h-96 md:h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
//             {messages.length === 0 ? (
//               <div className="text-center text-gray-500 mt-20">
//                 <div className="text-6xl mb-4">💬</div>
//                 <p className="text-lg">Start a conversation!</p>
//                 <p className="text-sm">Ask me anything you'd like to learn about.</p>
//               </div>
//             ) : (
//               messages.map((msg, i) => (
//                 <div
//                   key={i}
//                   className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
//                 >
//                   <div
//                     className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl px-4 py-3 rounded-2xl ${
//                       msg.role === "user"
//                         ? "bg-blue-600 text-white rounded-br-md"
//                         : "bg-white text-gray-800 shadow-md rounded-bl-md border"
//                     }`}
//                   >
//                     <div className="flex items-start space-x-2">
//                       <div
//                         className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
//                           msg.role === "user"
//                             ? "bg-blue-500 text-white"
//                             : "bg-green-500 text-white"
//                         }`}
//                       >
//                         {msg.role === "user" ? "U" : "🤖"}
//                       </div>
//                       <p className="flex-1 text-sm leading-relaxed">{msg.text}</p>
//                     </div>
//                   </div>
//                 </div>
//               ))
//             )}

//             {isLoading && (
//               <div className="flex justify-start">
//                 <div className="bg-white shadow-md rounded-2xl rounded-bl-md border px-4 py-3 max-w-xs">
//                   <div className="flex items-center space-x-2">
//                     <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
//                       <span className="text-white text-xs">🤖</span>
//                     </div>
//                     <div className="flex space-x-1">
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
//                     </div>
//                   </div>
//                 </div>
//               </div>
//             )}
//           </div>

//           {/* Input Area */}
//           <div className="p-6 bg-white border-t">
//             <div className="flex space-x-4">
//               <div className="flex-1">
//                 <textarea
//                   value={query}
//                   onChange={(e) => setQuery(e.target.value)}
//                   onKeyPress={handleKeyPress}
//                   placeholder="Type your message here..."
//                   className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none outline-none"
//                   rows={1}
//                   disabled={isLoading || !userId}
//                 />
//               </div>
//               <button
//                 onClick={handleSend}
//                 disabled={isLoading || !query.trim() || !userId}
//                 className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-xl transition duration-200 transform hover:scale-105 disabled:hover:scale-100 min-w-[80px]"
//               >
//                 {isLoading ? (
//                   <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto"></div>
//                 ) : (
//                   "Send"
//                 )}
//               </button>
//             </div>
//             {!userId && (
//               <p className="text-red-500 text-sm mt-2 text-center">
//                 Please sign in to use the chatbot
//               </p>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }
'use client'; 
import ChatBot from '../components/ChatBot';

interface ChatPageProps {
  params: {
    id: string;
  };
}

export default function ChatPage({ params }: ChatPageProps) {
  // You can use the chat ID from params.id if needed
  // For now, we'll just render the ChatBot component
  
  return <ChatBot />;
}