
// Define or import AuthUser type here
type AuthUser = {
  id: string;
  name: string;
  email: string;
  // add other properties as needed
};

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