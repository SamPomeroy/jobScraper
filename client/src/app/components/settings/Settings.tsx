
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
