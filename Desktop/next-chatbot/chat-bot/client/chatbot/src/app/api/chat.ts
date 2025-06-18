import axios from "axios";
import { supabase } from '../../utils/supabase/client';

export async function fetchChatResponse(query: string): Promise<string> {
  try {
    console.log("Sending request to FastAPI:", query);
    
    // Get the auth token
    const token = localStorage.getItem("sb-access-token");
    
    // Prepare headers
    const headers: Record<string, string> = {
      'Content-Type': 'application/json'
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    // Make the request with proper headers
    const res = await axios.get(`http://127.0.0.1:8000/chat`, { 
      params: { query },
      headers
    });
    
    console.log("Raw response from FastAPI:", res.data);
    
    return res.data.response;
  } catch (err) {
    console.error("Error fetching chat response:", err);
    
    // More specific error handling
    if (axios.isAxiosError(err)) {
      if (err.response?.status === 401) {
        // Token expired or invalid - redirect to login
        localStorage.removeItem("sb-access-token");
        window.location.href = '/signin';
        return "Authentication required. Please sign in again.";
      } else if (err.response?.status === 500) {
        return "Server error. Please try again later.";
      } else {
        return `Error: ${err.response?.data?.detail || "Unable to fetch response"}`;
      }
    }
    
    return "Error: Unable to connect to the server.";
  }
}

// Alternative function using POST method (more RESTful)
export async function fetchChatResponsePost(message: string): Promise<string> {
  try {
    console.log("Sending POST request to FastAPI:", message);
    
    // Get the auth token
    const token = localStorage.getItem("sb-access-token");
    
    if (!token) {
      throw new Error("No authentication token found");
    }
    
    // Prepare headers
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
    
    // Make POST request
    const res = await axios.post(`http://127.0.0.1:8000/chat`, 
      { message }, 
      { headers }
    );
    
    console.log("Raw response from FastAPI:", res.data);
    
    return res.data.response;
  } catch (err) {
    console.error("Error fetching chat response:", err);
    
    if (axios.isAxiosError(err)) {
      if (err.response?.status === 401) {
        localStorage.removeItem("sb-access-token");
        window.location.href = '/signin';
        return "Authentication required. Please sign in again.";
      } else if (err.response?.status === 500) {
        return "Server error. Please try again later.";
      } else {
        return `Error: ${err.response?.data?.detail || "Unable to fetch response"}`;
      }
    }
    
    return "Error: Unable to connect to the server.";
  }
}

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem("sb-access-token");
  const headers: Record<string, string> = {};
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export async function getUserClient() {
  const { data, error } = await supabase.auth.getUser();
  if (error) {
    console.error("Client-side user fetch error:", error);
    return null;
  }
  return data.user;
}

// Function to get chat history
export async function getChatHistory(userId: string): Promise<any[]> {
  try {
    const token = localStorage.getItem("sb-access-token");
    
    if (!token) {
      throw new Error("No authentication token found");
    }
    
    const headers = {
      'Authorization': `Bearer ${token}`
    };
    
    const res = await axios.get(`http://127.0.0.1:8000/history`, {
      params: { user_id: userId },
      headers
    });
    
    return res.data.history || [];
  } catch (err) {
    console.error("Error fetching chat history:", err);
    return [];
  }
}