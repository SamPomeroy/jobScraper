// lib/supabase-server.ts
import { createServerComponentClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { type SupabaseClient } from '@supabase/supabase-js';
import { type Database } from '@/types/supabase';


export const createSupabaseServerClient = (): SupabaseClient<Database> => {
  return createServerComponentClient<Database>({
    cookies,
  });
};
