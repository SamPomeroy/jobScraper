"use client";

import React, { useState, useEffect } from "react";

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

export default function AppShell({
  initialUser,
}: {
  initialUser: AuthUser | null;
}) {
  const [user, setUser] = useState<AuthUser | null>(initialUser);
  const [currentPage, setCurrentPage] = useState("home");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      const {
        data: { session },
        error,
      } = await supabase.auth.getSession();
      if (error) console.error("Session error:", error);
      else if (session?.user) {
        setUser(session.user as AuthUser);
        setCurrentPage("dashboard");
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
      } else if (event === "SIGNED_OUT") {
        setUser(null);
        setCurrentPage("home");
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  const handleAuthSuccess = (authUser: AuthUser) => {
    setUser(authUser);
    setCurrentPage("dashboard");
  };
const handleJobUpdate = (jobId: string, update: Partial<import("@/app/types/jobs").Job>) => {
  // Optionally: send update to backend or show notification
};

const handleApplyStatusChange = (jobId: string, applied: boolean) => {
  // Optionally: send update to backend or show notification
};
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Loading...
      </div>
    );
  }

  return (
    <div className="max-w-6xl  mx-auto bg-gray-50 dark:bg-gray-900 dark:text-gray-100">
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
    <Dashboard
      user={user}
    />
  )}
      </main>
      <Footer setCurrentPage={setCurrentPage} />
    </div>
  );
}

