'use-client'
import './globals.css'
import React, {useEffect} from 'react';

import { createClient } from './supabase/server'
import { Search, FileText, Bell } from 'lucide-react';
import { Inter } from "next/font/google";
interface DashboardProps {
  activeTab: string;
}
const inter = Inter({ subsets: ["latin"] });
export default async function RootLayout({ children }: { children: React.ReactNode }) {
 
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
 
  const userId = user?.id; 
 useEffect(() => {
  if (settings.darkMode) {
    document.documentElement.classList.add("dark");
  } else {
    document.documentElement.classList.remove("dark");
  }
}, [settings.darkMode]);

  return (
   <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} flex`} suppressHydrationWarning>
   
        <div className="flex-grow">
      
          {children}
        </div>
      </body>
    </html>
  );
}
