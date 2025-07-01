'use client';
import React from 'react';
import { Filter, Search, CalendarDays } from 'lucide-react';
import { JobFilterState } from '@/app/types/application';

interface Props {
  filters: JobFilterState;
  onFilterChange: (filters: JobFilterState) => void;
  darkMode?: boolean;
}

const JobFilter: React.FC<Props> = ({ filters, onFilterChange, darkMode = false }) => {
  const update = (key: keyof JobFilterState, value: string) => {
    onFilterChange({ ...filters, [key]: value });
  };

  const jobTypes = [
    "software engineer", "front-end developer", "back-end developer", "full-stack developer",
    "mobile app developer", "web developer", "wordpress developer", "shopify developer",
    "react developer", "vue.js developer", "angular developer", "javascript developer",
    "typescript developer", "html/css developer", "ui developer", "ux/ui developer",
    "web designer", "interaction designer", "accessibility specialist", "devops engineer",
    "qa engineer", "data analyst", "data scientist", "data engineer", "machine learning engineer",
    "ai developer", "python engineer", "python developer", "python web developer",
    "python data scientist", "python full stack developer", "cloud engineer", "cloud architect",
    "systems administrator", "network engineer", "site reliability engineer", "platform engineer",
    "product manager", "technical product manager", "ux designer", "ui designer",
    "cybersecurity analyst", "security engineer", "information security manager",
    "it support specialist", "help desk technician", "soc analyst", "blockchain developer",
    "ar/vr developer", "robotics engineer", "prompt engineer", "technical program manager",
    "database administrator", "etl developer", "solutions architect", "scrum master",
    "technical writer", "api integration specialist", "web performance engineer",
    "web accessibility engineer", "seo specialist", "web content manager"
  ];

  const selectClass = `border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode ? "bg-gray-700 border-gray-600 text-gray-100" : "bg-white border-gray-300 text-gray-900"
  }`;

  const inputClass = `w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
    darkMode ? "bg-gray-700 border-gray-600 text-gray-100 placeholder-gray-400" : "bg-white border-gray-300 text-gray-900 placeholder-gray-500"
  }`;

  return (
    <div className={`rounded-lg shadow p-6 mb-4 ${darkMode ? "bg-gray-800" : "bg-white"}`}>
      <div className="flex flex-wrap gap-4 items-center">

        {/* Job Type Filter */}
        <select
          value={filters.category}
          onChange={(e) => update("category", e.target.value)}
          className={`${selectClass} max-w-xs`}
        >
          <option value="all">All Job Types</option>
          {jobTypes.map((type) => (
            <option key={type} value={type}>
              {type
                .split(" ")
                .map((w) => w[0].toUpperCase() + w.slice(1))
                .join(" ")}
            </option>
          ))}
        </select>

        {/* Status Filter */}
        <select
          value={filters.status}
          onChange={(e) => update("status", e.target.value)}
          className={selectClass}
        >
          <option value="all">All Status</option>
          <option value="pending">Pending</option>
          <option value="applied">Applied</option>
          <option value="interview">Interview</option>
          <option value="rejected">Rejected</option>
          <option value="offer">Offer</option>
        </select>

        {/* From Date */}
        <div className="flex items-center gap-2">
          <CalendarDays className="w-4 h-4 text-gray-400" />
          <input
            type="date"
            value={filters.fromDate || ""}
            onChange={(e) => update("fromDate", e.target.value)}
            className={selectClass}
          />
        </div>

        {/* To Date */}
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-500">to</span>
          <input
            type="date"
            value={filters.toDate || ""}
            onChange={(e) => update("toDate", e.target.value)}
            className={selectClass}
          />
        </div>

        {/* Search Input */}
        <div className="flex-1 max-w-md relative">
          <Search
            className={`w-4 h-4 absolute left-3 top-1/2 transform -translate-y-1/2 ${
              darkMode ? "text-gray-400" : "text-gray-500"
            }`}
          />
          <input
            type="text"
            placeholder="Search jobs, companies, locations..."
            value={filters.searchTerm}
            onChange={(e) => update("searchTerm", e.target.value)}
            className={`${inputClass} pl-10`}
          />
        </div>

        {/* Clear Filters */}
<button
  onClick={() =>
onFilterChange({
  category: "all",
  status: "all",
  searchTerm: "",
  fromDate: "",
  toDate: "",
  filter: "all",
  priority: "all", // 👈 fix added
})
  }
  className={`px-4 py-2 text-sm rounded hover:bg-opacity-80 transition-colors ${
    darkMode
      ? "bg-gray-600 text-gray-100 hover:bg-gray-500"
      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
  }`}
>
  Clear Filters
</button>
      </div>
    </div>
  );
};

export default JobFilter;


