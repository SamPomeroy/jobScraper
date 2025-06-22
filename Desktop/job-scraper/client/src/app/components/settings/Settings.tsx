// "use client";
// import React, { useState } from "react";
// import { Bell, Settings, Moon, Sun, Volume2, VolumeX } from "lucide-react";
// import type { AuthUser } from "../../types/auth";

// import { createClient } from "@supabase/supabase-js";
// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );



// type SettingsState = {
//   darkMode: boolean;
//   notifications: boolean;
//   emailAlerts: boolean;
//   soundAlerts: boolean;
//   autoSave: boolean;
//   defaultCategory: string;
//   jobAlertFrequency: string;
// };

// type SettingsComponentProps = {
//   user: AuthUser;
//   onSettingsChange: (settings: SettingsState) => void;
// };

// type SettingKey = keyof SettingsState;

// const SettingsComponent: React.FC<SettingsComponentProps> = ({ user, onSettingsChange }) => {
 
//     const [settings, setSettings] = useState<SettingsState>({
//     darkMode: false,
//     notifications: true,
//     emailAlerts: true,
//     soundAlerts: false,
//     autoSave: true,
//     defaultCategory: "technology",
//     jobAlertFrequency: "realtime",
//   });

// const handleSettingsChange = async (updatedSettings: SettingsState) => {
//   setSettings(updatedSettings);
//   onSettingsChange(updatedSettings);

//   const { error } = await supabase
//     .from("user_settings")
//     .upsert({ user_id: user.id, ...updatedSettings });

//   if (error) {
//     console.error("Failed to save settings:", error.message);
//   }

//   };

//   return (
//     <div className="bg-white rounded-lg shadow p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-gray-900 flex items-center">
//         <Settings className="w-6 h-6 mr-2" />
//         Settings
//       </h2>

//       {/* Appearance */}
//       <div className="border-b pb-4">
//         <h3 className="text-lg font-semibold text-gray-800 mb-3">Appearance</h3>
//         <div className="flex items-center justify-between">
//           <div className="flex items-center">
//             {settings.darkMode ? <Moon className="w-5 h-5 mr-2" /> : <Sun className="w-5 h-5 mr-2" />}
//             <span>Dark Mode</span>
//           </div>
//           <button
//             onClick={() => handleSettingsChange("darkMode", !settings.darkMode)}
//             className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
//               settings.darkMode ? "bg-blue-600" : "bg-gray-200"
//             }`}
//           >
//             <span
//               className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
//                 settings.darkMode ? "translate-x-6" : "translate-x-1"
//               }`}
//             />
//           </button>
//         </div>
//       </div>

//       {/* Notifications */}
//       <div className="border-b pb-4">
//         <h3 className="text-lg font-semibold text-gray-800 mb-3">Notifications</h3>
//         <div className="space-y-3">
//           <div className="flex items-center justify-between">
//             <div className="flex items-center">
//               <Bell className="w-5 h-5 mr-2" />
//               <span>Push Notifications</span>
//             </div>
//             <button
//               onClick={() => handleSettingsChange("notifications", !settings.notifications)}
//               className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
//                 settings.notifications ? "bg-blue-600" : "bg-gray-200"
//               }`}
//             >
//               <span
//                 className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
//                   settings.notifications ? "translate-x-6" : "translate-x-1"
//                 }`}
//               />
//             </button>
//           </div>

//           <div className="flex items-center justify-between">
//             <div className="flex items-center">
//               {settings.soundAlerts ? <Volume2 className="w-5 h-5 mr-2" /> : <VolumeX className="w-5 h-5 mr-2" />}
//               <span>Sound Alerts</span>
//             </div>
//             <button
//               onClick={() => handleSettingsChange("soundAlerts", !settings.soundAlerts)}
//               className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
//                 settings.soundAlerts ? "bg-blue-600" : "bg-gray-200"
//               }`}
//             >
//               <span
//                 className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
//                   settings.soundAlerts ? "translate-x-6" : "translate-x-1"
//                 }`}
//               />
//             </button>
//           </div>
//         </div>
//       </div>

