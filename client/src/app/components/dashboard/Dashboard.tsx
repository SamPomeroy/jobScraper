"use client";
import React, { useState, useEffect } from "react";
import { useTheme } from "../../context/ThemeContext";
import { supabase } from "@/app/supabase/client";
import type { AuthUser } from "@/app/types/auth";
import type { Job } from "@/app/types/application";

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
  const [scrapingStatus, setScrapingStatus] = useState<{
    active: boolean;
    lastRun: string | null;
  }>({
    active: false,
    lastRun: null,
  });

  const { darkMode, toggleDarkMode } = useTheme();

  useEffect(() => {
    const fetchJobs = async () => {
      try {
    const { data, error } = await supabase
  .from("jobs")
  .select("*")
  .eq("user_id", user.id) // ensures only that user's jobs
  .order("date", { ascending: false });

        console.log("🛠️ Raw jobs data from Supabase:", data);

        if (error) {
          console.error("Error fetching jobs:", error);
        } else {
          const transformedJobs: Job[] = (data || []).map((job: any) => ({
            id: job.id,
            title: job.title,
            company: job.company ?? undefined,
            job_location: job.job_location ?? undefined,
            salary: job.salary ?? undefined,
            site: job.site || "",
            date: job.date || new Date().toISOString().split("T")[0],
            applied: job.applied === true,
            saved: job.saved ?? undefined,
            url: job.url || "",
            job_description: job.job_description ?? undefined,
            category: job.category ?? undefined,
            priority: job.priority ?? undefined,
            status: job.status ?? undefined,
            search_term: job.search_term ?? undefined,
          }));

          setJobs(transformedJobs);
          setScrapingStatus({
            active: true,
            lastRun: new Date().toLocaleString(),
          });
        }
      } catch (error) {
        console.error("Error fetching jobs:", error);
      }
    };

    fetchJobs();

    const subscription = supabase
      .channel("jobs_changes")
      .on(
        "postgres_changes",
        { event: "*", schema: "public", table: "jobs" },
        () => {
          fetchJobs();
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  const handleJobsUpdate = (jobId: string, update: Partial<Job>) => {
    setJobs((prev) =>
      prev.map((j) => (j.id === jobId ? { ...j, ...update } : j))
    );
  };

  const handleApplyStatusChange = (jobId: string, applied: boolean) => {
    handleJobsUpdate(jobId, { applied });
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case "dashboard":
        return (
          <JobTrackerTab
            jobs={jobs}
            onJobUpdateAction={handleJobsUpdate}
            onApplyStatusChangeAction={handleApplyStatusChange}
            darkMode={darkMode}
          />
        );
      case "applications":
        return (
          <JobTrackerTab
            jobs={jobs.filter((j) => j.applied)}
            onJobUpdateAction={handleJobsUpdate}
            onApplyStatusChangeAction={handleApplyStatusChange}
            darkMode={darkMode}
          />
        );
      case "resumes":
        return <ResumeTab user={user} darkMode={darkMode} />;
      case "settings":
        return (
          <SettingsTab
            darkMode={darkMode}
            toggleDarkMode={toggleDarkMode}
            scrapingStatus={scrapingStatus}
          />
        );
      case "notifications":
        return <NotificationsTab jobs={jobs} darkMode={darkMode} />;
      default:
        return null;
    }
  };

  return (
    <div
      className={`min-h-screen ${
        darkMode ? "bg-gray-900 text-white" : "bg-white text-black"
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <TabNavigation
          activeTab={activeTab}
          onTabChangeAction={setActiveTab}
          darkMode={darkMode}
        />
        {renderTabContent()}
      </div>
    </div>
  );
}