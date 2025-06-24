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

// // export default SettingsComponent;


'use client';

import { useState } from 'react';
import { useTheme } from '../../context/ThemeContext';
import { Settings as SettingsIcon, Volume2, VolumeX } from 'lucide-react';
import { Switch } from '@headlessui/react';
import type { AuthUser } from '../../types/auth';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

type SettingsState = {
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

const SettingsComponent = ({ user, onSettingsChange }: SettingsComponentProps) => {
  const { darkMode, toggleDarkMode } = useTheme();

  const [settings, setSettings] = useState<SettingsState>({
    notifications: true,
    emailAlerts: true,
    soundAlerts: false,
    autoSave: true,
    defaultCategory: 'technology',
    jobAlertFrequency: 'realtime',
  });

  const handleSettingsChange = async (updated: Partial<SettingsState>) => {
    const newSettings = { ...settings, ...updated };
    setSettings(newSettings);
    onSettingsChange(newSettings);

    const { error } = await supabase
      .from('user_settings')
      .upsert({ user_id: user.id, ...newSettings, darkMode }); // include darkMode for server sync if needed

    if (error) {
      console.error('Failed to save settings:', error.message);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-900 dark:text-white rounded-lg shadow p-6 space-y-6">
      <h2 className="text-2xl font-bold flex items-center">
        <SettingsIcon className="w-6 h-6 mr-2" />
        Settings
      </h2>

      <div className="space-y-4">
        {/* Dark mode via context */}
        <label className="flex items-center justify-between">
          <span className="text-sm">Dark Mode</span>
          <Switch
            checked={darkMode}
            onChange={toggleDarkMode}
            className="w-10 h-6 bg-gray-300 rounded-full relative dark:bg-gray-600"
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                darkMode ? 'translate-x-4 left-5' : 'left-1'
              }`}
            />
          </Switch>
        </label>

        {/* Other settings still stored locally */}
        <label className="flex items-center justify-between">
          <span className="text-sm">Push Notifications</span>
          <Switch
            checked={settings.notifications}
            onChange={(val) => handleSettingsChange({ notifications: val })}
            className="w-10 h-6 bg-gray-300 rounded-full relative"
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                settings.notifications ? 'translate-x-4 left-5' : 'left-1'
              }`}
            />
          </Switch>
        </label>

        <label className="flex items-center justify-between">
          <span className="flex items-center gap-2 text-sm">
            {settings.soundAlerts ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
            Sound Alerts
          </span>
          <Switch
            checked={settings.soundAlerts}
            onChange={(val) => handleSettingsChange({ soundAlerts: val })}
            className="w-10 h-6 bg-gray-300 rounded-full relative"
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                settings.soundAlerts ? 'translate-x-4 left-5' : 'left-1'
              }`}
            />
          </Switch>
        </label>

        <label className="flex items-center justify-between">
          <span className="text-sm">Auto Save</span>
          <Switch
            checked={settings.autoSave}
            onChange={(val) => handleSettingsChange({ autoSave: val })}
            className="w-10 h-6 bg-gray-300 rounded-full relative"
          >
            <span
              className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
                settings.autoSave ? 'translate-x-4 left-5' : 'left-1'
              }`}
            />
          </Switch>
        </label>
      </div>

      <div>
        <h3 className="text-lg font-semibold mb-3">Job Preferences</h3>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Default Category</label>
            <select
              value={settings.defaultCategory}
              onChange={(e) => handleSettingsChange({ defaultCategory: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-800"
            >
              <option value="technology">Technology</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
              <option value="education">Education</option>
              <option value="marketing">Marketing</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Job Alert Frequency</label>
            <select
              value={settings.jobAlertFrequency}
              onChange={(e) => handleSettingsChange({ jobAlertFrequency: e.target.value })}
              className="w-full p-2 border border-gray-300 rounded-md dark:bg-gray-800"
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

// "use client";
// import { useTheme } from "../../context/ThemeContext";

// import React, { useState } from "react";
// import { Settings as SettingsIcon, Volume2, VolumeX } from "lucide-react";
// import { Switch } from "@headlessui/react";
// import type { AuthUser } from "../../types/auth";
// import { createClient } from "@supabase/supabase-js";

// const supabase = createClient(
//   process.env.NEXT_PUBLIC_SUPABASE_URL!,
//   process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
// );
// const ToggleButton = () => {
//   const { darkMode, toggleDarkMode } = useTheme();
// };
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

// const SettingsComponent = ({
//   user,
//   onSettingsChange,
// }: SettingsComponentProps) => {
//   const [settings, setSettings] = useState<SettingsState>({
//     darkMode: false,
//     notifications: true,
//     emailAlerts: true,
//     soundAlerts: false,
//     autoSave: true,
//     defaultCategory: "technology",
//     jobAlertFrequency: "realtime",
//   });

//   const handleSettingsChange = async (updated: Partial<SettingsState>) => {
//     const { darkMode, toggleDarkMode } = useTheme();
//     const newSettings = { ...settings, ...updated };

//     setSettings(newSettings);
//     onSettingsChange(newSettings);
//     const { error } = await supabase
//       .from("user_settings")
//       .upsert({ user_id: user.id, ...newSettings });

//     if (error) {
//       console.error("Failed to save settings:", error.message);
//     }
//   };

//   return (
//     <div className="bg-white rounded-lg shadow p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-gray-900 flex items-center">
//         <SettingsIcon className="w-6 h-6 mr-2" />
//         Settings
//       </h2>

//       <div className="space-y-4">
//         <label className="flex items-center justify-between">
//           <span className="text-sm text-gray-700">Dark Mode</span>
//           <Switch
//             checked={settings.darkMode}
//             onChange={(val) => handleSettingsChange({ darkMode: val })}
//             className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//           >
//             <span
//               className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
//                 settings.darkMode ? "translate-x-4 left-5" : "left-1"
//               }`}
//             />
//           </Switch>
//         </label>

//         <label className="flex items-center justify-between">
//           <span className="text-sm text-gray-700">Push Notifications</span>
//           <Switch
//             checked={settings.notifications}
//             onChange={(val) => handleSettingsChange({ notifications: val })}
//             className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//           >
//             <span
//               className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
//                 settings.notifications ? "translate-x-4 left-5" : "left-1"
//               }`}
//             />
//           </Switch>
//         </label>

//         <label className="flex items-center justify-between">
//           <span className="flex items-center gap-2 text-sm text-gray-700">
//             {settings.soundAlerts ? (
//               <Volume2 className="w-4 h-4" />
//             ) : (
//               <VolumeX className="w-4 h-4" />
//             )}
//             Sound Alerts
//           </span>
//           <Switch
//             checked={settings.soundAlerts}
//             onChange={(val) => handleSettingsChange({ soundAlerts: val })}
//             className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//           >
//             <span
//               className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
//                 settings.soundAlerts ? "translate-x-4 left-5" : "left-1"
//               }`}
//             />
//           </Switch>
//         </label>

//         <label className="flex items-center justify-between">
//           <span className="text-sm text-gray-700">Auto Save</span>
//           <Switch
//             checked={settings.autoSave}
//             onChange={(val) => handleSettingsChange({ autoSave: val })}
//             className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//           >
//             <span
//               className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
//                 settings.autoSave ? "translate-x-4 left-5" : "left-1"
//               }`}
//             />
//           </Switch>
//         </label>
//       </div>

//       <div>
//         <h3 className="text-lg font-semibold text-gray-800 mb-3">
//           Job Preferences
//         </h3>

//         <div className="space-y-4">
//           <div>
//             <label className="block text-sm font-medium text-gray-700 mb-2">
//               Default Category
//             </label>
//             <select
//               value={settings.defaultCategory}
//               onChange={(e) =>
//                 handleSettingsChange({ defaultCategory: e.target.value })
//               }
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
//             <label className="block text-sm font-medium text-gray-700 mb-2">
//               Job Alert Frequency
//             </label>
//             <select
//               value={settings.jobAlertFrequency}
//               onChange={(e) =>
//                 handleSettingsChange({ jobAlertFrequency: e.target.value })
//               }
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
// "use client";
// import React, { useState } from "react";
// import { Bell, Settings as SettingsIcon, Moon, Sun, Volume2, VolumeX } from "lucide-react";
// import { Switch } from '@headlessui/react';
// import type { AuthUser } from "../../types/auth";
// import { createClient } from "@supabase/supabase-js";
// import ThemeChange from '../ThemeChange';
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

// const SettingsComponent = ({ user, onSettingsChange }: SettingsComponentProps) => {
//   const [settings, setSettings] = useState<SettingsState>({
//     darkMode: false,
//     notifications: true,
//     emailAlerts: true,
//     soundAlerts: false,
//     autoSave: true,
//     defaultCategory: "technology",
//     jobAlertFrequency: "realtime",
//   });

//   const handleSettingsChange = async (updated: Partial<SettingsState>) => {
//     const newSettings = { ...settings, ...updated };
//     setSettings(newSettings);
//     onSettingsChange(newSettings);

//     const { error } = await supabase
//       .from("user_settings")
//       .upsert({ user_id: user.id, ...newSettings });

//     if (error) {
//       console.error("Failed to save settings:", error.message);
//     }
//   };

//   return (
//     <div className="bg-white rounded-lg shadow p-6 space-y-6">
//       <h2 className="text-2xl font-bold text-gray-900 flex items-center">
//         <SettingsIcon className="w-6 h-6 mr-2" />
//         Settings
//       </h2>

//       {/* Appearance */}
//   <label className="flex items-center space-x-2">
//   <span>Dark Mode</span>
//   <Switch
//     checked={settings.darkMode}
//     onChange={(val: boolean) => handleSettingsChange({ darkMode: val })}
//     className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//   >
//     <span
//       className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
//         settings.darkMode ? "translate-x-4 left-5" : "left-1"
//       }`}
//     />
//   </Switch>
// </label>

//      <label className="flex items-center justify-between mb-2">
//   <span className="text-sm text-gray-700">Push Notifications</span>
//   <Switch
//     checked={settings.notifications}
//     onChange={(val) => handleSettingsChange({ notifications: val })}
//     className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//   >
//     <Switch.Thumb className="block w-4 h-4 bg-white rounded-full shadow absolute left-1 top-1 transition-transform data-[state=checked]:translate-x-4" />
//   </Switch>
// </label>
//      <label className="flex items-center justify-between mb-2">
//   <span className="flex items-center gap-2 text-sm text-gray-700">
//     {settings.soundAlerts ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
//     Sound Alerts
//   </span>
//   <Switch
//     checked={settings.soundAlerts}
//     onChange={(val) => handleSettingsChange({ soundAlerts: val })}
//     className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//   >
//     <Switch.Thumb className="block w-4 h-4 bg-white rounded-full shadow absolute left-1 top-1 transition-transform data-[state=checked]:translate-x-4" />
//   </Switch>
// </label>
//       </div>
//       <Switch
//         checked={settings.autoSave}
//         onChange={(val: boolean) => handleSettingsChange({ autoSave: val })}
//         label="Auto Save"
//       />
//     </div>

//       {/* Job Preferences */}
//       <div>
//         <h3 className="text-lg font-semibold text-gray-800 mb-3">Job Preferences</h3>

//         <div className="space-y-4">
//           <div>
//             <label className="block text-sm font-medium text-gray-700 mb-2">Default Category</label>
//             <select
//               value={settings.defaultCategory}
//               onChange={(e) => handleSettingsChange({ defaultCategory: e.target.value })}
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
//               onChange={(e) => handleSettingsChange({ jobAlertFrequency: e.target.value })}
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
