"use client";

import React from "react";
import { Job } from "../../types/jobs";

interface NotificationsTabProps {
  jobs: Job[];
  darkMode: boolean;
}

export const NotificationsTab: React.FC<NotificationsTabProps> = ({ jobs, darkMode }) => {
  return (
    <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow p-6`}>
      <h2 className="text-lg font-semibold">Notifications</h2>
      <p className={`text-sm mt-2 ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
        Stay updated on your job application progress.
      </p>
      <div className="mt-6 space-y-4">
        {/* Recent notifications based on job status changes */}
        {jobs.filter(job => job.applied).slice(0, 5).map(job => (
          <div key={job.id} className={`p-3 rounded border-l-4 border-blue-500 ${
            darkMode ? "bg-gray-700" : "bg-blue-50"
          }`}>
            <p className="text-sm font-medium">
              Application status: {job.status || 'Applied'}
            </p>
            <p className={`text-xs ${darkMode ? "text-gray-400" : "text-gray-600"}`}>
              {job.title} at {job.company} - {job.date}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};