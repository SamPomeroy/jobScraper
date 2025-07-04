"use client";

import React from "react";
import { Search, FileText, Bell, Settings, Mail } from "lucide-react";

interface Tab {
  id: string;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
}

interface TabNavigationProps {
  activeTab: string;
  onTabChangeAction: (tabId: string) => void;
  darkMode: boolean;
}

export const TabNavigation: React.FC<TabNavigationProps> = ({ 
  activeTab, 
  onTabChangeAction, 
  darkMode 
}) => {
  const tabs: Tab[] = [
    { id: "dashboard", label: "Job Tracker", icon: Search },
    { id: "applications", label: "Applications Sent", icon: Mail },
    { id: "resume", label: "Resume", icon: FileText },
    { id: "settings", label: "Settings", icon: Settings },
    { id: "notifications", label: "Notifications", icon: Bell },
  ];

  return (
    <div className="flex flex-wrap items-center justify-between">
      <div
        className={`flex flex-wrap gap-3 sm:gap-5 md:gap-6 overflow-x-auto pb-3 ${
          darkMode ? "border-gray-700" : "border-gray-200"
        }`}
      >
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChangeAction(tab.id)}
            className={`flex items-center gap-2 text-sm font-medium pb-2 border-b-2 transition-all ${
              activeTab === tab.id
                ? "border-blue-500 text-blue-600"
                : `border-transparent ${
                    darkMode
                      ? "text-gray-400 hover:text-gray-200 hover:border-gray-600"
                      : "text-gray-500 hover:text-gray-700 hover:border-gray-300"
                  }`
            }`}
          >
            <tab.icon className="w-5 h-5 shrink-0" />
            <span className="hidden sm:inline">{tab.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};