'use client';

import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { Database } from '@/app/types/database';

export const supabase: SupabaseClient<Database> = createPagesBrowserClient();

if (typeof window !== 'undefined') {
  (window as any).supabase = supabase;
}