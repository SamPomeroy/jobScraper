'use client'



import { Search, User, LogOut, Home, Mail, Info, Shield } from 'lucide-react';


interface AuthUser {
  id: string;
  email?: string;
  user_metadata?: {
    role?: 'user' | 'admin';
    full_name?: string;
  };
}


interface NavbarProps {
  user: AuthUser | null;
  onLogout: () => void;
  currentPage: string;
  setCurrentPage: (page: string) => void;
}

export default function Navbar({ user, onLogout, currentPage, setCurrentPage }: NavbarProps) {
  return (
    <nav className="bg-white shadow-lg border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
    
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-blue-600">JobTracker</h1>
            </div>
          </div>

     
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button
                onClick={() => setCurrentPage('home')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentPage === 'home'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Home className="w-4 h-4 inline mr-2" />
                Home
              </button>
              
              <button
                onClick={() => setCurrentPage('about')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentPage === 'about'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Info className="w-4 h-4 inline mr-2" />
                About
              </button>

              <button
                onClick={() => setCurrentPage('contact')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${
                  currentPage === 'contact'
                    ? 'bg-blue-100 text-blue-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Mail className="w-4 h-4 inline mr-2" />
                Contact
              </button>

              {user && (
                <button
                  onClick={() => setCurrentPage('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    currentPage === 'dashboard'
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Search className="w-4 h-4 inline mr-2" />
                  Dashboard
                </button>
              )}
            </div>
          </div>

          {/* User Menu */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <div className="flex items-center space-x-2">
                  <User className="w-5 h-5 text-gray-500" />
                  <span className="text-sm text-gray-700">
                    {user.user_metadata?.full_name || user.email}
                  </span>
                  {user.user_metadata?.role === 'admin' && (
                    <Shield className="w-4 h-4 text-red-500" role="Admin" />
                  )}
                </div>
                <button
                  onClick={onLogout}
                  className="flex items-center space-x-1 px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setCurrentPage('login')}
                  className={`px-4 py-2 text-sm font-medium rounded-md ${
                    currentPage === 'login'
                      ? 'bg-blue-600 text-white'
                      : 'text-blue-600 hover:text-blue-800'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => setCurrentPage('register')}
                  className={`px-4 py-2 text-sm font-medium rounded-md border ${
                    currentPage === 'register'
                      ? 'border-blue-600 bg-blue-600 text-white'
                      : 'border-blue-600 text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  Register
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}


