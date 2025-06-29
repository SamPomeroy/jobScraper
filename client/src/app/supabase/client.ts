// import { createClient } from '@supabase/supabase-js'

// const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
// const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { Database } from '@/app/types/supabase';
import { cookies } from 'next/headers';

export const supabase: SupabaseClient<Database> = createPagesBrowserClient<Database>();
// Example: Fetch jobs and log the result (remove or modify as needed)
async function fetchJobs() {
  const { data, error } = await supabase
    .from("jobs")
    .select("*")
    .order("date", { ascending: false })
    .limit(20);

  if (error) {
    console.error("Error fetching jobs:", error);
  } else {
    console.log("Fetched jobs:", data);
  }
}
