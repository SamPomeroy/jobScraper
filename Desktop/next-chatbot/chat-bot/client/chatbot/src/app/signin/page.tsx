'use client';

import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';
import { getUser, signIn } from '../api/auth/auth';
import type { User } from '@supabase/supabase-js';

// Initialize Supabase - replace with your actual credentials
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || "YOUR_SUPABASE_URL",
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || "YOUR_SUPABASE_ANON_KEY"
);

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [authLoading, setAuthLoading] = useState(true);
  
  // Guest mode state
  const [guestLoading, setGuestLoading] = useState(false);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error) {
          console.warn('Auth session error:', error);
        }
        
        // If user has valid session, redirect to their chat page
        if (session?.user) {
          window.location.replace(`/chats/${session.user.id}`);
          return;
        }
      } catch (err) {
        console.error('Error checking auth:', err);
      } finally {
        setAuthLoading(false);
      }
    };

    checkAuth();
  }, []);

  const handleSignIn = async (e?: React.FormEvent) => {
    e?.preventDefault();
    
    if (isLoading) return;
    
    setError(null);
    setIsLoading(true);

    // Basic validation
    if (!email.trim() || !password.trim()) {
      setError('Please enter both email and password');
      setIsLoading(false);
      return;
    }

    try {
      const response = await signIn(email.trim().toLowerCase(), password);

      if (!response?.user || !response?.session) {
        setError('Invalid credentials. Please check your email and password.');
        return;
      }

      const { user, session } = response;
      
      // Store session token for API calls if needed
      if (typeof window !== 'undefined') {
        sessionStorage.setItem('sb-access-token', session.access_token);
      }
      
      // Redirect to user's chat page
      window.location.replace(`/chats/${user.id}`);
      
    } catch (err: any) {
      console.error('Sign-in error:', err);
      
      let errorMessage = 'An error occurred during sign-in. Please try again.';
      
      if (err?.message) {
        if (err.message.includes('rate limit')) {
          errorMessage = 'Too many sign-in attempts. Please wait a few minutes and try again.';
        } else if (err.message.includes('Invalid login credentials')) {
          errorMessage = 'Invalid email or password. Please check your credentials.';
        } else if (err.message.includes('Email not confirmed')) {
          errorMessage = 'Please check your email and confirm your account before signing in.';
        }
      }
      
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Enhanced guest access with better UX
  const handleGuestAccess = async () => {
    setGuestLoading(true);
    setError(null);
    
    try {
      // Clear any existing auth data
      if (typeof window !== 'undefined') {
        sessionStorage.removeItem('sb-access-token');
        localStorage.setItem('guest-mode', 'true');
        localStorage.setItem('guest-session-start', new Date().toISOString());
      }
      
      // Small delay for better UX
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Redirect to guest chat
      window.location.replace('/chats/guest');
      
    } catch (err) {
      console.error('Guest access error:', err);
      setError('Failed to start guest session. Please try again.');
    } finally {
      setGuestLoading(false);
    }
  };

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
        <div className="flex items-center space-x-3 text-white">
          <div className="w-8 h-8 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          <span className="text-lg">Checking authentication...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900">
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -right-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -left-1/2 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-indigo-500/5 rounded-full blur-2xl animate-pulse delay-500"></div>
      </div>

      {/* Main Card */}
      <div className="relative bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 w-full max-w-md border border-white/20">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
            <span className="text-2xl">🎤</span>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-2">
            Welcome Back
          </h1>
          <p className="text-slate-600">Sign in to access your voice learning assistant</p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 shadow-sm">
            <div className="flex items-center">
              <span className="mr-2">⚠️</span>
              <p className="text-sm font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Sign In Form */}
        <form onSubmit={handleSignIn} className="space-y-6">
          {/* Email Input */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 pl-11 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
                required
                disabled={isLoading || guestLoading}
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                📧
              </span>
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 pl-11 pr-11 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
                required
                disabled={isLoading || guestLoading}
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                🔒
              </span>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors duration-200"
                disabled={isLoading || guestLoading}
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
          </div>

          {/* Sign In Button */}
          <button
            type="submit"
            disabled={isLoading || guestLoading || !email.trim() || !password.trim()}
            className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-slate-400 disabled:to-slate-500 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:hover:scale-100 shadow-lg hover:shadow-blue-500/25 disabled:shadow-none"
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Signing In...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2">
                <span>🚀</span>
                <span>Sign In</span>
              </div>
            )}
          </button>
        </form>

        {/* Divider */}
        <div className="mt-6">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-slate-300"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-white text-slate-500">or</span>
            </div>
          </div>
        </div>
        
        {/* Guest Access Button */}
        <button
          onClick={handleGuestAccess}
          disabled={isLoading || guestLoading}
          className="mt-4 w-full bg-gradient-to-r from-slate-600 to-slate-700 hover:from-slate-700 hover:to-slate-800 disabled:from-slate-400 disabled:to-slate-500 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:hover:scale-100 shadow-lg hover:shadow-slate-500/25"
        >
          {guestLoading ? (
            <div className="flex items-center justify-center space-x-2">
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Starting Guest Session...</span>
            </div>
          ) : (
            <div className="flex items-center justify-center space-x-2">
              <span>🎤</span>
              <span>Continue as Guest (Voice Chat)</span>
            </div>
          )}
        </button>

        {/* Guest Mode Info */}
        <div className="mt-3 text-center">
          <p className="text-xs text-slate-500">
            Guest mode provides full voice chat functionality without requiring an account
          </p>
        </div>

        {/* Footer Links */}
        <div className="mt-8 text-center space-y-2">
          <p className="text-slate-600">
            Don't have an account?{' '}
            <a 
              href="/signup" 
              className="text-blue-500 hover:text-blue-600 transition-colors font-medium"
            >
              Sign Up
            </a>
          </p>
          <p className="text-slate-500 text-sm">
            <a 
              href="/forgot-password" 
              className="hover:text-slate-700 transition-colors"
            >
              Forgot your password?
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}