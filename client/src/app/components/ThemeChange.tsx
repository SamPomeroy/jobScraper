'use client';

import { useState, useEffect } from 'react';

export default function ThemeChange() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div className="p-4">
      <label className="flex items-center justify-between">
        <span className="text-sm text-gray-700">Dark Mode</span>
        <input
          type="checkbox"
          checked={darkMode}
          onChange={(e) => setDarkMode(e.target.checked)}
          className="w-5 h-5"
        />
      </label>
    </div>
  );
}