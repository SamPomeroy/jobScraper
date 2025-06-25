"use client";
import React, { useState, useMemo, useEffect } from "react";
import type { Job, JobFilterState } from "@/app/types/jobs";
import DashboardStats from "./DashboardStats";
import JobFilter from "../job-filter/JobFilter";
import JobApplicationTracker from "../job-tracker/JobApplicationTracker";

export interface JobTrackerTabProps {
  jobs: Job[];
  onJobUpdateAction: (jobId: string, update: Partial<Job>) => void;
  onApplyStatusChangeAction: (jobId: string, applied: boolean) => void;
  darkMode: boolean;
}

export const JobTrackerTab: React.FC<JobTrackerTabProps> = ({
  jobs,
  onJobUpdateAction,
  onApplyStatusChangeAction,
  darkMode,
}) => {
  const [filters, setFilters] = useState<JobFilterState>({
    filter: "all",
    category: "all",
    priority: "all",
    status: "all",
    searchTerm: "",
    fromDate: "",
    toDate: "",
  });

  const [pendingJobId, setPendingJobId] = useState<string | null>(null);
  const [showConfirmModal, setShowConfirmModal] = useState(false);

  // ✅ Prompt if pending application is stored in localStorage
  useEffect(() => {
    const stored = localStorage.getItem("pendingApplicationJobId");
    if (stored) {
      setPendingJobId(stored);
      setShowConfirmModal(true);
    }
  }, []);

  const handleConfirmApplied = () => {
    if (pendingJobId) {
      onApplyStatusChangeAction(pendingJobId, true);
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
      const {
        filter,
        category,
        status,
        searchTerm,
        fromDate,
        toDate,
      } = filters;

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
      <JobFilter filters={filters} onFilterChange={setFilters} darkMode={darkMode} />
      <JobApplicationTracker
        jobs={filteredJobs}
        onJobUpdate={onJobUpdateAction}
        onApplyStatusChange={onApplyStatusChangeAction}
        darkMode={darkMode}
      />

      {/* ✅ Confirm Apply Modal */}
      {showConfirmModal && pendingJobId && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div className={`w-full max-w-md rounded-lg p-6 shadow-lg ${darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-800"}`}>
            <h2 className="text-xl font-semibold mb-4">Did you apply?</h2>
            <p className="text-sm mb-6">You clicked “Apply” on a job but didn’t confirm. Would you like to mark it as applied now?</p>
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



// "use client";

// import React, { useState, useMemo } from "react";
// import type { Job, JobFilterState } from "@/app/types/jobs";
// import DashboardStats from "../dashboard/DashboardStats";
// import JobFilter from "../job-filter/JobFilter";
// import JobApplicationTracker from "../job-tracker/JobApplicationTracker";

// export interface JobTrackerTabProps {
//   jobs: Job[];
//   onJobUpdateAction: (jobId: string, update: Partial<Job>) => void;
//   onApplyStatusChangeAction: (jobId: string, applied: boolean) => void;
//   darkMode: boolean;
// }

// export const JobTrackerTab: React.FC<JobTrackerTabProps> = ({
//   jobs,
//   onJobUpdateAction,
//   onApplyStatusChangeAction,
//   darkMode,
// }) => {
//   const [filters, setFilters] = useState<JobFilterState>({
//     filter: "all",
//     category: "all",
//     priority: "all",
//     status: "all",
//     searchTerm: "",
//   });

//   const filteredJobs = useMemo(() => {
//     return jobs.filter((job) => {
//       if (filters.filter !== "all") {
//         switch (filters.filter) {
//           case "pending":
//             if (job.applied) return false;
//             break;
//           case "applied":
//             if (!job.applied) return false;
//             break;
//           case "saved":
//             if (!job.saved) return false;
//             break;
//           case "interview":
//             if (job.status !== "interview") return false;
//             break;
//           case "offer":
//             if (job.status !== "offer") return false;
//             break;
//           case "rejected":
//             if (job.status !== "rejected") return false;
//             break;
//         }
//       }
//       if (filters.category !== "all" && job.category !== filters.category) return false;
//       if (filters.priority !== "all" && job.priority !== filters.priority) return false;
//       if (filters.status !== "all" && job.status !== filters.status) return false;
//       if (filters.searchTerm) {
//         const query = filters.searchTerm.toLowerCase();
//         const match =
//           job.title.toLowerCase().includes(query) ||
//           job.company?.toLowerCase().includes(query) ||
//           job.job_location?.toLowerCase().includes(query);
//         if (!match) return false;
//       }
//       return true;
//     });
//   }, [jobs, filters]);

//   const dashboardStats = {
//     totalJobs: jobs.length,
//     appliedJobs: jobs.filter((j) => j.applied).length,
//     savedJobs: jobs.filter((j) => j.saved).length,
//     pendingJobs: jobs.filter((j) => !j.applied).length,
//     interviewJobs: jobs.filter((j) => j.status === "interview").length,
//     offerJobs: jobs.filter((j) => j.status === "offer").length,
//   };
// console.log("✅ Filtered jobs in view:", filteredJobs.length);


//   return (
//     <>
//       <DashboardStats stats={dashboardStats} darkMode={darkMode} />
//       <JobFilter filters={filters} onFilterChange={setFilters} darkMode={darkMode} />
//       <JobApplicationTracker
//         jobs={filteredJobs}
//         onJobUpdate={onJobUpdateAction}
//         onApplyStatusChange={onApplyStatusChangeAction}
//         onJobsUpdate={() => {}}
//         darkMode={darkMode}
//       />
//     </>
//   );
// };

// export default JobTrackerTab;