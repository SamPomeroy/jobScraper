// // utils/api.ts
// export const sendMessage = async (message: string, userId: string, token: string) => {
//   // const res = await fetch("http://localhost:8000/chat", {
//   //   method: "POST",
//   //   headers: { "Content-Type": "application/json" },
//   //   body: JSON.stringify({ user_id: userId, message }),
//   // });
// const res = await fetch("http://localhost:8000/chat", {
//   method: "POST",
//   headers: {
//     "Content-Type": "application/json",
//     Authorization: `Bearer ${token}`
//   },
//   body: JSON.stringify({ user_id: userId, message }),
// });
//   const data = await res.json();
//   console.log("Raw response from FastAPI:", data);

//   return data.response || "Error: could not get response.";
// };

// export const getChatHistory = async (userId: string, token?: string) => {
//   const res = await fetch(`http://localhost:8000/history?user_id=${userId}`, {
//     headers: token
//       ? {
//           Authorization: `Bearer ${token}`
//         }
//       : undefined
//   });

//   const data = await res.json();
//   return data.history || [];
// };
// // export const getChatHistory = async (userId: string) => {
//   const res = await fetch(`http://localhost:8000/history?user_id=${userId}`);
//   const data = await res.json();
//   return data.history || [];
// };
// import { createServerClient, type CookieOptions } from "@supabase/ssr";
// import { type NextRequest, NextResponse } from "next/server";

// export const createMiddlewareClient = (request: NextRequest, response: NextResponse) => {
//   return createServerClient(
//     process.env.NEXT_PUBLIC_SUPABASE_URL!,
//     process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
//     {
//       cookies: {
//         getAll() {
//           return request.cookies.getAll().map(({ name, value }) => ({
//             name,
//             value,
//             options: {},
//           }));
//         },
//         setAll(cookiesToSet) {
//           cookiesToSet.forEach(({ name, value, options }) => {
//             response.cookies.set(name, value, options);
//           });
//         },
//       },
//     }
//   );
// };

// function getAuthHeaders(): Record<string, string> {
//   const token = localStorage.getItem("sb-access-token");
//   return token
//     ? { Authorization: `Bearer ${token}` }
//     : {};
// }

// export const sendMessage = async (message: string, userId: string) => {
//   const res = await fetch("http://localhost:8000/chat", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//       ...getAuthHeaders()
//     },
//     body: JSON.stringify({ user_id: userId, message })
//   });

//   const data = await res.json();
//   console.log("Raw response from FastAPI:", data);
//   return data.response || "Error: could not get response.";
// };

// export const getChatHistory = async (userId: string) => {
//   const res = await fetch(`http://localhost:8000/history?user_id=${userId}`, {
//     headers: getAuthHeaders()
//   });

//   const data = await res.json();
//   return data.history || [];
// };
// src/utils/api.ts
import { supabase } from '@/utils/supabase/client';

// Example function to send a message
export async function sendMessage(query: string, userId: string): Promise<string> {
  // Insert the message into your "chat_messages" table.
  const { data, error } = await supabase
    .from('chat_messages')
    .insert([{ user_id: userId, message: query }]);
    
  if (error) {
    console.error('Error sending message:', error);
    throw new Error(error.message);
  }
  
  // Return a dummy reply for now.
  return 'This is a dummy reply.';
}

// Example function to get chat history for a user
export async function getChatHistory(userId: string): Promise<any[]> {
  const { data, error } = await supabase
    .from('chat_messages')
    .select('*')
    .eq('user_id', userId);
    
  if (error) {
    console.error('Error fetching chat history:', error);
    return [];
  }
  
  return data ?? [];
}