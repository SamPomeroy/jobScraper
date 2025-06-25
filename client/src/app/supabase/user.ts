// src/app/supabase/user.ts
'use server';

import { cookies } from 'next/headers';
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import type { Database } from '@/app/types/supabase';
import type { User } from '@supabase/supabase-js';

export async function getUserServer(): Promise<User | null> {
  // Pass the function reference directly.
  const supabase = createServerComponentClient<Database>({ cookies });
  
  const { data, error } = await supabase.auth.getUser();
  if (error) {
    console.error('Server-side user fetch error:', error);
    return null;
  }
  return data.user;
}