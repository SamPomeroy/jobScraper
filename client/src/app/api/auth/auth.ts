"use client";

import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";
import type { Session, User } from "@supabase/supabase-js"; // ✅ Import needed types

export const supabase = createClientComponentClient();

// ✅ Sign In
export async function signIn(
  email: string,
  password: string
): Promise<{ user: User | null; session: Session | null } | null> {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    console.error("Login error:", error.message);
    return null;
  }

  const accessToken = data?.session?.access_token;
  if (accessToken) {
    localStorage.setItem("sb-access-token", accessToken);
  }

  return {
    user: data.user,
    session: data.session,
  };
}

// ✅ Sign Up
export async function signUp(
  email: string,
  password: string
): Promise<User | null> {
  const { data, error } = await supabase.auth.signUp({ email, password });

  if (error) {
    console.error("Signup error:", error.message);
    return null;
  }

  const accessToken = data?.session?.access_token;
  if (accessToken) {
    localStorage.setItem("sb-access-token", accessToken);
  }

  return data.user;
}

// ✅ Sign Out
export async function signOut(): Promise<void> {
  const { error } = await supabase.auth.signOut();
  if (error) console.error("Logout error:", error.message);
}

// ✅ Get Logged-In User from Session
export async function getUser(): Promise<User | null> {

  const {
    data: { session },
    error: sessionError,
  } = await supabase.auth.getSession();

  if (sessionError) {
    console.error("Error getting session:", sessionError.message);
    return null;
  }

  if (!session) {
    console.warn("No active session");
    return null;
  }

  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError) {
    console.error("Error fetching user:", userError.message);
    return null;
  }

  return user;
}
// ✅ Google Sign-In
export async function signInWithGoogle(): Promise<void> {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider: 'google',
  });

  if (error) {
    console.error('Google login error:', error.message);
  } else {
    // Redirection will handle the rest; no need to manually grab tokens here
    console.log('Redirecting to Google for login...');
  }
}