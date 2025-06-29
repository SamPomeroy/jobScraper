import { supabase } from "@/app/supabase/client";
import { Job } from "../types/jobs";

export class JobService {
  static async getAllJobs(): Promise<Job[]> {
    try {
      const { data, error } = await supabase
        .from("jobs")
        .select("*")
        .order("date", { ascending: false });

      if (error) {
        console.error("Error fetching jobs:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in getAllJobs:", error);
      return [];
    }
  }

  static async updateJob(
    jobId: string,
    updates: Partial<Job>
  ): Promise<Job | null> {
    try {
      const updateData = {
        ...updates,
        updated_at: new Date().toISOString(),
      };

      const { data, error } = await supabase
        .from("jobs")
        .update(updateData)
        .eq("id", jobId)
        .select()
        .single();

      if (error) {
        console.error("Error updating job:", error);
        throw error;
      }

      console.log("Job updated successfully:", data);
      return this.transformJobData(data);
    } catch (error) {
      console.error("Error in updateJob:", error);
      throw error; // Re-throw to handle in component
    }
  }

  static async markJobAsApplied(jobId: string): Promise<Job | null> {
    const updates: Partial<Job> = {
      applied: true,
      status: "applied",
      applied_date: new Date().toISOString().split("T")[0], // Track when they applied
      updated_at: new Date().toISOString(),
    };

    try {
      const result = await this.updateJob(jobId, updates);
      console.log("Job marked as applied:", result);
      return result;
    } catch (error) {
      console.error("Error marking job as applied:", error);
      throw error;
    }
  }

  static async updateJobStatus(
    jobId: string,
    status: Job["status"]
  ): Promise<Job | null> {
    const updates: Partial<Job> = {
      status,
      status_updated_at: new Date().toISOString(),
    };

    if (status === "applied") {
      updates.applied = true;
      updates.applied_date = new Date().toISOString().split("T")[0];
    }

    return this.updateJob(jobId, updates);
  }

  static async toggleJobSaved(
    jobId: string,
    currentSavedStatus: boolean
  ): Promise<Job | null> {
    return this.updateJob(jobId, {
      saved: !currentSavedStatus,
      saved_date: !currentSavedStatus
        ? new Date().toISOString().split("T")[0]
        : null,
    });
  }

  static async getJobsByStatus(status: Job["status"]): Promise<Job[]> {
    if (typeof status === "undefined") {
      return [];
    }
    try {
      const { data, error } = await supabase
        .from("jobs")
        .select("*")
        .eq("status", status)
        .order("date", { ascending: false });

      if (error) {
        console.error("Error fetching jobs by status:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in getJobsByStatus:", error);
      return [];
    }
  }

  static async getAppliedJobs(): Promise<Job[]> {
    try {
      const { data, error } = await supabase
        .from("jobs")
        .select("*")
        .eq("applied", true)
        .order("applied_date", { ascending: false });

      if (error) {
        console.error("Error fetching applied jobs:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in getAppliedJobs:", error);
      return [];
    }
  }

  static async getSavedJobs(): Promise<Job[]> {
    try {
      const { data, error } = await supabase
        .from("jobs")
        .select("*")
        .eq("saved", true)
        .order("saved_date", { ascending: false });

      if (error) {
        console.error("Error fetching saved jobs:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in getSavedJobs:", error);
      return [];
    }
  }

  static async searchJobs(searchTerm: string): Promise<Job[]> {
    try {
      const { data, error } = await supabase
        .from("jobs")
        .select("*")
        .or(
          `title.ilike.%${searchTerm}%,company.ilike.%${searchTerm}%,job_location.ilike.%${searchTerm}%,search_term.ilike.%${searchTerm}%`
        )
        .order("date", { ascending: false });

      if (error) {
        console.error("Error searching jobs:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in searchJobs:", error);
      return [];
    }
  }

  static async getFilteredJobs(filters: {
    filter?: string;
    category?: string;
    priority?: string;
    status?: string;
    searchTerm?: string;
  }): Promise<Job[]> {
    try {
      let query = supabase.from("jobs").select("*");

      if (filters.filter && filters.filter !== "all") {
        if (filters.filter === "applied") {
          query = query.eq("applied", true);
        } else if (filters.filter === "saved") {
          query = query.eq("saved", true);
        } else {
          query = query.eq("status", filters.filter);
        }
      }

      if (filters.category && filters.category !== "all") {
        query = query.eq("search_term", filters.category);
      }

      if (filters.priority && filters.priority !== "all") {
        query = query.eq("priority", filters.priority);
      }

      if (filters.status && filters.status !== "all") {
        query = query.eq("status", filters.status);
      }

      if (filters.searchTerm && filters.searchTerm.trim()) {
        const searchTerm = filters.searchTerm.trim();
        query = query.or(
          `title.ilike.%${searchTerm}%,company.ilike.%${searchTerm}%,job_location.ilike.%${searchTerm}%`
        );
      }

      query = query.order("date", { ascending: false });

      const { data, error } = await query;

      if (error) {
        console.error("Error fetching filtered jobs:", error);
        throw error;
      }

      return (data || []).map(this.transformJobData);
    } catch (error) {
      console.error("Error in getFilteredJobs:", error);
      return [];
    }
  }

  static async getJobStatistics(): Promise<{
    total: number;
    applied: number;
    saved: number;
    pending: number;
    interviews: number;
    offers: number;
    rejected: number;
  }> {
    try {
      const jobs = await this.getAllJobs();

      return {
        total: jobs.length,
        applied: jobs.filter((job) => job.applied).length,
        saved: jobs.filter((job) => job.saved).length,
        pending: jobs.filter(
          (job) => !job.applied && (!job.status || job.status === "pending")
        ).length,
        interviews: jobs.filter((job) => job.status === "interview").length,
        offers: jobs.filter((job) => job.status === "offer").length,
        rejected: jobs.filter((job) => job.status === "rejected").length,
      };
    } catch (error) {
      console.error("Error getting job statistics:", error);
      return {
        total: 0,
        applied: 0,
        saved: 0,
        pending: 0,
        interviews: 0,
        offers: 0,
        rejected: 0,
      };
    }
  }

  private static transformJobData(rawJob: any): Job {
    return {
      id: rawJob.id,
      title: rawJob.title,
      company: rawJob.company ?? undefined,
      job_location: rawJob.job_location ?? undefined,
      job_state: rawJob.job_state ?? undefined,
      salary: rawJob.salary ?? undefined,
      site: rawJob.site || "",
      date: rawJob.date || new Date().toISOString().split("T")[0],
      applied: rawJob.applied || false,
      applied_date: rawJob.applied_date ?? undefined,
      saved: rawJob.saved ?? undefined,
      saved_date: rawJob.saved_date ?? undefined,
      url: rawJob.url || "",
      job_description: rawJob.job_description ?? undefined,
      search_term: rawJob.search_term ?? undefined,
      category: rawJob.category ?? undefined,
      priority: rawJob.priority ?? undefined,
      status: rawJob.status ?? undefined,
      status_updated_at: rawJob.status_updated_at ?? undefined,
      updated_at: rawJob.updated_at ?? undefined,
      skills: rawJob.skills ?? [],
      user_id: rawJob.user_id ?? undefined,
      inserted_at: rawJob.inserted_at ?? undefined,
     
    };
  }

  static subscribeToJobChanges(callback: (jobs: Job[]) => void) {
    const subscription = supabase
      .channel("jobs_changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "jobs" },
        async (payload) => {
          console.log("Job database change detected:", payload);
          // Fetch updated jobs and call callback
          const updatedJobs = await this.getAllJobs();
          callback(updatedJobs);
        }
      )
      .subscribe();

    return subscription;
  }

  static async batchUpdateJobs(
    updates: Array<{ id: string; data: Partial<Job> }>
  ): Promise<Job[]> {
    try {
      const updatePromises = updates.map(({ id, data }) =>
        this.updateJob(id, data)
      );

      const results = await Promise.all(updatePromises);
      return results.filter((result) => result !== null) as Job[];
    } catch (error) {
      console.error("Error in batch update:", error);
      return [];
    }
  }

  static async verifyConnection(): Promise<boolean> {
    try {
      const { data, error } = await supabase.from("jobs").select("id").limit(1);

      if (error) {
        console.error("Database connection error:", error);
        return false;
      }

      console.log("Database connection verified");
      return true;
    } catch (error) {
      console.error("Error verifying database connection:", error);
      return false;
    }
  }
}
