import { useEffect, useState } from "react";
import { supabase } from "../supabase/client";
import type { Job } from "../types/application";

const LOCAL_STORAGE_KEY = "user_jobs_cache";

export const useJobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    const storedJobs = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (storedJobs) {
      setJobs(JSON.parse(storedJobs));
    }

    const fetchJobs = async () => {
      const { data, error } = await supabase
        .from("jobs")
        .select("id, title, company, url, inserted_at, last_verified, date, applied, status");

      if (error) {
        console.error("❌ Supabase error:", error.message);
        return;
      }
    }
    fetchJobs();
  }, []);

  return jobs;
};