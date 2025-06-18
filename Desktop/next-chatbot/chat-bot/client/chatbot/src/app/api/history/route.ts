import { createClient } from "@/utils/supabase/server";
import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get('user_id');
  
  if (!userId) {
    return Response.json({ error: 'User ID required' }, { status: 400 });
  }

  const supabase = createClient();
  
  // Replace with your actual table/query
  const { data, error } = await supabase
    .from('chat_history') // or whatever your table is called
    .select('*')
    .eq('user_id', userId)
    .order('timestamp', { ascending: false });

  if (error) {
    return Response.json({ error: error.message }, { status: 500 });
  }

  return Response.json({ history: data || [] });
}