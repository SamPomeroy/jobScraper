export type Database = {
  public: {
    Tables: {
      jobs: {
        Row: {
          applied: boolean | null
          company: string | null
          date: string | null
          id: string
          job_description: string | null
          job_location: string | null
          job_state: string | null
          salary: string | null
          search_term: string | null
          site: string | null
          title: string
          url: string | null
          user_id: string | null  // Added this
          status: string | null   // If you added this from previous step
        }
        Insert: {
          applied?: boolean | null
          company?: string | null
          date?: string | null
          id?: string
          job_description?: string | null
          job_location?: string | null
          job_state?: string | null
          salary?: string | null
          search_term?: string | null
          site?: string | null
          title: string
          url?: string | null
          user_id?: string | null  // Added this
          status?: string | null   // If you added this from previous step
        }
        Update: {
          applied?: boolean | null
          company?: string | null
          date?: string | null
          id?: string
          job_description?: string | null
          job_location?: string | null
          job_state?: string | null
          salary?: string | null
          search_term?: string | null
          site?: string | null
          title?: string
          url?: string | null
          user_id?: string | null  // Added this
          status?: string | null   // If you added this from previous step
        }
        Relationships: [
          {
            foreignKeyName: "jobs_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["id"]
          }
        ]
      }
      // ... rest of your schema
    }
  }
}