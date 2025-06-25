'use client';

import { Search, User, LogOut, Home, Mail, Info, Shield } from 'lucide-react';
import { Switch } from '@headlessui/react';
import { useTheme } from '@/app/context/ThemeContext';

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
  onLogoutAction: () => void;
  currentPage: string;
  setCurrentPageAction: (page: string) => void;
}

export default function Navbar({
  user,
  onLogoutAction,
  currentPage,
  setCurrentPageAction,
}: NavbarProps) {
  const { darkMode, toggleDarkMode } = useTheme();

  return (
    <nav
      style={{
        backgroundColor: 'var(--bg-color)',
        color: 'var(--text-color)',
        width: '100%', 
      }}
      
      className={`shadow-lg border-b transition-colors duration-200 w-full ${
        darkMode ? 'border-gray-600' : 'border-gray-200'
      }`}
    >
      <div className="max-w-7xl  mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold text-blue-600">JobTracker</h1>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button
                onClick={() => setCurrentPageAction('home')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  currentPage === 'home'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                    : darkMode
                    ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Home className="w-4 h-4 inline mr-2" />
                Home
              </button>
              <button
                onClick={() => setCurrentPageAction('about')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  currentPage === 'about'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                    : darkMode
                    ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Info className="w-4 h-4 inline mr-2" />
                About
              </button>
              <button
                onClick={() => setCurrentPageAction('contact')}
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                  currentPage === 'contact'
                    ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                    : darkMode
                    ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                }`}
              >
                <Mail className="w-4 h-4 inline mr-2" />
                Contact
              </button>
              {user && (
                <button
                  onClick={() => setCurrentPageAction('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    currentPage === 'dashboard'
                      ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
                      : darkMode
                      ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Search className="w-4 h-4 inline mr-2" />
                  Dashboard
                </button>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
              Dark Mode
            </span>
            <div className="flex items-center">
              <Switch
                checked={darkMode}
                onChange={toggleDarkMode}
                className={`${
                  darkMode ? 'bg-blue-600' : 'bg-gray-300'
                } relative inline-flex h-6 w-11 items-center rounded-full transition-colors`}
              >
                <span className="sr-only">Toggle Dark Mode</span>
                <span
                  className={`${
                    darkMode ? 'translate-x-6' : 'translate-x-1'
                  } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
                />
              </Switch>
            </div>

            {user ? (
              <>
                <div className="flex items-center space-x-2">
                  <User className={`w-5 h-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
                  <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
                    {user.user_metadata?.full_name || user.email}
                  </span>
                  {user.user_metadata?.role === 'admin' && (
                    <Shield className="w-4 h-4 text-red-500" role="Admin" />
                  )}
                </div>
                <button
                  onClick={onLogoutAction}
                  className={`flex items-center space-x-1 px-3 py-2 text-sm rounded-md transition-colors duration-200 ${
                    darkMode
                      ? 'text-red-400 hover:text-red-300 hover:bg-red-900/20'
                      : 'text-red-600 hover:text-red-800 hover:bg-red-50'
                  }`}
                >
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setCurrentPageAction('login')}
                  className={`px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
                    currentPage === 'login'
                      ? 'bg-blue-600 text-white'
                      : darkMode
                      ? 'text-blue-400 hover:text-blue-300'
                      : 'text-blue-600 hover:text-blue-800'
                  }`}
                >
                  Login
                </button>
                <button
                  onClick={() => setCurrentPageAction('register')}
                  className={`px-4 py-2 text-sm font-medium rounded-md border transition-colors duration-200 ${
                    currentPage === 'register'
                      ? 'border-blue-600 bg-blue-600 text-white'
                      : darkMode
                      ? 'border-blue-400 text-blue-400 hover:bg-blue-900/20'
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











// 'use client';

// import { Search, User, LogOut, Home, Mail, Info, Shield } from 'lucide-react';
// import { Switch } from '@headlessui/react';
// import { useTheme } from '@/app/context/ThemeContext';

// interface AuthUser {
//   id: string;
//   email?: string;
//   user_metadata?: {
//     role?: 'user' | 'admin';
//     full_name?: string;
//   };
// }

// interface NavbarProps {
//   user: AuthUser | null;
//   onLogout: () => void;
//   currentPage: string;
//   setCurrentPage: (page: string) => void;
// }

// export default function Navbar({
//   user,
//   onLogout,
//   currentPage,
//   setCurrentPage,
// }: NavbarProps) {
//   const { darkMode, toggleDarkMode } = useTheme();

//   return (
//     <nav 
//       style={{
//         backgroundColor: 'var(--bg-color)',
//         color: 'var(--text-color)'
//        }}
//        className={`shadow-lg border-b transition-colors duration-200 w-full ${
//         darkMode ? 'border-gray-600' : 'border-gray-200'
//       }`}
//     >
//      <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex justify-between items-center h-16">
//           {/* Logo */}
//           <div className="flex items-center">
//             <div className="flex-shrink-0">
//               <h1 className="text-xl font-bold text-blue-600">JobTracker</h1>
//             </div>
//           </div>

//           {/* Navigation Links */}
//           <div className="hidden md:block">
//             <div className="ml-10 flex items-baseline space-x-4">
//               <button
//                 onClick={() => setCurrentPage('home')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
//                   currentPage === 'home'
//                     ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
//                     : darkMode
//                     ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Home className="w-4 h-4 inline mr-2" />
//                 Home
//               </button>
//               <button
//                 onClick={() => setCurrentPage('about')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
//                   currentPage === 'about'
//                     ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
//                     : darkMode
//                     ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Info className="w-4 h-4 inline mr-2" />
//                 About
//               </button>
//               <button
//                 onClick={() => setCurrentPage('contact')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
//                   currentPage === 'contact'
//                     ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
//                     : darkMode
//                     ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Mail className="w-4 h-4 inline mr-2" />
//                 Contact
//               </button>
//               {user && (
//                 <button
//                   onClick={() => setCurrentPage('dashboard')}
//                   className={`px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
//                     currentPage === 'dashboard'
//                       ? 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300'
//                       : darkMode
//                       ? 'text-gray-300 hover:text-gray-100 hover:bg-gray-700'
//                       : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                   }`}
//                 >
//                   <Search className="w-4 h-4 inline mr-2" />
//                   Dashboard
//                 </button>
//               )}
//             </div>
//           </div>

//           <div className="flex items-center space-x-4">
//             <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>
//               Dark Mode
//             </span>
//             <div className="flex items-center">
//               <Switch
//                 checked={darkMode}
//                 onChange={toggleDarkMode}
//                 className={`${
//                   darkMode ? 'bg-blue-600' : 'bg-gray-300'
//                 } relative inline-flex h-6 w-11 items-center rounded-full transition-colors`}
//               >
//                 <span className="sr-only">Toggle Dark Mode</span>
//                 <span
//                   className={`${
//                     darkMode ? 'translate-x-6' : 'translate-x-1'
//                   } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
//                 />
//               </Switch>
//             </div>

//             {user ? (
//               <>
//                 <div className="flex items-center space-x-2">
//                   <User className={`w-5 h-5 ${darkMode ? 'text-gray-400' : 'text-gray-500'}`} />
//                   <span className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>
//                     {user.user_metadata?.full_name || user.email}
//                   </span>
//                   {user.user_metadata?.role === 'admin' && (
//                     <Shield className="w-4 h-4 text-red-500" role="Admin" />
//                   )}
//                 </div>
//                 <button
//                   onClick={onLogout}
//                   className={`flex items-center space-x-1 px-3 py-2 text-sm rounded-md transition-colors duration-200 ${
//                     darkMode
//                       ? 'text-red-400 hover:text-red-300 hover:bg-red-900/20'
//                       : 'text-red-600 hover:text-red-800 hover:bg-red-50'
//                   }`}
//                 >
//                   <LogOut className="w-4 h-4" />
//                   <span>Logout</span>
//                 </button>
//               </>
//             ) : (
//               <div className="flex items-center space-x-2">
//                 <button
//                   onClick={() => setCurrentPage('login')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md transition-colors duration-200 ${
//                     currentPage === 'login'
//                       ? 'bg-blue-600 text-white'
//                       : darkMode
//                       ? 'text-blue-400 hover:text-blue-300'
//                       : 'text-blue-600 hover:text-blue-800'
//                   }`}
//                 >
//                   Login
//                 </button>
//                 <button
//                   onClick={() => setCurrentPage('register')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md border transition-colors duration-200 ${
//                     currentPage === 'register'
//                       ? 'border-blue-600 bg-blue-600 text-white'
//                       : darkMode
//                       ? 'border-blue-400 text-blue-400 hover:bg-blue-900/20'
//                       : 'border-blue-600 text-blue-600 hover:bg-blue-50'
//                   }`}
//                 >
//                   Register
//                 </button>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </nav>
//   );
// }





// 'use client';

// import { Search, User, LogOut, Home, Mail, Info, Shield } from 'lucide-react';
// import { Switch } from '@headlessui/react';
// import { useTheme } from '@/app/context/ThemeContext';

// interface AuthUser {
//   id: string;
//   email?: string;
//   user_metadata?: {
//     role?: 'user' | 'admin';
//     full_name?: string;
//   };
// }

// interface NavbarProps {
//   user: AuthUser | null;
//   onLogout: () => void;
//   currentPage: string;
//   setCurrentPage: (page: string) => void;
// }

// export default function Navbar({
//   user,
//   onLogout,
//   currentPage,
//   setCurrentPage,
// }: NavbarProps) {
//   const { darkMode, toggleDarkMode } = useTheme();

//   return (
//     <nav className="bg-white shadow-lg border-b">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex justify-between items-center h-16">
//           {/* Logo */}
//           <div className="flex items-center">
//             <div className="flex-shrink-0">
//               <h1 className="text-xl font-bold text-blue-600">JobTracker</h1>
//             </div>
//           </div>

//           {/* Navigation Links */}
//           <div className="hidden md:block">
//             <div className="ml-10 flex items-baseline space-x-4">
//               <button
//                 onClick={() => setCurrentPage('home')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'home'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Home className="w-4 h-4 inline mr-2" />
//                 Home
//               </button>
//               <button
//                 onClick={() => setCurrentPage('about')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'about'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Info className="w-4 h-4 inline mr-2" />
//                 About
//               </button>
//               <button
//                 onClick={() => setCurrentPage('contact')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'contact'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Mail className="w-4 h-4 inline mr-2" />
//                 Contact
//               </button>
//               {user && (
//                 <button
//                   onClick={() => setCurrentPage('dashboard')}
//                   className={`px-3 py-2 rounded-md text-sm font-medium ${
//                     currentPage === 'dashboard'
//                       ? 'bg-blue-100 text-blue-700'
//                       : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                   }`}
//                 >
//                   <Search className="w-4 h-4 inline mr-2" />
//                   Dashboard
//                 </button>
//               )}
//             </div>
//           </div>

        
//           <div className="flex items-center space-x-4">
//             DarkMode
//             <div className="flex items-center">
//               <Switch
//                 checked={darkMode}
//                 onChange={toggleDarkMode}
//                 className={`${
//                   darkMode ? 'bg-blue-600' : 'bg-gray-300'
//                 } relative inline-flex h-6 w-11 items-center rounded-full transition-colors`}
//               >
//                 <span className="sr-only">Toggle Dark Mode</span>
//                 <span
//                   className={`${
//                     darkMode ? 'translate-x-6' : 'translate-x-1'
//                   } inline-block h-4 w-4 transform rounded-full bg-white transition-transform`}
//                 />
//               </Switch>
//             </div>

           
//             {user ? (
//               <>
//                 <div className="flex items-center space-x-2">
//                   <User className="w-5 h-5 text-gray-500" />
//                   <span className="text-sm text-gray-700">
//                     {user.user_metadata?.full_name || user.email}
//                   </span>
//                   {user.user_metadata?.role === 'admin' && (
//                     <Shield className="w-4 h-4 text-red-500" role="Admin" />
//                   )}
//                 </div>
//                 <button
//                   onClick={onLogout}
//                   className="flex items-center space-x-1 px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md"
//                 >
//                   <LogOut className="w-4 h-4" />
//                   <span>Logout</span>
//                 </button>
//               </>
//             ) : (
//               <div className="flex items-center space-x-2">
//                 <button
//                   onClick={() => setCurrentPage('login')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md ${
//                     currentPage === 'login'
//                       ? 'bg-blue-600 text-white'
//                       : 'text-blue-600 hover:text-blue-800'
//                   }`}
//                 >
//                   Login
//                 </button>
//                 <button
//                   onClick={() => setCurrentPage('register')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md border ${
//                     currentPage === 'register'
//                       ? 'border-blue-600 bg-blue-600 text-white'
//                       : 'border-blue-600 text-blue-600 hover:bg-blue-50'
//                   }`}
//                 >
//                   Register
//                 </button>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </nav>
//   );
// }


// 'use client'



// import { Search, User, LogOut, Home, Mail, Info, Shield } from 'lucide-react';


// interface AuthUser {
//   id: string;
//   email?: string;
//   user_metadata?: {
//     role?: 'user' | 'admin';
//     full_name?: string;
//   };
// }


// interface NavbarProps {
//   user: AuthUser | null;
//   onLogout: () => void;
//   currentPage: string;
//   setCurrentPage: (page: string) => void;
// }

// export default function Navbar({ user, onLogout, currentPage, setCurrentPage }: NavbarProps) {
//   return (
//     <nav className="bg-white shadow-lg border-b">
//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="flex justify-between items-center h-16">
    
//           <div className="flex items-center">
//             <div className="flex-shrink-0">
//               <h1 className="text-xl font-bold text-blue-600">JobTracker</h1>
//             </div>
//           </div>

     
//           <div className="hidden md:block">
//             <div className="ml-10 flex items-baseline space-x-4">
//               <button
//                 onClick={() => setCurrentPage('home')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'home'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Home className="w-4 h-4 inline mr-2" />
//                 Home
//               </button>
              
//               <button
//                 onClick={() => setCurrentPage('about')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'about'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Info className="w-4 h-4 inline mr-2" />
//                 About
//               </button>

//               <button
//                 onClick={() => setCurrentPage('contact')}
//                 className={`px-3 py-2 rounded-md text-sm font-medium ${
//                   currentPage === 'contact'
//                     ? 'bg-blue-100 text-blue-700'
//                     : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                 }`}
//               >
//                 <Mail className="w-4 h-4 inline mr-2" />
//                 Contact
//               </button>

//               {user && (
//                 <button
//                   onClick={() => setCurrentPage('dashboard')}
//                   className={`px-3 py-2 rounded-md text-sm font-medium ${
//                     currentPage === 'dashboard'
//                       ? 'bg-blue-100 text-blue-700'
//                       : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
//                   }`}
//                 >
//                   <Search className="w-4 h-4 inline mr-2" />
//                   Dashboard
//                 </button>
//               )}
//             </div>
//           </div>

//           {/* User Menu */}
//           <div className="flex items-center space-x-4">
//             {user ? (
//               <>
//                 <div className="flex items-center space-x-2">
//                   <User className="w-5 h-5 text-gray-500" />
//                   <span className="text-sm text-gray-700">
//                     {user.user_metadata?.full_name || user.email}
//                   </span>
//                   {user.user_metadata?.role === 'admin' && (
//                     <Shield className="w-4 h-4 text-red-500" role="Admin" />
//                   )}
//                 </div>
//                 <button
//                   onClick={onLogout}
//                   className="flex items-center space-x-1 px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-md"
//                 >
//                   <LogOut className="w-4 h-4" />
//                   <span>Logout</span>
//                 </button>
//               </>
//             ) : (
//               <div className="flex items-center space-x-2">
//                 <button
//                   onClick={() => setCurrentPage('login')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md ${
//                     currentPage === 'login'
//                       ? 'bg-blue-600 text-white'
//                       : 'text-blue-600 hover:text-blue-800'
//                   }`}
//                 >
//                   Login
//                 </button>
//                 <button
//                   onClick={() => setCurrentPage('register')}
//                   className={`px-4 py-2 text-sm font-medium rounded-md border ${
//                     currentPage === 'register'
//                       ? 'border-blue-600 bg-blue-600 text-white'
//                       : 'border-blue-600 text-blue-600 hover:bg-blue-50'
//                   }`}
//                 >
//                   Register
//                 </button>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </nav>
//   );
// }


