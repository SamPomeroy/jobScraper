// client.ts
import { createPagesBrowserClient } from '@supabase/auth-helpers-nextjs';
import type { SupabaseClient } from '@supabase/supabase-js';
import type { Database } from '@/types/supabase';

export const supabase: SupabaseClient<Database> = createPagesBrowserClient<Database>();