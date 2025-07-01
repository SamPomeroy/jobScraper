
import { getUserServer } from '@/app/supabase/user';
import AppShell from '@/app/components/AppShell'; // or Dashboard if directly
import type { AuthUser } from '@/app/types/application';

export default async function Page() {
  const user = await getUserServer();
  return <AppShell initialUser={user as AuthUser | null} />;
}









