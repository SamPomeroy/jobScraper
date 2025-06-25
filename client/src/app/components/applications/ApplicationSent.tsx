// 'use client';
// import React, { useState, useEffect } from 'react';
// import {
//   Filter,
//   Calendar,
//   Building,
//   MapPin,
//   ExternalLink,
//   Save,
//   CheckCircle,
//   Clock,
//   XCircle,
//   AlertCircle
// } from 'lucide-react';
// import { supabase } from '@/app/supabase/client';
// import { Job } from '../../types/jobs';

// interface JobApplicationTrackerProps {
//   jobs: Job[];
//   onJobsUpdate: (jobs: Job[]) => void;
//   darkMode?: boolean;
// }

// interface ApplicationModalProps {
//   job: Job;
//   onClose: () => void;
//   onApply: (jobId: string, applied: boolean) => void;
//   darkMode?: boolean;
// }

// const JobApplicationTracker: React.FC<JobApplicationTrackerProps> = ({
//   jobs,
//   onJobsUpdate,
//   darkMode = false,
// }) => {
//   const [filter, setFilter] = useState<string>('all');
//   const [category, setCategory] = useState<string>('all');
//   const [searchTerm, setSearchTerm] = useState<string>('');
//   const [selectedJob, setSelectedJob] = useState<Job | null>(null);
//   const [showApplicationModal, setShowApplicationModal] = useState<boolean>(false);
//   const [isUpdating, setIsUpdating] = useState<string | null>(null);

//   // Filter jobs based on the current values
//   const filteredJobs = jobs.filter((job: Job) => {
//     const matchesFilter =
//       filter === 'all' ||
//       (filter === 'applied' && job.applied) ||
//       (filter === 'saved' && job.saved) ||
//       (filter === 'pending' && !job.applied);

//     const matchesCategory = category === 'all' || job.category === category;
//     const matchesSearch =
//       job.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
//       (job.company?.toLowerCase().includes(searchTerm.toLowerCase()) ?? false);

//     return matchesFilter && matchesCategory && matchesSearch;
//   });

//   // Update job in Supabase
//   const updateJobInDatabase = async (jobId: string, update: Partial<Job>) => {
//     try {
//       setIsUpdating(jobId);
//       const { data, error } = await supabase
//         .from('jobs')
//         .update(update)
//         .eq('id', jobId)
//         .select()
//         .single();

//       if (error) {
//         console.error('Error updating job:', error);
//         return false;
//       }

//       // Update local state
//       const updatedJobs = jobs.map(job =>
//         job.id === jobId ? { ...job, ...update } : job
//       );
//       onJobsUpdate(updatedJobs);
//       return true;
//     } catch (error) {
//       console.error('Error updating job:', error);
//       return false;
//     } finally {
//       setIsUpdating(null);
//     }
//   };

//   const handleJobUpdate = async (jobId: string, update: Partial<Job>) => {
//     await updateJobInDatabase(jobId, update);
//   };

//   const handleApplyStatusChange = async (jobId: string, applied: boolean) => {
//     const update: Partial<Job> = {
//       applied,
//       status: applied ? 'applied' : 'pending',
//       date: applied ? new Date().toISOString().split('T')[0] : jobs.find(j => j.id === jobId)?.date
//     };
//     await updateJobInDatabase(jobId, update);
//   };

//   const handleSaveJob = async (jobId: string) => {
//     const job = jobs.find(j => j.id === jobId);
//     if (job) {
//       await handleJobUpdate(jobId, { saved: !job.saved });
//     }
//   };

//   const getStatusIcon = (status?: string) => {
//     switch (status) {
//       case 'applied':
//         return <CheckCircle className="w-4 h-4 text-green-600" />;
//       case 'interview':
//         return <Clock className="w-4 h-4 text-blue-600" />;
//       case 'rejected':
//         return <XCircle className="w-4 h-4 text-red-600" />;
//       case 'offer':
//         return <CheckCircle className="w-4 h-4 text-yellow-600" />;
//       case 'pending':
//       default:
//         return <AlertCircle className="w-4 h-4 text-gray-500" />;
//     }
//   };

