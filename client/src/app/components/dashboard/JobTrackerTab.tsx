"use client";
import React, { useState, useMemo, useEffect } from "react";
import type { Job, JobFilterState } from "@/app/types/application";
import DashboardStats from "./DashboardStats";
import JobFilter from "../job-filter/JobFilter";

export interface JobTrackerTabProps {
  jobs: Job[];
  onJobUpdateAction: (jobId: string, update: Partial<Job>) => void;
  onApplyStatusChangeAction: (jobId: string, applied: boolean) => void;
  onToggleSavedAction: (jobId: string, currentSaved: boolean) => Promise<void>; // ✅ Added
  darkMode: boolean;
  userId: string;
}

export const JobTrackerTab: React.FC<JobTrackerTabProps> = ({
  jobs,
  onJobUpdateAction,
  onApplyStatusChangeAction,
  onToggleSavedAction,
  darkMode,
  userId,
}) => {
  const [filters, setFilters] = useState<JobFilterState>({
    filter: "all",
    category: "all",
    priority: "all",
    status: "all",
    searchTerm: "",
    fromDate: undefined,
    toDate: undefined,
  });

  const [pendingJobId, setPendingJobId] = useState<string | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  const formatDate = (d?: string) =>
    d ? new Date(d).toLocaleString("en-US") : "n/a";

  const newest = useMemo(() => {
    return [...jobs].sort(
      (a, b) =>
        new Date(b.inserted_at ?? "").getTime() -
        new Date(a.inserted_at ?? "").getTime()
    )[0];
  }, [jobs]);

  useEffect(() => {
    console.log("📦 Jobs fetched:", jobs.length);
    console.log("📅 Top job date:", formatDate(newest?.date));
    console.log(
      "📥 Most recent job inserted:",
      formatDate(newest?.inserted_at)
    );
  }, [jobs, newest]);
  console.log("Current userId →", userId);

  useEffect(() => {
    const stored = localStorage.getItem("pendingApplicationJobId");
    if (stored) {
      setPendingJobId(stored);
      setShowConfirmModal(true);
    }
  }, []);

  const persistJobsForUser = (updatedJobs: Job[]) => {
    localStorage.setItem(`jobs_${userId}`, JSON.stringify(updatedJobs));
  };

  const handleConfirmApplied = () => {
    if (pendingJobId) {
      onApplyStatusChangeAction(pendingJobId, true);
      const updated = jobs.map((j) =>
        j.id === pendingJobId ? { ...j, applied: true } : j
      );
      persistJobsForUser(updated);
      localStorage.removeItem("pendingApplicationJobId");
      setShowConfirmModal(false);
      setPendingJobId(null);
    }
  };

  const handleSkipApplied = () => {
    localStorage.removeItem("pendingApplicationJobId");
    setShowConfirmModal(false);
    setPendingJobId(null);
  };

  const filteredJobs = useMemo(() => {
    return jobs.filter((job) => {
      const { filter, category, status, searchTerm, fromDate, toDate } =
        filters;

      if (filter !== "all") {
        switch (filter) {
          case "pending":
            if (job.applied) return false;
            break;
          case "applied":
            if (!job.applied) return false;
            break;
          case "saved":
            if (!job.saved) return false;
            break;
          case "interview":
          case "offer":
          case "rejected":
            if (job.status !== filter) return false;
            break;
        }
      }

      if (category !== "all") {
        const needle = category.toLowerCase();
        const haystack = (job.title ?? "") + (job.search_term ?? "");
        if (!haystack.toLowerCase().includes(needle)) return false;
      }

      if (status !== "all" && job.status !== status) return false;

      if (searchTerm) {
        const q = searchTerm.toLowerCase();
        const match =
          job.title?.toLowerCase().includes(q) ||
          job.company?.toLowerCase().includes(q) ||
          job.job_location?.toLowerCase().includes(q);
        if (!match) return false;
      }

      if (fromDate && new Date(job.date) < new Date(fromDate)) return false;
      if (toDate && new Date(job.date) > new Date(toDate)) return false;

      return true;
    });
  }, [jobs, filters]);

  const dashboardStats = {
    totalJobs: jobs.length,
    appliedJobs: jobs.filter((j) => j.applied).length,
    savedJobs: jobs.filter((j) => j.saved).length,
    pendingJobs: jobs.filter((j) => !j.applied).length,
    interviewJobs: jobs.filter((j) => j.status === "interview").length,
    offerJobs: jobs.filter((j) => j.status === "offer").length,
  };

  return (
    <>
      <DashboardStats stats={dashboardStats} darkMode={darkMode} />
      <JobFilter
        filters={filters}
        onFilterChange={setFilters}
        darkMode={darkMode}
      />

      <div className="mt-6 space-y-4">
        {filteredJobs.map((job) => (
          <div
            key={job.id}
            className={`p-4 rounded shadow transition ${
              darkMode ? "bg-gray-800 text-white" : "bg-white border text-black"
            }`}
          >
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-lg font-semibold">{job.title}</h2>
                <p className="text-sm text-gray-500">
                  {job.company} — {job.job_location}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() =>
                  onToggleSavedAction(job.id, job.saved ?? false)
                  }
                  className={`px-2 py-1 rounded text-sm transition-colors
                  ${
                    job.saved
                    ? darkMode
                      ? "bg-yellow-300 text-black hover:bg-yellow-400"
                      : "bg-yellow-400 text-black hover:bg-yellow-500"
                    : darkMode
                    ? "bg-gray-700 text-gray-300 hover:bg-gray-600"
                    : "bg-gray-200 text-gray-600 hover:bg-gray-300"
                  }
                  `}
                >
                  {job.saved ? "★ Unsave" : "☆ Save"}
                </button>

                <button
                  onClick={() =>
                    onApplyStatusChangeAction(job.id, !job.applied)
                  }
                  className={`px-2 py-1 rounded text-sm ${
                    job.applied
                      ? "bg-green-600 hover:bg-green-700 text-white"
                      : "bg-blue-500 hover:bg-blue-600 text-white"
                  }`}
                >
                  {job.applied ? "✅ Applied" : "Apply"}
                </button>
              </div>
            </div>
            <div className="mt-2">
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:underline text-sm"
              >
                View Posting
              </a>
              <p className="text-xs text-gray-400 mt-1">
                Posted on: {job.date}
              </p>
            </div>
          </div>
        ))}
      </div>

      {showConfirmModal && pendingJobId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div
            className={`w-full max-w-md rounded-lg p-6 shadow-lg ${
              darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"
            }`}
          >
            <h2 className="text-xl font-semibold mb-4">Did you apply?</h2>
            <p className="text-sm mb-6">
              You clicked “Apply” on a job but didn’t confirm. Would you like to
              mark it as applied now?
            </p>
            <div className="flex justify-end gap-3">
              <button
                onClick={handleSkipApplied}
                className="px-4 py-2 text-sm rounded border border-gray-300 hover:bg-gray-100"
              >
                Not Yet
              </button>
              <button
                onClick={handleConfirmApplied}
                className="px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Yes, I Applied
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default JobTrackerTab;
