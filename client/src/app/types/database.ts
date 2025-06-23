interface Job {
  id: string;
  title: string;
  company?: string;
  job_location?: string;
  salary?: string;
  site: string;
  date: string;
  applied: boolean;
  saved?: boolean;
  url?: string;
  job_description?: string;
  category?: string;
  priority?: 'low' | 'medium' | 'high';
  status?: 'pending' | 'applied' | 'interview' | 'rejected' | 'offer';
}