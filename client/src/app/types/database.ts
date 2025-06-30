export type Database = {
  public: {
    Tables: {
      jobs: {
        Row: {
          id: string;
          title: string;
          company: string | null;
          job_location: string | null;
          job_state: string | null;
          salary: string | null;
          site: string | null;
          date: string | null;
          inserted_at: string | null;
          updated_at: string | null;
          url: string | null;
          job_description: string | null;
          search_term: string | null;
          category: string | null;
          priority: "low" | "medium" | "high" | string | null;
          last_verified: string | null;
          skills: string[] | null;
        };
        Insert: {
          id?: string;
          title: string;
          company?: string | null;
          job_location?: string | null;
          job_state?: string | null;
          salary?: string | null;
          site?: string | null;
          date?: string | null;
          inserted_at?: string | null;
          updated_at?: string | null;
          url?: string | null;
          job_description?: string | null;
          search_term?: string | null;
          category?: string | null;
          priority?: "low" | "medium" | "high" | string | null;
          last_verified?: string | null;
          skills?: string[] | null;
        };
        Update: {
          id?: string;
          title?: string;
          company?: string | null;
          job_location?: string | null;
          job_state?: string | null;
          salary?: string | null;
          site?: string | null;
          date?: string | null;
          inserted_at?: string | null;
          updated_at?: string | null;
          url?: string | null;
          job_description?: string | null;
          search_term?: string | null;
          category?: string | null;
          priority?: "low" | "medium" | "high" | string | null;
          last_verified?: string | null;
          skills?: string[] | null;
        };
        Relationships: [];
      };
    };
  };
};
