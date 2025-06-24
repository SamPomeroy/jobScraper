'use client';

// import * as Switch from '@radix-ui/react-switch';

// interface SettingsToggleProps {
//   settings: {
//     darkMode: boolean;
//     [key: string]: any;
//   };
//   handleSettingsChange: (settings: { darkMode: boolean }) => void;
// }

// export default function SettingsToggle({ settings, handleSettingsChange }: SettingsToggleProps) {
//   return (
//     <div>
//       <label htmlFor="dark-mode-toggle">
//         Dark Mode
//         <Switch.Root
//           id="dark-mode-toggle"
//           checked={settings.darkMode}
//           onCheckedChange={(val) => handleSettingsChange({ darkMode: val })}
//           className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//         >
//           <Switch.Thumb className="block w-4 h-4 bg-white rounded-full shadow absolute left-1 top-1 transition-transform data-[state=checked]:translate-x-4" />
//         </Switch.Root>
//       </label>
//     </div>
//   );
// }


// import { useState } from 'react';
// import * as Switch from '@radix-ui/react-switch';

// export default function ThemeChange() {
//   const [settings, setSettings] = useState({ darkMode: false });

//   const handleSettingsChange = (newSettings: Partial<typeof settings>) => {
//     setSettings((prev) => ({ ...prev, ...newSettings }));
//     // You could also toggle a Tailwind theme class here
//   };

//   return (
//     <div>
//       <label htmlFor="dark-mode-toggle" className="flex items-center gap-2">
//         Dark Mode
//         <Switch.Root
//           id="dark-mode-toggle"
//           checked={settings.darkMode}
//           onCheckedChange={(val) => handleSettingsChange({ darkMode: val })}
//           className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
//         >
//           <Switch.Thumb className="block w-4 h-4 bg-white rounded-full shadow absolute left-1 top-1 transition-transform data-[state=checked]:translate-x-4" />
//         </Switch.Root>
//       </label>
//     </div>
//   );
// }
// 'use client';

// type SettingsState = {
//   darkMode: boolean;
//   notifications: boolean;
//   emailAlerts: boolean;
//   soundAlerts: boolean;
//   autoSave: boolean;
//   defaultCategory: string;
//   jobAlertFrequency: string;
// };

// type ThemeChangeProps = {
//   settings: SettingsState;
//   handleSettingsChange: (updated: Partial<SettingsState>) => void;
// };

// export default function ThemeChange({ settings, handleSettingsChange }: ThemeChangeProps) {
//   // You can use settings.darkMode etc. here safely
//   return (
//     <div>
//       <label className="flex items-center justify-between">
//         <span className="text-sm text-gray-700">Dark Mode</span>
//         <input
//           type="checkbox"
//           checked={settings.darkMode}
//           onChange={(e) => handleSettingsChange({ darkMode: e.target.checked })}
//         />
//       </label>
//     </div>
//   );
// }

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