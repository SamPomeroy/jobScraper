"use client";
import React, { useState, useEffect } from "react";
import { useTheme } from "../../context/ThemeContext";
import { JobService } from "@/app/utils/supabase-jobs";
import { supabase } from "@/app/supabase/client";
import type { AuthUser, Job } from "@/app/types/application";
import { TabNavigation } from "@/app/components/dashboard/TabsNavigation";
import { JobTrackerTab } from "@/app/components/dashboard/JobTrackerTab";
import { ResumeTab } from "@/app/components/resume/ResumeTab";
import { SettingsTab } from "@/app/components/settings/SettingsTab";
import { NotificationsTab } from "@/app/components/notifications/NotificationTab";

interface DashboardProps {
  user: AuthUser;
}

export default function Dashboard({ user }: DashboardProps) {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [jobs, setJobs] = useState<Job[]>([]);
  const [todayOnly, setTodayOnly] = useState(false);
  const [scrapingStatus, setScrapingStatus] = useState({
    active: false,
    lastRun: null as string | null,
  });
  const [isLoading, setIsLoading] = useState(true);

  const { darkMode, toggleDarkMode } = useTheme();
  const localKey = `user_preferences_${user.id}`; // Only save user preferences

  const fetchJobs = async (): Promise<Job[]> => {
    try {
      setIsLoading(true);
      const allJobs = await JobService.getAllJobs(user.id);
      console.log("📦 Total jobs fetched:", allJobs.length);
      setJobs(allJobs);
      setScrapingStatus({
        active: true,
        lastRun: new Date().toLocaleString(),
      });
      return allJobs;
    } catch (error) {
      console.error("❌ Failed to fetch jobs:", error);
      return [];
    } finally {
      setIsLoading(false);
    }
  };

  // Auto-refresh jobs every 30 seconds
  useEffect(() => {
    fetchJobs(); // Initial fetch

    const interval = setInterval(() => {
      fetchJobs();
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, [user.id]);

  // Real-time job updates from Supabase
  useEffect(() => {
    const sub = supabase
      .channel("jobs_changes")
      .on("postgres_changes", { event: "*", schema: "public", table: "jobs" }, (payload) => {
        const { eventType, new: newJob, old: oldJob } = payload;
        
        // Helper to ensure newJob/oldJob are of type Job
        const transformJob = (job: any): Job => ({
          id: job.id,
          title: job.title,
          company: job.company ?? undefined,
          job_location: job.job_location ?? undefined,
          salary: job.salary ?? undefined,
          site: job.site || "",
          date: job.date
            ? new Date(job.date).toISOString().split("T")[0]
            : new Date().toISOString().split("T")[0],
          applied: job.applied ?? false,
          saved: job.saved ?? false,
          url: job.url || "",
          job_description: job.job_description ?? undefined,
          category: job.category ?? undefined,
          priority: job.priority ?? undefined,
          status: job.status ?? undefined,
          search_term: job.search_term ?? undefined,
          skills: job.skills ?? [],
          inserted_at: job.inserted_at ?? null,
        });

        setJobs((prev: Job[]) => {
          switch (eventType) {
            case "INSERT":
              return [transformJob(newJob), ...prev];
            case "UPDATE":
              return prev.map((j) => (j.id === newJob.id ? { ...j, ...transformJob(newJob) } : j));
            case "DELETE":
              return prev.filter((j) => j.id !== oldJob.id);
            default:
              return prev;
          }
        });
      })
      .subscribe();

    return () => {
      sub.unsubscribe();
    };
  }, [user.id]);

  // Load user preferences from localStorage
  useEffect(() => {
    const stored = localStorage.getItem(localKey);
    if (stored) {
      try {
        const preferences = JSON.parse(stored);
        // Load any saved preferences like filters, etc.
      } catch (error) {
        console.error("Failed to parse user preferences:", error);
      }
    }
  }, [user.id]);

  const handleToggleSaved = async (jobId: string, currentSaved: boolean) => {
    try {
      await JobService.toggleSaved(user.id, jobId, currentSaved);
      
      // Update local state
      setJobs(prev => prev.map((job) =>
        job.id === jobId ? { ...job, saved: !currentSaved } : job
      ));

      // Save only the applied/saved status to localStorage
      const userActions = JSON.parse(localStorage.getItem(`user_actions_${user.id}`) || '{}');
      userActions[jobId] = { ...userActions[jobId], saved: !currentSaved };
      localStorage.setItem(`user_actions_${user.id}`, JSON.stringify(userActions));
    } catch (error) {
      console.error("❌ Failed to toggle saved status:", error);
    }
  };

  const handleJobsUpdate = async (jobId: string, update: Partial<Job>) => {
    try {
      // Update in database
      await JobService.updateUserJobStatus(user.id, jobId, update);
      
      // Update local state
      setJobs(prev => prev.map((j) => (j.id === jobId ? { ...j, ...update } : j)));
      
      // Save user actions to localStorage
      const userActions = JSON.parse(localStorage.getItem(`user_actions_${user.id}`) || '{}');
      userActions[jobId] = { ...userActions[jobId], ...update };
      localStorage.setItem(`user_actions_${user.id}`, JSON.stringify(userActions));
    } catch (error) {
      console.error("❌ Failed to update job:", error);
    }
  };

  const handleApplyStatusChange = async (jobId: string, applied: boolean) => {
    try {
      await JobService.updateUserJobStatus(user.id, jobId, { applied });
      
      // Update local state
      setJobs(prev => prev.map((j) =>
        j.id === jobId ? { ...j, applied } : j
      ));

      // Save user actions to localStorage
      const userActions = JSON.parse(localStorage.getItem(`user_actions_${user.id}`) || '{}');
      userActions[jobId] = { ...userActions[jobId], applied };
      localStorage.setItem(`user_actions_${user.id}`, JSON.stringify(userActions));
    } catch (error) {
      console.error("❌ Failed to update applied status:", error);
    }
  };

  const handleRefreshJobs = () => {
    fetchJobs();
  };

  if (isLoading && jobs.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p>Loading jobs...</p>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'}`}>
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Dashboard</h1>
          <div className="flex items-center gap-4">
            <button
              onClick={handleRefreshJobs}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
              disabled={isLoading}
            >
              {isLoading ? 'Refreshing...' : 'Refresh Jobs'}
            </button>
            <span className="text-sm text-gray-500">
              Last updated: {scrapingStatus.lastRun || 'Never'}
            </span>
          </div>
        </div>

        <TabNavigation 
          activeTab={activeTab} 
          onTabChangeAction={setActiveTab} 
          darkMode={darkMode}
        />

        {activeTab === "dashboard" && (
          <JobTrackerTab
            jobs={jobs}
            onJobUpdateAction={handleJobsUpdate}
            onApplyStatusChangeAction={handleApplyStatusChange}
            onToggleSavedAction={handleToggleSaved}
            darkMode={darkMode}
            userId={user.id}
          />
        )}

        {activeTab === "resume" && (
          <ResumeTab 
            user={user}
            darkMode={darkMode} 
          />
        )}

        {activeTab === "settings" && (
          <SettingsTab 
            darkMode={darkMode}
            toggleDarkMode={toggleDarkMode}
            scrapingStatus={scrapingStatus}
          />
        )}

        {activeTab === "notifications" && (
          <NotificationsTab 
            jobs={jobs}
            darkMode={darkMode} 
          />
        )}
      </div>
    </div>
  );
}

