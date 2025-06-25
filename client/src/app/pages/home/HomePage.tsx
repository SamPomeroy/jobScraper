"use client";
import { Search, FileText, Bell } from "lucide-react";
import { AuthUser } from "@supabase/supabase-js";
import { useTheme } from '@/app/context/ThemeContext';

interface HomePageProps {
  user: import("@/app/types/auth").AuthUser | null;
  setCurrentPageAction: (page: string) => void;
}

export default function HomePage({
  user,
  setCurrentPageAction,
}: {
  user: AuthUser | null;
  setCurrentPageAction: (page: string) => void;
}) {
  const { darkMode } = useTheme();

  return (
    <div
      style={{
        backgroundColor: "var(--bg-color)",
        color: "var(--text-color)",
      }}
      className="min-h-screen transition-colors duration-200"
    >
      {/* Hero Section */}
      <div 
        style={{
          backgroundColor: 'var(--bg-color)',
          color: 'var(--text-color)'
        }}
        className="transition-colors duration-200"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 
              className={`text-4xl font-extrabold sm:text-5xl md:text-6xl transition-colors duration-200 ${
                darkMode ? 'text-gray-100' : 'text-gray-900'
              }`}
            >
              Track Your Job Applications
            </h1>
            <p 
              className={`mt-3 max-w-md mx-auto text-base sm:text-lg md:mt-5 md:text-xl md:max-w-3xl transition-colors duration-200 ${
                darkMode ? 'text-gray-400' : 'text-gray-500'
              }`}
            >
              Stay organized and never miss an opportunity. Our job tracking
              system helps you manage applications, follow up on prospects, and
              land your dream job
            </p>
            <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
              {user ? (
                <button
                  onClick={() => setCurrentPageAction("dashboard")}
                  className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors duration-200"
                >
                  Go to Dashboard
                </button>
              ) : (
                <div className="space-y-3 sm:space-y-0 sm:space-x-3 sm:flex">
                  <button
                    onClick={() => setCurrentPageAction("register")}
                    className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-colors duration-200"
                  >
                    Get Started
                  </button>
                  <button
                    onClick={() => setCurrentPageAction("login")}
                    className={`w-full flex items-center justify-center px-8 py-3 border text-base font-medium rounded-md md:py-4 md:text-lg md:px-10 transition-colors duration-200 ${
                      darkMode
                        ? 'border-blue-400 text-blue-400 bg-transparent hover:bg-blue-900/20'
                        : 'border-blue-600 text-blue-600 bg-white hover:bg-blue-50'
                    }`}
                  >
                    Sign In
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div 
        className={`py-16 transition-colors duration-200 ${
          darkMode ? 'bg-gray-800' : 'bg-gray-50'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 
              className={`text-3xl font-extrabold transition-colors duration-200 ${
                darkMode ? 'text-gray-100' : 'text-gray-900'
              }`}
            >
              Everything you need to manage your job search
            </h2>
          </div>
          <div className="mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            <div className="text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white mx-auto">
                <Search className="h-6 w-6" />
              </div>
              <h3 
                className={`mt-6 text-lg font-medium transition-colors duration-200 ${
                  darkMode ? 'text-gray-200' : 'text-gray-900'
                }`}
              >
                Updated Daily
              </h3>
              <p 
                className={`mt-2 text-base transition-colors duration-200 ${
                  darkMode ? 'text-gray-400' : 'text-gray-500'
                }`}
              >
                Automatically find and track job opportunities from multiple
                sources.
              </p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-green-500 text-white mx-auto">
                <FileText className="h-6 w-6" />
              </div>
              <h3 
                className={`mt-6 text-lg font-medium transition-colors duration-200 ${
                  darkMode ? 'text-gray-200' : 'text-gray-900'
                }`}
              >
                Resume Management
              </h3>
              <p 
                className={`mt-2 text-base transition-colors duration-200 ${
                  darkMode ? 'text-gray-400' : 'text-gray-500'
                }`}
              >
                Store and manage multiple versions of your resume for different
                positions.
              </p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center h-12 w-12 rounded-md bg-purple-500 text-white mx-auto">
                <Bell className="h-6 w-6" />
              </div>
              <h3 
                className={`mt-6 text-lg font-medium transition-colors duration-200 ${
                  darkMode ? 'text-gray-200' : 'text-gray-900'
                }`}
              >
                Application Tracking
              </h3>
              <p 
                className={`mt-2 text-base transition-colors duration-200 ${
                  darkMode ? 'text-gray-400' : 'text-gray-500'
                }`}
              >
                Keep track of your applications and follow up at the right time.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
