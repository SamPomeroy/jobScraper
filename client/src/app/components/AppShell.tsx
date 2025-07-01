"use client";
import React, { useState, useEffect, useRef } from "react";
import { createClient } from "@supabase/supabase-js";
import Navbar from "@/app/components/navbar";
import HomePage from "@/app/pages/home/HomePage";
import AboutPage from "../pages/about/AboutPage";
import ContactPage from "../pages/contact/ContactPage";
import AuthForm from "@/app/components/AuthForm";
import Dashboard from "./dashboard/Dashboard";
import Footer from "./footer/Footer";
import type { AuthUser } from "../types/application";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);


const AUTH_TIMEOUT = 2 * 60 * 60 * 1000;

export default function AppShell({
  initialUser,
}: {
  initialUser: AuthUser | null;
}) {
  const [user, setUser] = useState<AuthUser | null>(initialUser);
  const [currentPage, setCurrentPage] = useState("home");
  const [loading, setLoading] = useState(true);
  const [showTimeoutWarning, setShowTimeoutWarning] = useState(false);
  
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const warningTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const lastActivityRef = useRef<number>(Date.now());


  const resetAuthTimeout = () => {
    lastActivityRef.current = Date.now();
    

    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);

    if (user) {

      warningTimeoutRef.current = setTimeout(() => {
        setShowTimeoutWarning(true);
      }, AUTH_TIMEOUT - 10 * 60 * 1000);

      timeoutRef.current = setTimeout(() => {
        handleLogout();
        alert("Session expired due to inactivity. Please log in again.");
      }, AUTH_TIMEOUT);
    }
  };


  useEffect(() => {
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    const resetTimer = () => {
      if (user) {
        resetAuthTimeout();
        setShowTimeoutWarning(false);
      }
    };


    events.forEach(event => {
      document.addEventListener(event, resetTimer, true);
    });


    return () => {
      events.forEach(event => {
        document.removeEventListener(event, resetTimer, true);
      });
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
    };
  }, [user]);

  useEffect(() => {
    const checkSession = async () => {
      const {
        data: { session },
        error,
      } = await supabase.auth.getSession();
      
      if (error) {
        console.error("Session error:", error);
      } else if (session?.user) {
        setUser(session.user as AuthUser);
        setCurrentPage("dashboard");
        resetAuthTimeout(); // Start timeout timer
      }
      setLoading(false);
    };

    checkSession();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((event: string, session: any) => {
      if (event === "SIGNED_IN" && session?.user) {
        setUser(session.user as AuthUser);
        setCurrentPage("dashboard");
        resetAuthTimeout(); // Start timeout timer
      } else if (event === "SIGNED_OUT") {
        setUser(null);
        setCurrentPage("home");
        setShowTimeoutWarning(false);
        // Clear timeouts
        if (timeoutRef.current) clearTimeout(timeoutRef.current);
        if (warningTimeoutRef.current) clearTimeout(warningTimeoutRef.current);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    // Clear any user-specific localStorage data
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith(`user_`) || key.startsWith(`jobs_`)) {
        localStorage.removeItem(key);
      }
    });
  };

  const handleAuthSuccess = (authUser: AuthUser) => {
    setUser(authUser);
    setCurrentPage("dashboard");
    resetAuthTimeout(); // Start timeout timer
  };
  const handleExtendSession = () => {
    resetAuthTimeout();
    setShowTimeoutWarning(false);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto bg-gray-50 dark:bg-gray-900 dark:text-gray-100">
      <Navbar
        user={user}
        onLogoutAction={handleLogout}
        currentPage={currentPage}
        setCurrentPageAction={setCurrentPage}
      />
      
      <main className="flex-1">
        {currentPage === "home" && (
          <HomePage user={user as any} setCurrentPageAction={setCurrentPage} />
        )}
        {currentPage === "about" && <AboutPage />}
        {currentPage === "contact" && <ContactPage />}
        {currentPage === "login" && (
          <AuthForm
            mode="login"
            onSuccessAction={handleAuthSuccess}
            setCurrentPageAction={setCurrentPage}
          />
        )}
        {currentPage === "register" && (
          <AuthForm
            mode="register"
            onSuccessAction={handleAuthSuccess}
            setCurrentPageAction={setCurrentPage}
          />
        )}
        {currentPage === "dashboard" && user && (
          <Dashboard user={user} />
        )}
      </main>

      <Footer setCurrentPage={setCurrentPage} />

      {/* Session Timeout Warning Modal */}
      {showTimeoutWarning && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg max-w-md w-full">
            <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">
              Session Expiring Soon
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Your session will expire in 10 minutes due to inactivity. 
              Would you like to extend your session?
            </p>
            <div className="flex justify-end gap-3">
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm rounded border border-gray-300 hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
              >
                Logout Now
              </button>
              <button
                onClick={handleExtendSession}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Stay Logged In
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
