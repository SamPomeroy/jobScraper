"use client";

import React from "react";

interface SettingsTabProps {
  darkMode: boolean;
  toggleDarkMode: () => void;
  scrapingStatus: {
    active: boolean;
    lastRun: string | null;
  };
}

const SettingsTab: React.FC<SettingsTabProps> = ({
  darkMode,
  toggleDarkMode,
  scrapingStatus
}) => {
  return (
    <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow p-6`}>
      <h2 className="text-lg font-semibold">Settings</h2>
      <div className="mt-6 space-y-4">
        {/* Dark Mode Toggle */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium">Dark Mode</h3>
            <p className={`text-xs ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
              Toggle between light and dark theme
            </p>
          </div>
          <button
            onClick={toggleDarkMode}
            className={`w-10 h-6 rounded-full relative transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              darkMode ? "bg-blue-600" : "bg-gray-300"
            }`}
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                darkMode ? "translate-x-5" : "translate-x-1"
              }`}
            />
          </button>
        </div>

        {/* Auto-update Settings */}
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-medium">Auto-update Applications</h3>
            <p className={`text-xs ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
              Automatically track application status changes
            </p>
          </div>
          <button
            className={`w-10 h-6 rounded-full relative transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 ${
              scrapingStatus.active ? "bg-blue-600" : "bg-gray-300"
            }`}
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                scrapingStatus.active ? "translate-x-5" : "translate-x-1"
              }`}
            />
          </button>
        </div>
      </div>
    </div>
  );
};

export { SettingsTab } 