//   // Application Modal Component
//   const ApplicationModal: React.FC<ApplicationModalProps> = ({
//     job,
//     onClose,
//     onApply,
//     darkMode = false,
//   }) => (
//     <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//       <div className={`rounded-lg max-w-md w-full p-6 ${
//         darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"
//       }`}>
//         <h3 className="text-lg font-semibold mb-4">Confirm Application</h3>
//         <p className={`mb-6 ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//           Did you successfully apply to <strong>{job.title}</strong> at{' '}
//           <strong>{job.company}</strong>?
//         </p>
//         <div className="flex space-x-3">
//           <button
//             onClick={() => {
//               onApply(job.id, true);
//               onClose();
//             }}
//             className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
//           >
//             Yes, Applied
//           </button>
//           <button
//             onClick={() => {
//               onApply(job.id, false);
//               onClose();
//             }}
//             className={`flex-1 px-4 py-2 rounded transition-colors ${
//               darkMode 
//                 ? "bg-gray-600 text-white hover:bg-gray-700" 
//                 : "bg-gray-600 text-white hover:bg-gray-700"
//             }`}
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
//       <div className={`rounded-lg shadow p-6 ${
//         darkMode ? "bg-gray-800" : "bg-white"
//       }`}>
//         <div className="flex flex-wrap gap-4 items-center">
//           <div className="flex items-center space-x-2">
//             <Filter className={`w-5 h-5 ${darkMode ? "text-gray-400" : "text-gray-500"}`} />
//             <select
//               value={filter}
//               onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
//                 setFilter(e.target.value)
//               }
//               className={`border rounded px-3 py-1 ${
//                 darkMode 
//                   ? "border-gray-600 bg-gray-700 text-gray-100" 
//                   : "border-gray-300 bg-white text-gray-900"
//               }`}
//             >
//               <option value="all">All Jobs</option>
//               <option value="pending">Pending</option>
//               <option value="applied">Applied</option>
//               <option value="saved">Saved</option>
//             </select>
//           </div>

       

//           <div className="flex-1 max-w-md">
//             <input
//               type="text"
//               placeholder="Search jobs..."
//               value={searchTerm}
//               onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
//                 setSearchTerm(e.target.value)
//               }
//               className={`w-full border rounded px-3 py-1 ${
//                 darkMode 
//                   ? "border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400" 
//                   : "border-gray-300 bg-white text-gray-900"
//               }`}
//             />
//           </div>
//         </div>
//       </div>

//       {/* Job List */}
//       <div className={`rounded-lg shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
//         <div className={`px-6 py-4 border-b ${darkMode ? "border-gray-700" : "border-gray-200"}`}>
//           <h2 className="text-lg font-semibold">
//             Job Applications ({filteredJobs.length})
//           </h2>
//         </div>
//         <div className={`divide-y ${darkMode ? "divide-gray-700" : "divide-gray-200"}`}>
//           {filteredJobs.map((job: Job) => (
//             <div
//               key={job.id}
//               className={`px-6 py-4 transition-colors ${
//                 darkMode ? "hover:bg-gray-700" : "hover:bg-gray-50"
//               }`}
//             >
//               <div className="flex items-center justify-between">
//                 <div className="flex-1">
//                   <div className="flex items-center space-x-3">
//                     <h3 className="font-medium">{job.title}</h3>
//                     {getStatusIcon(job.status)}
//                     <span
//                       className={`px-2 py-1 text-xs rounded-full ${
//                         job.applied
//                           ? 'bg-green-100 text-green-800'
//                           : job.saved
//                           ? 'bg-blue-100 text-blue-800'
//                           : 'bg-yellow-100 text-yellow-800'
//                       }`}
//                     >
//                       {job.applied
//                         ? 'Applied'
//                         : job.saved
//                         ? 'Saved'
//                         : 'Pending'}
//                     </span>
//                   </div>
//                   <div className={`mt-1 flex items-center space-x-4 text-sm ${
//                     darkMode ? "text-gray-400" : "text-gray-500"
//                   }`}>
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
//                     disabled={isUpdating === job.id}
//                     className="flex items-center px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
//                   >
//                     <ExternalLink className="w-4 h-4 mr-1" />
//                     {isUpdating === job.id ? 'Updating...' : 'Apply'}
//                   </button>
//                   <button
//                     onClick={() => handleSaveJob(job.id)}
//                     disabled={isUpdating === job.id}
//                     className={`p-2 rounded transition-colors ${
//                       job.saved
//                         ? 'text-blue-600'
//                         : `${darkMode ? "text-gray-400 hover:text-blue-400" : "text-gray-400 hover:text-blue-600"}`
//                     }`}
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
//           onApply={handleApplyStatusChange}
//           darkMode={darkMode}
//         />
//       )}
//     </div>
//   );
// };

// export default JobApplicationTracker;