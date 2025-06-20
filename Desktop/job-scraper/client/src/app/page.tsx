

// src/app/page.tsx
import { getUserServer } from '@/app/supabase/user';
import AppShell from '@/app/components/AppShell';
import { createClient } from '@supabase/supabase-js';
import type { AuthUser } from '@/app/types/auth';


export default async function Page() {
  const user = await getUserServer();
  return <AppShell initialUser={user as AuthUser | null} />;
}  



const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

















// 'use client'
// import React, { useState, useEffect } from 'react';
// import { Upload, FileText, Settings, Bell, Search, User, LogOut, Eye, Trash2, Plus } from 'lucide-react';
// import { getUserServer } from '@/app/supabase/user';
// import type { AuthUser } from '@/app/types/auth';
// import '../app/globals.css'
// import { createClient } from '@supabase/supabase-js';
// import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
// import { cookies } from 'next/headers';





// if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
//   throw new Error('Supabase environment variables are not set.');
// }

// export default async function App() {
//   const supabase = createServerComponentClient({ cookies });
//   const {
//     data: { user }
//   } = await supabase.auth.getUser();
//   const [currentPage, setCurrentPage] = useState('home');
//   const [loading, setLoading] = useState(true);
  
//   const user = await getUserServer(); 
//   const supabase = createClient(
//     process.env.NEXT_PUBLIC_SUPABASE_URL as string,
//     process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string
//   );
//   // Check for existing session on mount
//   useEffect(() => {
//     const checkSession = async () => {
//       const { data: { session }, error } = await supabase.auth.getSession();
//       if (error) {
//         console.error('Error checking session:', error);
//       } else if (session?.user) {
//         setUser(session.user as AuthUser);
//         setCurrentPage('dashboard');
//       }
//       setLoading(false);
//     };

//     checkSession();

//     // Listen for auth state changes
//     const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
//       if (event === 'SIGNED_IN' && session?.user) {
//         setUser(session.user as AuthUser);
//         setCurrentPage('dashboard');
//       } else if (event === 'SIGNED_OUT') {
//         setUser(null);
//         setCurrentPage('home');
//       }
//     });

//     return () => subscription.unsubscribe();
//   }, []);

//   const handleLogout = async () => {
//     await supabase.auth.signOut();
//   };

//   const handleAuthSuccess = (authUser: AuthUser) => {
//     setUser(authUser);
//     setCurrentPage('dashboard');
//   };

//   if (loading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gray-50">
//         <div className="text-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
//           <p className="mt-4 text-gray-600">Loading...</p>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gray-50">
//       <Navbar 
//         user={user} 
//         onLogout={handleLogout} 
//         currentPage={currentPage} 
//         setCurrentPage={setCurrentPage} 
//       />
      
//       <main className="flex-1">
//         {currentPage === 'home' && <HomePage user={user} setCurrentPage={setCurrentPage} />}
//         {currentPage === 'about' && <AboutPage />}
//         {currentPage === 'contact' && <ContactPage />}
//         {currentPage === 'login' && (
//           <AuthForm 
//             mode="login" 
//             onSuccess={handleAuthSuccess} 
//             setCurrentPage={setCurrentPage} 
//           />
//         )}
//         {currentPage === 'register' && (
//           <AuthForm 
//             mode="register" 
//             onSuccess={handleAuthSuccess} 
//             setCurrentPage={setCurrentPage} 
//           />
//         )}
//         {currentPage === 'dashboard' && user && <Dashboard user={user} />}
//       </main>
      
//       <Footer setCurrentPage={setCurrentPage} />
//     </div>
//   );
// }
