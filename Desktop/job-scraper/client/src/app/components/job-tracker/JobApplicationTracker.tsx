
// 'use-client';
// import React, { useState} from 'react';
// import { 
//  Filter, Calendar, Building, MapPin, ExternalLink, Save
// } from 'lucide-react';
// import type { Notifications } from '../../types/auth';

// const JobApplicationTracker = ({ jobs, onJobUpdate, onApplyStatusChange }) => {
//   const [filter, setFilter] = useState('all');
//   const [category, setCategory] = useState('all');
//   const [searchTerm, setSearchTerm] = useState('');
//   const [selectedJob, setSelectedJob] = useState(null);
//   const [showApplicationModal, setShowApplicationModal] = useState(false);

//   const filteredJobs = jobs.filter(job => {
//     const matchesFilter = filter === 'all' || 
//       (filter === 'applied' && job.applied) ||
//       (filter === 'saved' && job.saved) ||
//       (filter === 'pending' && !job.applied);
    
//     const matchesCategory = category === 'all' || job.category === category;
//     const matchesSearch = job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
//                          job.company?.toLowerCase().includes(searchTerm.toLowerCase());
    
//     return matchesFilter && matchesCategory && matchesSearch;
//   });

//   const ApplicationModal = ({ job, onClose, onApply }) => (
//     <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//       <div className="bg-white rounded-lg max-w-md w-full p-6">
//         <h3 className="text-lg font-semibold mb-4">Confirm Application</h3>
//         <p className="text-gray-600 mb-6">
//           Did you successfully apply to <strong>{job.title}</strong> at <strong>{job.company}</strong>?
//         </p>
//         <div className="flex space-x-3">
//           <button
//             onClick={() => {
//               onApply(job.id, true);
//               onClose();
//             }}
//             className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
//           >
//             Yes, Applied
//           </button>
//           <button
//             onClick={() => {
//               onApply(job.id, false);
//               onClose();
//             }}
//             className="flex-1 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700"
//           >
//             No, Not Yet
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   return (
//     <div className="space-y-6">
//       {/* Filters */}
//       <div className="bg-white rounded-lg shadow p-6">
//         <div className="flex flex-wrap gap-4 items-center">
//           <div className="flex items-center space-x-2">
//             <Filter className="w-5 h-5 text-gray-500" />
//             <select
//               value={filter}
//               onChange={(e) => setFilter(e.target.value)}
//               className="border border-gray-300 rounded px-3 py-1"
//             >
//               <option value="all">All Jobs</option>
//               <option value="pending">Pending</option>
//               <option value="applied">Applied</option>
//               <option value="saved">Saved</option>
//             </select>
//           </div>
          
//           <select
//             value={category}
//             onChange={(e) => setCategory(e.target.value)}
//             className="border border-gray-300 rounded px-3 py-1"
//           >
//             <option value="all">All Categories</option>
//             <option value="technology">Technology</option>
//             <option value="finance">Finance</option>
//             <option value="healthcare">Healthcare</option>
//           </select>
          
//           <div className="flex-1 max-w-md">
//             <input
//               type="text"
//               placeholder="Search jobs..."
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
//               className="w-full border border-gray-300 rounded px-3 py-1"
//             />
//           </div>
//         </div>
//       </div>

//       {/* Job List */}
//       <div className="bg-white rounded-lg shadow">
//         <div className="px-6 py-4 border-b">
//           <h2 className="text-lg font-semibold text-gray-900">
//             Job Applications ({filteredJobs.length})
//           </h2>
//         </div>
//         <div className="divide-y">
//           {filteredJobs.map(job => (
//             <div key={job.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
//               <div className="flex items-center justify-between">
//                 <div className="flex-1">
//                   <div className="flex items-center space-x-3">
//                     <h3 className="font-medium text-gray-900">{job.title}</h3>
//                     <span className={`px-2 py-1 text-xs rounded-full ${
//                       job.applied ? 'bg-green-100 text-green-800' : 
//                       job.saved ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'
//                     }`}>
//                       {job.applied ? 'Applied' : job.saved ? 'Saved' : 'Pending'}
//                     </span>
//                   </div>
//                   <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
//                     <span className="flex items-center">
//                       <Building className="w-4 h-4 mr-1" />
//                       {job.company || 'Unknown Company'}
//                     </span>
//                     <span className="flex items-center">
//                       <MapPin className="w-4 h-4 mr-1" />
//                       {job.job_location || 'Remote'}
//                     </span>
//                     <span className="flex items-center">
//                       <Calendar className="w-4 h-4 mr-1" />
//                       {job.date}
//                     </span>
//                   </div>
//                 </div>
//                 <div className="flex items-center space-x-2">
//                   <button
//                     onClick={() => {
//                       window.open(job.url, '_blank');
//                       setTimeout(() => {
//                         setSelectedJob(job);
//                         setShowApplicationModal(true);
//                       }, 2000);
//                     }}
//                     className="flex items-center px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
//                   >
//                     <ExternalLink className="w-4 h-4 mr-1" />
//                     Apply
//                   </button>
//                   <button
//                     onClick={() => onJobUpdate(job.id, { saved: !job.saved })}
//                     className={`p-2 rounded ${job.saved ? 'text-blue-600' : 'text-gray-400 hover:text-blue-600'}`}
//                   >
//                     <Save className="w-4 h-4" />
//                   </button>
//                 </div>
//               </div>
//             </div>
//           ))}
//         </div>
//       </div>

//       {showApplicationModal && selectedJob && (
//         <ApplicationModal
//           job={selectedJob}
//           onClose={() => setShowApplicationModal(false)}
//           onApply={onApplyStatusChange}
//         />
//       )}
//     </div>
//   );
// };
