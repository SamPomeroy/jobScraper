
"use client";

import React from "react";
import { Search, Mail, Save, Bell } from "lucide-react";
import { DashboardStats as StatsType } from "../../types/dashboard";

interface DashboardStatsProps {
  stats: StatsType;
  darkMode: boolean;
}

const DashboardStats: React.FC<DashboardStatsProps> = ({ stats, darkMode }) => {
  const statCards = [
    {
      title: "Total Jobs",
      value: stats.totalJobs,
      icon: Search,
      color: "blue",
      bgColor: "bg-blue-100",
      textColor: "text-blue-600"
    },
    {
      title: "Applied",
      value: stats.appliedJobs,
      icon: Mail,
      color: "green",
      bgColor: "bg-green-100",
      textColor: "text-green-600"
    },
    {
      title: "Saved",
      value: stats.savedJobs,
      icon: Save,
      color: "yellow",
      bgColor: "bg-yellow-100",
      textColor: "text-yellow-600"
    },
    {
      title: "Interviews",
      value: stats.interviewJobs,
      icon: Bell,
      color: "purple",
      bgColor: "bg-purple-100",
      textColor: "text-purple-600"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
      {statCards.map((card) => (
        <div key={card.title} className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow p-6`}>
          <div className="flex items-center">
            <div className={`w-12 h-12 ${card.bgColor} rounded-lg flex items-center justify-center`}>
              <card.icon className={`w-6 h-6 ${card.textColor}`} />
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-semibold">{card.title}</h3>
              <p className={`text-2xl font-bold ${card.textColor}`}>{card.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default DashboardStats;