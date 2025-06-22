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

interface SettingsProps {
  user: AuthUser;
  onSettingsChange: (settings: {
    darkMode: boolean;
    notifications: boolean;
    emailAlerts: boolean;
    soundAlerts: boolean;
    autoSave: boolean;
    defaultCategory: string;
    jobAlertFrequency: string;
  }) => void;
}