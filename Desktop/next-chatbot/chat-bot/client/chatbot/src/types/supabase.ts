import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import type { SupabaseClient } from '@supabase/supabase-js';
// import type { Database } from '@/types/supabase';

export const supabase: SupabaseClient<Database> = createPagesBrowserClient({
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL!,
  supabaseKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
});

export type Database = {
  public: {
    Tables: {
      // table definitions...
    };
    // ...
  };
};