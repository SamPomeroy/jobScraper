// layout.tsx (server component)
import './globals.css';
import { Inter } from 'next/font/google';
import { createClient } from './supabase/server';
import ThemeChange from '../app/components/ThemeChange'; // 👈 client component
import { cookies } from 'next/headers';
import React from 'react';
import { Switch } from '@headlessui/react';
import { ThemeProvider } from'./context/ThemeContext'


type SettingsState = {
  darkMode: boolean;
  notifications: boolean;
  emailAlerts: boolean;
  soundAlerts: boolean;
  autoSave: boolean;
  defaultCategory: string;
  jobAlertFrequency: string;
};

const inter = Inter({ subsets: ['latin'] });

export default async function RootLayout({ children }: { children: React.ReactNode }) {
const cookieStore = cookies(); // no need to await
const supabase = createClient();

  // const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} flex`} suppressHydrationWarning>
        <ThemeChange /> {/* 👈 handles dark mode */}
       <ThemeProvider>
          {children}
        </ThemeProvider>

      </body>
    </html>
  );
}