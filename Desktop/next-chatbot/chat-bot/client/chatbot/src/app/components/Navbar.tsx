// Enhanced Navbar Component
"use client";

import { useState, useEffect } from "react";
import { getUser, signOut } from "../api/auth/auth";
import { User } from "@supabase/supabase-js";
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs';

const supabase = createClientComponentClient();

export default function Navbar() {
  const [user, setUser] = useState<User | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await getUser();
        setUser(currentUser);
      } catch (error) {
        console.log("Error fetching user:", error);
      }
    };

    fetchUser();

    // Keep listening for authentication state changes
    const { data: authListener } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setUser(session?.user || null);
      }
    );

    return () => {
      authListener.subscription.unsubscribe();
    };
  }, []);

  const handleSignOut = async () => {
    try {
      await signOut();
      setUser(null);
      setIsMenuOpen(false);
      window.location.href = "/";
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };

  return (
    <nav className="bg-gradient-to-r from-slate-900 via-blue-900 to-indigo-900 shadow-2xl sticky top-0 z-50 backdrop-blur-sm border-b border-blue-800/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <a 
              href="/" 
              className="flex items-center space-x-2 text-white text-xl font-bold hover:text-blue-200 transition-all duration-300 group"
            >
              <div className="bg-gradient-to-br from-blue-400 to-purple-500 p-2 rounded-xl group-hover:scale-110 transition-transform duration-300">
                <span className="text-white">🤖</span>
              </div>
              <span className="bg-gradient-to-r from-blue-200 to-purple-200 bg-clip-text text-transparent">
                Learning Assistant
              </span>
            </a>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            <a
              href="/chat"
              className="text-white/90 hover:text-white hover:bg-white/10 px-4 py-2 rounded-xl transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-white/20"
            >
              Home
            </a>
            
            {user ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-3 bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-sm border border-blue-400/30 px-4 py-2 rounded-xl">
                  <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">
                      {user.email?.charAt(0).toUpperCase()}
                    </span>
                  </div>
                  <span className="text-white/90 text-sm font-medium">
                    {user.email?.split('@')[0]}
                  </span>
                </div>
                <button
                  onClick={handleSignOut}
                  className="bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white px-5 py-2 rounded-xl transition-all duration-300 font-medium shadow-lg hover:shadow-red-500/25 transform hover:scale-105"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <a
                  href="/signin"
                  className="text-white/90 hover:text-white hover:bg-white/10 px-5 py-2 rounded-xl transition-all duration-300 font-medium backdrop-blur-sm border border-transparent hover:border-white/20"
                >
                  Sign In
                </a>
                <a
                  href="/signup"
                  className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-5 py-2 rounded-xl transition-all duration-300 font-medium shadow-lg hover:shadow-emerald-500/25 transform hover:scale-105"
                >
                  Sign Up
                </a>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="text-white hover:bg-white/10 p-2 rounded-xl transition-all duration-300 backdrop-blur-sm"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {isMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-2 bg-gradient-to-r from-slate-800/95 to-blue-900/95 backdrop-blur-lg rounded-2xl mt-2 border border-white/10 shadow-2xl">
              <a
                href="/"
                className="text-white/90 hover:text-white hover:bg-white/10 block px-4 py-3 rounded-xl transition-all duration-300 font-medium"
                onClick={() => setIsMenuOpen(false)}
              >
                <span className="flex items-center space-x-2">
                  <span>🏠</span>
                  <span>Home</span>
                </span>
              </a>
              
              {user ? (
                <>
                  <div className="flex items-center space-x-3 px-4 py-3 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-xl border border-blue-400/20">
                    <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-bold">
                        {user.email?.charAt(0).toUpperCase()}
                      </span>
                    </div>
                    <span className="text-white/90 text-sm font-medium">
                      Hello, {user.email?.split('@')[0]}
                    </span>
                  </div>
                  <button
                    onClick={handleSignOut}
                    className="w-full text-left bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white px-4 py-3 rounded-xl transition-all duration-300 font-medium shadow-lg"
                  >
                    <span className="flex items-center space-x-2">
                      <span>🚪</span>
                      <span>Sign Out</span>
                    </span>
                  </button>
                </>
              ) : (
                <>
                  <a
                    href="/signin"
                    className="text-white/90 hover:text-white hover:bg-white/10 block px-4 py-3 rounded-xl transition-all duration-300 font-medium"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <span className="flex items-center space-x-2">
                      <span>🔑</span>
                      <span>Sign In</span>
                    </span>
                  </a>
                  <a
                    href="/signup"
                    className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white block px-4 py-3 rounded-xl transition-all duration-300 font-medium shadow-lg"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <span className="flex items-center space-x-2">
                      <span>✨</span>
                      <span>Sign Up</span>
                    </span>
                  </a>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}