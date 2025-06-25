export interface Job {
  id: string;
  title: string;
  company?: string;
  job_location?: string;
  job_state?: string;
  salary?: string;
  site: string;
  date: string;
  applied: boolean;
  applied_date?: string;
  saved?: boolean;
  saved_date?: string;
  url: string;
  job_description?: string;
  search_term?: string;
  category?: string;
  priority?: "low" | "medium" | "high";
  status?: "pending" | "applied" | "interview" | "rejected" | "offer";
  status_updated_at?: string;
  updated_at?: string;
  [key: string]: any;
}

export interface DashboardStats {
  totalJobs: number;
  appliedJobs: number;
  savedJobs: number;
  pendingJobs: number;
  interviewJobs: number;
  offerJobs: number;
}

export interface AuthUser {
  id: string;
  email?: string;
  name?: string;
  user_metadata?: {
    role?: "user" | "admin";
    full_name?: string;
  };
}

export type UserType = {
  id: string;
  email: string;
  name: string;
} | null;

export type SettingsState = {
  darkMode: boolean;
  notifications: boolean;
  emailAlerts: boolean;
  soundAlerts: boolean;
  autoSave: boolean;
  defaultCategory: string;
  jobAlertFrequency: string;
};

export interface SettingsProps {
  user: AuthUser;
  onSettingsChange: (settings: SettingsState) => void;
}

export interface Resume {
  id: string;
  name: string;
  file_name: string;
  file_url: string;
  created_at: string;
  updated_at: string;
  is_default: boolean;
}

export type NotificationProps = {
  id: string;
  title: string;
  message: string;
  type: "info" | "success" | "warning" | "error";
  read: boolean;
  created_at: string;
};

// export interface JobFilterState {
//   filter: string;
//   category: string;
//   priority: string;
//   status: string;
//   searchTerm: string;
//   fromDate?: string;
//   toDate?: string;
// }

export interface JobFilterState {
  filter: string;

  category: string;
  status: string;
  searchTerm: string;
  fromDate?: string;
  toDate?: string;
}
