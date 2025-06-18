import { createClient } from '@/utils/supabase/server';
import { redirect } from 'next/navigation';

export default async function Page() {
  const supabase = createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

 if (user) {
  redirect(`/chats/${user.id}`);
}

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Welcome to the Chat App 💬</h1>
      {/* Optional: show login button or intro here */}
    </main>
  );
}