//       {/* Job Preferences */}
//       <div>
//         <h3 className="text-lg font-semibold text-gray-800 mb-3">Job Preferences</h3>
//         <div className="space-y-4">
//           <div>
//             <label className="block text-sm font-medium text-gray-700 mb-2">Default Category</label>
//             <select
//               value={settings.defaultCategory}
//               onChange={(e) => handleSettingsChange("defaultCategory", e.target.value)}
//               className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//             >
//               <option value="technology">Technology</option>
//               <option value="finance">Finance</option>
//               <option value="healthcare">Healthcare</option>
//               <option value="education">Education</option>
//               <option value="marketing">Marketing</option>
//             </select>
//           </div>

//           <div>
//             <label className="block text-sm font-medium text-gray-700 mb-2">Job Alert Frequency</label>
//             <select
//               value={settings.jobAlertFrequency}
//               onChange={(e) => handleSettingsChange("jobAlertFrequency", e.target.value)}
//               className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
//             >
//               <option value="realtime">Real-time</option>
//               <option value="daily">Daily</option>
//               <option value="weekly">Weekly</option>
//             </select>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default SettingsComponent;

"use client";
import React, { useState } from "react";
import { Bell, Settings as SettingsIcon, Moon, Sun, Volume2, VolumeX } from "lucide-react";
import { Switch } from "eldora-ui";
import type { AuthUser } from "../../types/auth";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type SettingsState = {
  darkMode: boolean;
  notifications: boolean;
  emailAlerts: boolean;
  soundAlerts: boolean;
  autoSave: boolean;
  defaultCategory: string;
  jobAlertFrequency: string;
};

type SettingsComponentProps = {
  user: AuthUser;
  onSettingsChange: (settings: SettingsState) => void;
};

const SettingsComponent: React.FC<SettingsComponentProps> = ({ user, onSettingsChange }) => {
  const [settings, setSettings] = useState<SettingsState>({
    darkMode: false,
    notifications: true,
    emailAlerts: true,
    soundAlerts: false,
    autoSave: true,
    defaultCategory: "technology",
    jobAlertFrequency: "realtime",
  });

  const handleSettingsChange = async (updated: Partial<SettingsState>) => {
    const newSettings = { ...settings, ...updated };
    setSettings(newSettings);
    onSettingsChange(newSettings);

    const { error } = await supabase
      .from("user_settings")
      .upsert({ user_id: user.id, ...newSettings });

    if (error) {
      console.error("Failed to save settings:", error.message);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 flex items-center">
        <SettingsIcon className="w-6 h-6 mr-2" />
        Settings
      </h2>

      {/* Appearance */}
    <div className="border-b pb-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Appearance</h3>
      <Switch
        checked={settings.darkMode}
        onCheckedChange={(val: boolean) => handleSettingsChange({ darkMode: val })}
        label="Dark Mode"
      />
    </div>

      {/* Notifications */}
    <div className="border-b pb-4">
      <h3 className="text-lg font-semibold text-gray-800 mb-3">Notifications</h3>
      <Switch
        checked={settings.notifications}
        onCheckedChange={(val: boolean) => handleSettingsChange({ notifications: val })}
        label="Push Notifications"
      />
      <Switch
        checked={settings.soundAlerts}
        onCheckedChange={(val: boolean) => handleSettingsChange({ soundAlerts: val })}
        label="Sound Alerts"
        icon={settings.soundAlerts ? <Volume2 /> : <VolumeX />}
      />
    </div>

      {/* Job Preferences */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3">Job Preferences</h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Default Category</label>
            <select
              value={settings.defaultCategory}
              onChange={(e) => handleSettingsChange({ defaultCategory: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="technology">Technology</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
              <option value="education">Education</option>
              <option value="marketing">Marketing</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Job Alert Frequency</label>
            <select
              value={settings.jobAlertFrequency}
              onChange={(e) => handleSettingsChange({ jobAlertFrequency: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="realtime">Real-time</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsComponent;