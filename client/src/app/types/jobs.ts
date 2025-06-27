export interface Job {
  id: string;
  title: string;
  company?: string;
  job_location?: string;
  salary?: string;
  site: string;
  date: string;
  applied: boolean;
  saved?: boolean;
  url: string;
  job_description?: string;
  category?: string;
  priority?: "low" | "medium" | "high";
  status?: "pending" | "applied" | "interview" | "rejected" | "offer";
  [key: string]: any;
}
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