import { supabase } from './client';
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
// For client components (hooks, useEffect, etc.)
export async function getUserClient() {
  const { data, error } = await supabase.auth.getUser();
  if (error) {
    console.error('Client-side user fetch error:', error);
    return undefined;
  }
  return data.user;
}

// For server components and routes
export async function getUserServer() {
  const supabase = createServerComponentClient({ cookies });
  const { data, error } = await supabase.auth.getUser();
  if (error) {
    console.error('Server-side user fetch error:', error);
    return null;
  }
  return data.user;
}