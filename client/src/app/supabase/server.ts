import { createClient as createClientBase } from '@supabase/supabase-js';
import {supabase} from "../supabase/client"
export const createClient = () => {
  return createClientBase(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
};const { data: { session } } = await supabase.auth.getSession();
const accessToken = session?.access_token;

await fetch('', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    job_id: 'abc123',
    action: 'saved',
    value: true
  })
});

