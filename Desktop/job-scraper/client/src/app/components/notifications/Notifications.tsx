// 'use-client'

// import React, { useState } from 'react';
// import { 
//    Bell,  Trash2, 
//   Check, AlertCircle, CheckCircle
// } from 'lucide-react';
// import { createClient } from '@supabase/supabase-js';
// import type { AuthUser } from '../../types/auth';

// const NotificationsComponent = ({ user }) => {
//   const [notifications, setNotifications] = useState([
//     {
//       id: '1',
//       title: 'New Job Match',
//       message: 'Found 5 new jobs matching your criteria',
//       type: 'info',
//       read: false,
//       created_at: new Date().toISOString()
//     },
//     {
//       id: '2',
//       title: 'Application Deadline',
//       message: 'Reminder: Senior Developer at TechCorp deadline is tomorrow',
//       type: 'warning',
//       read: true,
//       created_at: new Date(Date.now() - 86400000).toISOString()
//     }
//   ]);

//   const markAsRead = (id) => {
//     setNotifications(prev => 
//       prev.map(notif => 
//         notif.id === id ? { ...notif, read: true } : notif
//       )
//     );
//   };

//   const markAllAsRead = () => {
//     setNotifications(prev => 
//       prev.map(notif => ({ ...notif, read: true }))
//     );
//   };

//   const deleteNotification = (id) => {
//     setNotifications(prev => prev.filter(notif => notif.id !== id));
//   };

//   const getIcon = (type) => {
//     switch(type) {
//       case 'success': return <CheckCircle className="w-5 h-5 text-green-500" />;
//       case 'warning': return <AlertCircle className="w-5 h-5 text-yellow-500" />;
//       case 'error': return <AlertCircle className="w-5 h-5 text-red-500" />;
//       default: return <Bell className="w-5 h-5 text-blue-500" />;
//     }
//   };

//   return (
//     <div className="bg-white rounded-lg shadow p-6">
//       <div className="flex items-center justify-between mb-6">
//         <h2 className="text-2xl font-bold text-gray-900 flex items-center">
//           <Bell className="w-6 h-6 mr-2" />
//           Notifications
//         </h2>
//         <button
//           onClick={markAllAsRead}
//           className="text-sm text-blue-600 hover:text-blue-800"
//         >
//           Mark all as read
//         </button>
//       </div>

//       <div className="space-y-4">
//         {notifications.map(notification => (
//           <div
//             key={notification.id}
//             className={`p-4 rounded-lg border transition-colors ${
//               notification.read ? 'bg-gray-50 border-gray-200' : 'bg-blue-50 border-blue-200'
//             }`}
//           >
//             <div className="flex items-start justify-between">
//               <div className="flex items-start space-x-3">
//                 {getIcon(notification.type)}
//                 <div className="flex-1">
//                   <h3 className={`font-medium ${notification.read ? 'text-gray-700' : 'text-gray-900'}`}>
//                     {notification.title}
//                   </h3>
//                   <p className={`text-sm mt-1 ${notification.read ? 'text-gray-500' : 'text-gray-700'}`}>
//                     {notification.message}
//                   </p>
//                   <p className="text-xs text-gray-400 mt-2">
//                     {new Date(notification.created_at).toLocaleString()}
//                   </p>
//                 </div>
//               </div>
//               <div className="flex items-center space-x-2">
//                 {!notification.read && (
//                   <button
//                     onClick={() => markAsRead(notification.id)}
//                     className="text-blue-600 hover:text-blue-800"
//                   >
//                     <Check className="w-4 h-4" />
//                   </button>
//                 )}
//                 <button
//                   onClick={() => deleteNotification(notification.id)}
//                   className="text-red-600 hover:text-red-800"
//                 >
//                   <Trash2 className="w-4 h-4" />
//                 </button>
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// };