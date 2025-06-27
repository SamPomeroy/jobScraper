
"use client";
import React, { useState } from "react";
import {
  Calendar,
  Building,
  MapPin,
  ExternalLink,
  Save,
  CheckCircle,
  Clock,
  XCircle,
  AlertCircle,
  Eye,
} from "lucide-react";
import { Job } from "@/app/types/jobs";

interface Props {
  jobs: Job[];
  onJobUpdate: (jobId: string, update: Partial<Job>) => void;
  onApplyStatusChange: (jobId: string, applied: boolean) => void;
  darkMode: boolean;
}

const JobApplicationTracker: React.FC<Props> = ({
  jobs,
  onJobUpdate,
  onApplyStatusChange,
  darkMode,
}) => {
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showModal, setShowModal] = useState(false);

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case "applied":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "interview":
        return <Clock className="w-4 h-4 text-blue-600" />;
      case "rejected":
        return <XCircle className="w-4 h-4 text-red-600" />;
      case "offer":
        return <CheckCircle className="w-4 h-4 text-yellow-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const handleApplyClick = (job: Job) => {
    window.open(job.url, "_blank");
    localStorage.setItem("pendingApplicationJobId", job.id);
  };

  return (
    <div className="space-y-4">
      {jobs.map((job) => (
        <div
          key={job.id}
          className={`p-4 rounded border transition-opacity duration-700 opacity-0 animate-fade-in delay-[${jobs.indexOf(job) * 100}ms] ${
            darkMode
              ? "bg-gray-800 border-gray-700 hover:bg-gray-700"
              : "bg-white border-gray-200 hover:bg-gray-50"
          }`}
        >

          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-1">
                <h3 className="font-semibold text-lg">{job.title}</h3>
                {job.applied && (
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                    ✅ Applied
                  </span>
                )}
                {job.saved && (
                  <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                    💾 Saved
                  </span>
                )}
              </div>
              <div
                className={`flex items-center space-x-4 text-sm ${
                  darkMode ? "text-gray-400" : "text-gray-500"
                }`}
              >
                <span className="flex items-center">
                  <Building className="w-4 h-4 mr-1" />
                  {job.company || "Unknown"}
                </span>
                <span className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {job.job_location || "Remote"}
                </span>
                <span className="flex items-center">
                  <Calendar className="w-4 h-4 mr-1" />
                  {new Date(job.date).toLocaleDateString()}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-2 ml-4">
              <button
                onClick={() => {
                  setSelectedJob(job);
                  setShowModal(true);
                }}
                className={`p-2 rounded ${
                  darkMode
                    ? "hover:bg-gray-700 text-gray-400"
                    : "hover:bg-gray-100 text-gray-500"
                }`}
              >
                <Eye className="w-4 h-4" />
              </button>

              <button
                onClick={() => handleApplyClick(job)}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                <ExternalLink className="w-4 h-4 inline mr-1" />
                Apply
              </button>

              <button
                onClick={() => onJobUpdate(job.id, { saved: !job.saved })}
                className={`p-2 rounded ${
                  job.saved
                    ? "text-blue-600"
                    : darkMode
                    ? "text-gray-400 hover:text-blue-400"
                    : "text-gray-500 hover:text-blue-600"
                }`}
              >
                <Save className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      ))}

      {/* Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div
            className={`w-full max-w-2xl rounded-lg p-6 overflow-y-auto max-h-[90vh] ${
              darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"
            }`}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">{selectedJob.title}</h3>
              <button
                onClick={() => setShowModal(false)}
                className={`rounded px-2 py-1 text-sm ${
                  darkMode
                    ? "bg-gray-700 hover:bg-gray-600"
                    : "bg-gray-100 hover:bg-gray-200"
                }`}
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <p><strong>Company:</strong> {selectedJob.company}</p>
              <p><strong>Location:</strong> {selectedJob.job_location}</p>
              <p><strong>Status:</strong> {selectedJob.status || "Pending"}</p>
              <p><strong>Site:</strong> {selectedJob.site || "N/A"}</p>
            </div>

            {selectedJob.salary && (
              <p className="mt-4 text-sm"><strong>Salary:</strong> {selectedJob.salary}</p>
            )}

            {selectedJob.search_term && (
              <p className="mt-2 text-sm"><strong>Search Term:</strong> {selectedJob.search_term}</p>
            )}

            {selectedJob.job_description && (
              <div className="mt-6">
                <p className="text-sm font-medium mb-1">Job Description</p>
                <div className="text-sm whitespace-pre-line leading-relaxed mt-2">
                  {selectedJob.job_description}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobApplicationTracker;