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
  inserted_at?: string; // when the job was inserted (for deduplication)
  last_verified?: string;
  [key: string]: any;
  // skills?: string[];
  // user_id?: string;
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

// interface SettingsProps {
//   user: AuthUser;
//   onSettingsChange: (settings: {
//     darkMode: boolean;
//     notifications: boolean;
//     emailAlerts: boolean;
//     soundAlerts: boolean;
//     autoSave: boolean;
//     defaultCategory: string;
//     jobAlertFrequency: string;
//   }) => void;
// }

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

export interface JobFilterState {
  filter: string;
  category: string;
  priority: string;
  status: string;
  searchTerm: string;
  fromDate?: string;
  toDate?: string;
}

export interface JobStats {
  total: number;
  applied: number;
  pending: number;
  saved: number;
  interviews: number;
  offers: number;
  rejected: number;
}

// export type Database = {
//   public: {
//     Tables: {
//       jobs: {
//         Row: {
//           applied: boolean | null
//           company: string | null
//           date: string | null
//           id: string
//           job_description: string | null
//           job_location: string | null
//           job_state: string | null
//           salary: string | null
//           search_term: string | null
//           site: string | null
//           title: string
//           url: string | null
//           user_id: string | null  // Added this
//           status: string | null   // If you added this from previous step
//         }
//         Insert: {
//           applied?: boolean | null
//           company?: string | null
//           date?: string | null
//           id?: string
//           job_description?: string | null
//           job_location?: string | null
//           job_state?: string | null
//           salary?: string | null
//           search_term?: string | null
//           site?: string | null
//           title: string
//           url?: string | null
//           user_id?: string | null  // Added this
//           status?: string | null   // If you added this from previous step
//         }
//         Update: {
//           applied?: boolean | null
//           company?: string | null
//           date?: string | null
//           id?: string
//           job_description?: string | null
//           job_location?: string | null
//           job_state?: string | null
//           salary?: string | null
//           search_term?: string | null
//           site?: string | null
//           title?: string
//           url?: string | null
//           user_id?: string | null  // Added this
//           status?: string | null   // If you added this from previous step
//         }
//         Relationships: [
//           {
//             foreignKeyName: "jobs_user_id_fkey"
//             columns: ["user_id"]
//             isOneToOne: false
//             referencedRelation: "users"
//             referencedColumns: ["id"]
//           }
//         ]
//       }
//       // ... rest of your schema
//     }
//   }
// }
