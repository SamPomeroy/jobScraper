import { createClient } from "@/utils/supabase/server";
import SidebarWrapper from "./components/SidebarWrapper"; 
import Navbar from "./components/Navbar";
import { Metadata } from "next";
import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Learning Assistant Chatbot",
  description: "AI-powered learning assistant to help you learn anything",
};

export default async function Layout({ children }: { children: React.ReactNode }) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  const userId = user?.id; // ✅ Define userId properly

  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} flex`} suppressHydrationWarning>
        {userId && <SidebarWrapper userId={userId} />}
        <div className="flex-grow">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
