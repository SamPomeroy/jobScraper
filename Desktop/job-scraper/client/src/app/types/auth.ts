export interface AuthUser {
  id: string;
  email?: string;
  user_metadata?: {
    role?: 'user' | 'admin';
    full_name?: string;
  };
}
type UserType = {
  id: string;
  email: string;
  name: string;
} | null;
