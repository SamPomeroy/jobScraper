// 'use client';
// import React, { useState } from 'react';
// import {
//   Calendar,
//   Building,
//   MapPin,
//   ExternJobink,
//   Save,
//   DollarSign,
//   Clock,
//   CheckCircle,
//   XCircle,
//   AlertCircle,
//   Trophy,
//   Eye
// } from 'lucide-react';
// import { Job } from '../../types/jobs';

// interface JobTrackerProps {
//   jobs: Job[];
//   onJobUpdate: (jobId: string, update: Partial<Job>) => void;
//   onApplyStatusChange: (jobId: string, applied: boolean) => void;
//   darkMode?: boolean;
// }

// interface ApplicationModalProps {
//   job: Job;
//   onClose: () => void;
//   onApply: (jobId: string, applied: boolean) => void;
//   darkMode?: boolean;
// }

// interface JobDetailsModalProps {
//   job: Job;
//   onClose: () => void;
//   onJobUpdate: (jobId: string, update: Partial<Job>) => void;
//   darkMode?: boolean;
// }

// const JobApplicationTracker: React.FC<JobTrackerProps> = ({
//   jobs,
//   onJobUpdate,
//   onApplyStatusChange,
//   darkMode = false,
// }) => {
//   const [selectedJob, setSelectedJob] = useState<Job | null>(null);
//   const [showApplicationModal, setShowApplicationModal] = useState<boolean>(false);
//   const [showDetailsModal, setShowDetailsModal] = useState<boolean>(false);

//   const getStatusIcon = (status?: string) => {
//     switch (status) {
//       case 'applied':
//         return <CheckCircle className="w-4 h-4 text-green-600" />;
//       case 'interview':
//         return <Clock className="w-4 h-4 text-blue-600" />;
//       case 'rejected':
//         return <XCircle className="w-4 h-4 text-red-600" />;
//       case 'offer':
//         return <Trophy className="w-4 h-4 text-yellow-600" />;
//       default:
//         return <AlertCircle className="w-4 h-4 text-gray-500" />;
//     }
//   };

//   const getStatusColor = (status?: string, applied?: boolean) => {
//     if (applied) return 'bg-green-100 text-green-800';
    
//     switch (status) {
//       case 'applied':
//         return 'bg-green-100 text-green-800';
//       case 'interview':
//         return 'bg-blue-100 text-blue-800';
//       case 'rejected':
//         return 'bg-red-100 text-red-800';
//       case 'offer':
//         return 'bg-yellow-100 text-yellow-800';
//       case 'pending':
//         return 'bg-gray-100 text-gray-800';
//       default:
//         return 'bg-gray-100 text-gray-800';
//     }
//   };

//   const getPriorityColor = (priority?: string) => {
//     switch (priority) {
//       case 'high':
//         return 'border-l-red-500';
//       case 'medium':
//         return 'border-l-yellow-500';
//       case 'low':
//         return 'border-l-green-500';
//       default:
//         return 'border-l-gray-300';
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
//       <div className={`rounded-lg max-w-md w-full p-6 ${darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"}`}>
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
//             className="flex-1 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
//           >
//             No, Not Yet
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   // Job Details Modal Component
//   const JobDetailsModal: React.FC<JobDetailsModalProps> = ({
//     job,
//     onClose,
//     onJobUpdate,
//     darkMode = false,
//   }) => {
//     const [editedJob, setEditedJob] = useState<Partial<Job>>({
//       status: job.status,
//       priority: job.priority,
//       category: job.category,
//     });

//     const handleSave = () => {
//       onJobUpdate(job.id, editedJob);
//       onClose();
//     };

//     return (
//       <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//         <div className={`rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 ${
//           darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"
//         }`}>
//           <div className="flex justify-between items-center mb-6">
//             <h3 className="text-xl font-semibold">{job.title}</h3>
//             <button
//               onClick={onClose}
//               className={`p-2 rounded hover:bg-opacity-80 ${
//                 darkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
//               }`}
//             >
//               <XCircle className="w-5 h-5" />
//             </button>
//           </div>

//           <div className="space-y-4">
//             {/* Job Info */}
//             <div className="grid grid-cols-2 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-1">Company</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.company || 'Unknown'}
//                 </p>
//               </div>
//               <div>
//                 <label className="block text-sm font-medium mb-1">Location</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.job_location || 'Remote'}
//                 </p>
//               </div>
//             </div>

//             {job.salary && (
//               <div>
//                 <label className="block text-sm font-medium mb-1">Salary</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.salary}
//                 </p>
//               </div>
//             )}

//             {/* Editable Fields */}
//             <div className="grid grid-cols-3 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-1">Status</label>
//                 <select
//                   value={editedJob.status || ''}
//                   onChange={(e) => setEditedJob({...editedJob, status: e.target.value as Job['status']})}
//                   className={`w-full border rounded px-3 py-2 text-sm ${
//                     darkMode 
//                       ? "bg-gray-700 border-gray-600 text-gray-100" 
//                       : "bg-white border-gray-300 text-gray-900"
//                   }`}
//                 >
//                   <option value="">Select Status</option>
//                   <option value="pending">Pending</option>
//                   <option value="applied">Applied</option>
//                   <option value="interview">Interview</option>
//                   <option value="rejected">Rejected</option>
//                   <option value="offer">Offer</option>
//                 </select>
//               </div>

//               <div>
//                 <label className="block text-sm font-medium mb-1">Priority</label>
//                 <select
//                   value={editedJob.priority || ''}
//                   onChange={(e) => setEditedJob({...editedJob, priority: e.target.value as Job['priority']})}
//                   className={`w-full border rounded px-3 py-2 text-sm ${
//                     darkMode 
//                       ? "bg-gray-700 border-gray-600 text-gray-100" 
//                       : "bg-white border-gray-300 text-gray-900"
//                   }`}
//                 >
//                   <option value="">Select Priority</option>
//                   <option value="low">Low</option>
//                   <option value="medium">Medium</option>
//                   <option value="high">High</option>
//                 </select>
//               </div>

//               <div>
//                 <label className="block text-sm font-medium mb-1">Category</label>
//                 <select
//                   value={editedJob.category || ''}
//                   onChange={(e) => setEditedJob({...editedJob, category: e.target.value})}
//                   className={`w-full border rounded px-3 py-2 text-sm ${
//                     darkMode 
//                       ? "bg-gray-700 border-gray-600 text-gray-100" 
//                       : "bg-white border-gray-300 text-gray-900"
//                   }`}
//                 >
//                   <option value="">Select Category</option>
//                   <option value="technology">Technology</option>
//                   <option value="finance">Finance</option>
//                   <option value="healthcare">Healthcare</option>
//                   <option value="marketing">Marketing</option>
//                   <option value="sales">Sales</option>
//                   <option value="design">Design</option>
//                   <option value="engineering">Engineering</option>
//                   <option value="management">Management</option>
//                 </select>
//               </div>
//             </div>

//             {/* Job Description */}
//             {job.job_description && (
//               <div>
//                 <label className="block text-sm font-medium mb-1">Description</label>
//                 <div className={`p-3 rounded border text-sm max-h-32 overflow-y-auto ${
//                   darkMode ? "bg-gray-700 border-gray-600" : "bg-gray-50 border-gray-200"
//                 }`}>
//                   {job.job_description}
//                 </div>
//               </div>
//             )}

//             {/* Action Buttons */}
//             <div className="flex space-x-3 pt-4">
//               <button
//                 onClick={handleSave}
//                 className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
//               >
//                 Save Changes
//               </button>
//               <button
//                 onClick={onClose}
//                 className={`flex-1 px-4 py-2 rounded transition-colors ${
//                   darkMode 
//                     ? "bg-gray-600 text-gray-100 hover:bg-gray-500" 
//                     : "bg-gray-200 text-gray-700 hover:bg-gray-300"
//                 }`}
//               >
//                 Cancel
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   };

//   if (jobs.length === 0) {
//     return (
//       <div className={`rounded-lg shadow p-8 text-center ${
//         darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"
//       }`}>
//         <AlertCircle className={`w-12 h-12 mx-auto mb-4 ${
//           darkMode ? "text-gray-400" : "text-gray-500"
//         }`} />
//         <h3 className="text-lg font-medium mb-2">No jobs found</h3>
//         <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
//           Try adjusting your filters or search terms.
//         </p>
//       </div>
//     );
//   }

//   return (
//     <div className="space-y-4">
//       {/* Job List */}
//       <div className={`rounded-lg shadow ${darkMode ? "bg-gray-800" : "bg-white"}`}>
//         <div className={`px-6 py-4 border-b ${darkMode ? "border-gray-700" : "border-gray-200"}`}>
//           <h2 className="text-lg font-semibold">
//             Job Applications ({jobs.length})
//           </h2>
//         </div>
//         <div className={`divide-y ${darkMode ? "divide-gray-700" : "divide-gray-200"}`}>
//           {jobs.map((job: Job) => (
//             <div
//               key={job.id}
//               className={`px-6 py-4 border-l-4 transition-colors ${getPriorityColor(job.priority)} ${
//                 darkMode ? "hover:bg-gray-700" : "hover:bg-gray-50"
//               }`}
//             >
//               <div className="flex items-center justify-between">
//                 <div className="flex-1">
//                   <div className="flex items-center space-x-3 mb-2">
//                     <h3 className="font-medium text-lg">{job.title}</h3>
//                     <div className="flex items-center space-x-1">
//                       {getStatusIcon(job.status)}
//                       <span
//                         className={`px-2 py-1 text-xs rounded-full ${getStatusColor(job.status, job.applied)}`}
//                       >
//                         {job.applied ? 'Applied' : (job.status || 'Pending')}
//                       </span>
//                     </div>
//                     {job.priority && (
//                       <span className={`px-2 py-1 text-xs rounded-full ${
//                         job.priority === 'high' ? 'bg-red-100 text-red-800' :
//                         job.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
//                         'bg-green-100 text-green-800'
//                       }`}>
//                         {job.priority} priority
//                       </span>
//                     )}
//                   </div>
//                   <div className={`flex items-center space-x-4 text-sm ${
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
//                       {new Date(job.date).toLocaleDateString()}
//                     </span>
//                     {job.salary && (
//                       <span className="flex items-center">
//                         <DollarSign className="w-4 h-4 mr-1" />
//                         {job.salary}
//                       </span>
//                     )}
//                   </div>
//                 </div>
//                 <div className="flex items-center space-x-2">
//                   <button
//                     onClick={() => {
//                       setSelectedJob(job);
//                       setShowDetailsModal(true);
//                     }}
//                     className={`p-2 rounded transition-colors ${
//                       darkMode 
//                         ? "text-gray-400 hover:text-gray-200 hover:bg-gray-700" 
//                         : "text-gray-400 hover:text-gray-600 hover:bg-gray-100"
//                     }`}
//                   >
//                     <Eye className="w-4 h-4" />
//                   </button>
//                   <button
//                     onClick={() => {
//                       window.open(job.url, '_blank');
//                       setTimeout(() => {
//                         setSelectedJob(job);
//                         setShowApplicationModal(true);
//                       }, 2000);
//                     }}
//                     className="flex items-center px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
//                   >
//                     <ExternalLink className="w-4 h-4 mr-1" />
//                     Apply
//                   </button>
//                   <button
//                     onClick={() =>
//                       onJobUpdate(job.id, { saved: !job.saved })
//                     }
//                     className={`p-2 rounded transition-colors ${
//                       job.saved
//                         ? 'text-blue-600 hover:bg-blue-50'
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

//       {/* Modals */}
//       {showApplicationModal && selectedJob && (
//         <ApplicationModal
//           job={selectedJob}
//           onClose={() => setShowApplicationModal(false)}
//           onApply={onApplyStatusChange}
//           darkMode={darkMode}
//         />
//       )}

//       {showDetailsModal && selectedJob && (
//         <JobDetailsModal
//           job={selectedJob}
//           onClose={() => setShowDetailsModal(false)}
//           onJobUpdate={onJobUpdate}
//           darkMode={darkMode}
//         />
//       )}
//     </div>
//   );
// };

// export default JobApplicationTracker;



// 'use client';
// import React, { useState } from 'react';
// import {
//   Calendar,
//   Building,
//   MapPin,
//   ExternalLink,
//   Save,
//   DollarSign,
//   Clock,
//   CheckCircle,
//   XCircle,
//   AlertCircle,
//   Trophy,
//   Eye,
//   Filter
// } from 'lucide-react';
// import { supabase } from '@/app/supabase/client';
// import { Job } from '../../types/jobs';

// interface JobTrackerProps {
//   jobs: Job[];
//   onJobUpdate: (jobId: string, update: Partial<Job>) => void;
//   onApplyStatusChange: (jobId: string, applied: boolean) => void;
//   onJobsUpdate: (jobs: Job[]) => void;
//   darkMode?: boolean;
// }

// interface ApplicationModalProps {
//   job: Job;
//   onClose: () => void;
//   onApply: (jobId: string, applied: boolean) => void;
//   darkMode?: boolean;
// }

// interface JobDetailsModalProps {
//   job: Job;
//   onClose: () => void;
//   onJobUpdate: (jobId: string, update: Partial<Job>) => void;
//   darkMode?: boolean;
// }

// const JobApplicationTracker: React.FC<JobTrackerProps> = ({
//   jobs,
//   onJobUpdate,
//   onApplyStatusChange,
//   onJobsUpdate,
//   darkMode = false,
// }) => {
//   const [selectedJob, setSelectedJob] = useState<Job | null>(null);
//   const [showApplicationModal, setShowApplicationModal] = useState<boolean>(false);
//   const [showDetailsModal, setShowDetailsModal] = useState<boolean>(false);
//   const [filter, setFilter] = useState<string>('all');
//   const [category, setCategory] = useState<string>('all');
//   const [searchTerm, setSearchTerm] = useState<string>('');
//   const [isUpdating, setIsUpdating] = useState<string | null>(null);

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
//         throw error;
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
//     const success = await updateJobInDatabase(jobId, update);
//     if (success) {
//       onJobUpdate(jobId, update);
//     }
//   };

//   const handleApplyStatusChange = async (jobId: string, applied: boolean) => {
//     const update: Partial<Job> = {
//       applied,
//       status: applied ? 'applied' : 'pending',
//       // Update the date to current date when applied
//       date: applied ? new Date().toISOString().split('T')[0] : jobs.find(j => j.id === jobId)?.date
//     };
    
//     const success = await updateJobInDatabase(jobId, update);
//     if (success) {
//       onApplyStatusChange(jobId, applied);
//     }
//   };

//   const handleSaveJob = async (jobId: string) => {
//     const job = jobs.find(j => j.id === jobId);
//     if (job) {
//       await handleJobUpdate(jobId, { saved: !job.saved });
//     }
//   };

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

//   const getStatusIcon = (status?: string) => {
//     switch (status) {
//       case 'applied':
//         return <CheckCircle className="w-4 h-4 text-green-600" />;
//       case 'interview':
//         return <Clock className="w-4 h-4 text-blue-600" />;
//       case 'rejected':
//         return <XCircle className="w-4 h-4 text-red-600" />;
//       case 'offer':
//         return <Trophy className="w-4 h-4 text-yellow-600" />;
//       default:
//         return <AlertCircle className="w-4 h-4 text-gray-500" />;
//     }
//   };

//   const getStatusColor = (status?: string, applied?: boolean) => {
//     if (applied) return 'bg-green-100 text-green-800';
    
//     switch (status) {
//       case 'applied':
//         return 'bg-green-100 text-green-800';
//       case 'interview':
//         return 'bg-blue-100 text-blue-800';
//       case 'rejected':
//         return 'bg-red-100 text-red-800';
//       case 'offer':
//         return 'bg-yellow-100 text-yellow-800';
//       case 'pending':
//         return 'bg-gray-100 text-gray-800';
//       default:
//         return 'bg-gray-100 text-gray-800';
//     }
//   };

//   const getPriorityColor = (priority?: string) => {
//     switch (priority) {
//       case 'high':
//         return 'border-l-red-500';
//       case 'medium':
//         return 'border-l-yellow-500';
//       case 'low':
//         return 'border-l-green-500';
//       default:
//         return 'border-l-gray-300';
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
//       <div className={`rounded-lg max-w-md w-full p-6 ${darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"}`}>
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
//             className="flex-1 bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
//           >
//             No, Not Yet
//           </button>
//         </div>
//       </div>
//     </div>
//   );

//   // Job Details Modal Component
//   const JobDetailsModal: React.FC<JobDetailsModalProps> = ({
//     job,
//     onClose,
//     onJobUpdate,
//     darkMode = false,
//   }) => {
//     const [editedJob, setEditedJob] = useState<Partial<Job>>({
//       status: job.status,
//       priority: job.priority,
//       category: job.category,
//     });

//     const handleSave = async () => {
//       await onJobUpdate(job.id, editedJob);
//       onClose();
//     };

//     return (
//       <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
//         <div className={`rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 ${
//           darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"
//         }`}>
//           <div className="flex justify-between items-center mb-6">
//             <h3 className="text-xl font-semibold">{job.title}</h3>
//             <button
//               onClick={onClose}
//               className={`p-2 rounded hover:bg-opacity-80 ${
//                 darkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
//               }`}
//             >
//               <XCircle className="w-5 h-5" />
//             </button>
//           </div>

//           <div className="space-y-4">
//             {/* Job Info */}
//             <div className="grid grid-cols-2 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-1">Company</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.company || 'N/A'}
//                 </p>
//               </div>
//               <div>
//                 <label className="block text-sm font-medium mb-1">Location</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.job_location || 'Remote'}
//                 </p>
//               </div>
//             </div>

//             <div className="grid grid-cols-2 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-1">State</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.job_state || 'N/A'}
//                 </p>
//               </div>
//               <div>
//                 <label className="block text-sm font-medium mb-1">Site</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.site || 'N/A'}
//                 </p>
//               </div>
//             </div>

//             {job.salary && job.salary !== 'N/A' && (
//               <div>
//                 <label className="block text-sm font-medium mb-1">Salary</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.salary}
//                 </p>
//               </div>
//             )}

//             {job.search_term && (
//               <div>
//                 <label className="block text-sm font-medium mb-1">Search Term</label>
//                 <p className={`text-sm ${darkMode ? "text-gray-300" : "text-gray-600"}`}>
//                   {job.search_term}
//                 </p>
//               </div>
//             )}

//             {/* Editable Fields */}
//             <div className="grid grid-cols-3 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-1">Status</label>
//                 <select
//                   value={editedJob.status || ''}
//                   onChange={(e) => setEditedJob({...editedJob, status: e.target.value as Job['status']})}
//                   className={`w-full border rounded px-3 py-2 text-sm ${
//                     darkMode 
//                       ? "bg-gray-700 border-gray-600 text-gray-100" 
//                       : "bg-white border-gray-300 text-gray-900"
//                   }`}
//                 >
//                   <option value="">Select Status</option>
//                   <option value="pending">Pending</option>
//                   <option value="applied">Applied</option>
//                   <option value="interview">Interview</option>
//                   <option value="rejected">Rejected</option>
//                   <option value="offer">Offer</option>
//                 </select>
//               </div>

//               <div>
//                 <label className="block text-sm font-medium mb-1">Priority</label>
//                 <select
//                   value={editedJob.priority || ''}
//                   onChange={(e) => setEditedJob({...editedJob, priority: e.target.value as Job['priority']})}
//                   className={`w-full border rounded px-3 py-2 text-sm ${
//                     darkMode 
//                       ? "bg-gray-700 border-gray-600 text-gray-100" 
//                       : "bg-white border-gray-300 text-gray-900"
//                   }`}
//                 >
//                   <option value="">Select Priority</option>
//                   <option value="low">Low</option>
//                   <option value="medium">Medium</option>
//                   <option value="high">High</option>
//                 </select>
//               </div>

//               <div>
//                 <label className="block text-sm font-medium mb-1">Category</label>
                
//               </div>
//             </div>

//             {/* Job Description */}
//             {job.job_description && (
//               <div>
//                 <label className="block text-sm font-medium mb-1">Description</label>
//                 <div className={`p-3 rounded border text-sm max-h-32 overflow-y-auto ${
//                   darkMode ? "bg-gray-700 border-gray-600" : "bg-gray-50 border-gray-200"
//                 }`}>
//                   {job.job_description}
//                 </div>
//               </div>
//             )}

//             {/* Action Buttons */}
//             <div className="flex space-x-3 pt-4">
//               <button
//                 onClick={handleSave}
//                 disabled={isUpdating === job.id}
//                 className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors disabled:opacity-50"
//               >
//                 {isUpdating === job.id ? 'Saving...' : 'Save Changes'}
//               </button>
//               <button
//                 onClick={onClose}
//                 disabled={isUpdating === job.id}
//                 className={`flex-1 px-4 py-2 rounded transition-colors disabled:opacity-50 ${
//                   darkMode 
//                     ? "bg-gray-600 text-gray-100 hover:bg-gray-500" 
//                     : "bg-gray-200 text-gray-700 hover:bg-gray-300"
//                 }`}
//               >
//                 Cancel
//               </button>
//             </div>
//           </div>
//         </div>
//       </div>
//     );
//   };

//   if (jobs.length === 0) {
//     return (
//       <div className={`rounded-lg shadow p-8 text-center ${
//         darkMode ? "bg-gray-800 text-gray-100" : "bg-white text-gray-900"
//       }`}>
//         <AlertCircle className={`w-12 h-12 mx-auto mb-4 ${
//           darkMode ? "text-gray-400" : "text-gray-500"
//         }`} />
//         <h3 className="text-lg font-medium mb-2">No jobs found</h3>
//         <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
//           Try adjusting your filters or search terms.
//         </p>
//       </div>
//     );
//   }

//   return (
//     <div className="space-y-4">
//       {/* Filters */}
//       <div className={`rounded-lg shadow p-6 ${
//         darkMode ? "bg-gray-800" : "bg-white"
//       }`}>
//         <div className="flex flex-wrap gap-4 items-center">
//           <div className="flex items-center space-x-2">
//             <Filter className={`w-5 h-5 ${darkMode ? "text-gray-400" : "text-gray-500"}`} />
          
           
//           </div>


//           <div className="flex-1 max-w-md">
//             <input
//               type="text"
//               placeholder="Search jobs..."
//               value={searchTerm}
//               onChange={(e) => setSearchTerm(e.target.value)}
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
//               className={`px-6 py-4 border-l-4 transition-colors ${getPriorityColor(job.priority)} ${
//                 darkMode ? "hover:bg-gray-700" : "hover:bg-gray-50"
//               }`}
//             >
//               <div className="flex items-center justify-between">
//                 <div className="flex-1">
//                   <div className="flex items-center space-x-3 mb-2">
//                     <h3 className="font-medium text-lg">{job.title}</h3>
//                     <div className="flex items-center space-x-1">
//                       {getStatusIcon(job.status)}
//                       <span
//                         className={`px-2 py-1 text-xs rounded-full ${getStatusColor(job.status, job.applied)}`}
//                       >
//                         {job.applied ? 'Applied' : (job.status || 'Pending')}
//                       </span>
//                     </div>
//                     {job.priority && (
//                       <span className={`px-2 py-1 text-xs rounded-full ${
//                         job.priority === 'high' ? 'bg-red-100 text-red-800' :
//                         job.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
//                         'bg-green-100 text-green-800'
//                       }`}>
//                         {job.priority} priority
//                       </span>
//                     )}
//                   </div>
//                   <div className={`flex items-center space-x-4 text-sm ${
//                     darkMode ? "text-gray-400" : "text-gray-500"
//                   }`}>
//                     <span className="flex items-center">
//                       <Building className="w-4 h-4 mr-1" />
//                       {job.company || 'N/A'}
//                     </span>
//                     <span className="flex items-center">
//                       <MapPin className="w-4 h-4 mr-1" />
//                       {job.job_location || 'Remote'}
//                     </span>
//                     <span className="flex items-center">
//                       <Calendar className="w-4 h-4 mr-1" />
//                       {new Date(job.date).toLocaleDateString()}
//                     </span>
//                     {job.salary && job.salary !== 'N/A' && (
//                       <span className="flex items-center">
//                         <DollarSign className="w-4 h-4 mr-1" />
//                         {job.salary}
//                       </span>
//                     )}
//                   </div>
//                 </div>
//                 <div className="flex items-center space-x-2">
//                   <button
//                     onClick={() => {
//                       setSelectedJob(job);
//                       setShowDetailsModal(true);
//                     }}
//                     className={`p-2 rounded transition-colors ${
//                       darkMode 
//                         ? "text-gray-400 hover:text-gray-200 hover:bg-gray-700" 
//                         : "text-gray-400 hover:text-gray-600 hover:bg-gray-100"
//                     }`}
//                   >
//                     <Eye className="w-4 h-4" />
//                   </button>
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
//                     className={`p-2 rounded transition-colors disabled:opacity-50 ${
//                       job.saved
//                         ? 'text-blue-600 hover:bg-blue-50'
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

//       {/* Modals */}
//       {showApplicationModal && selectedJob && (
//         <ApplicationModal
//           job={selectedJob}
//           onClose={() => setShowApplicationModal(false)}
//           onApply={handleApplyStatusChange}
//           darkMode={darkMode}
//         />
//       )}

//       {showDetailsModal && selectedJob && (
//         <JobDetailsModal
//           job={selectedJob}
//           onClose={() => setShowDetailsModal(false)}
//           onJobUpdate={handleJobUpdate}
//           darkMode={darkMode}
//         />
//       )}
//     </div>
//   );
// };

// export default JobApplicationTracker;
"use client";
import React, { useState } from "react";
import {
  Calendar,
  Building,
  MapPin,
  ExternalLink,
  Save,
  CheckCircle,
  Clock,
  XCircle,
  AlertCircle,
  Eye,
} from "lucide-react";
import { Job } from "@/app/types/jobs";

interface Props {
  jobs: Job[];
  onJobUpdate: (jobId: string, update: Partial<Job>) => void;
  onApplyStatusChange: (jobId: string, applied: boolean) => void;
  darkMode: boolean;
}

const JobApplicationTracker: React.FC<Props> = ({
  jobs,
  onJobUpdate,
  onApplyStatusChange,
  darkMode,
}) => {
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [showModal, setShowModal] = useState(false);

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case "applied":
        return <CheckCircle className="w-4 h-4 text-green-600" />;
      case "interview":
        return <Clock className="w-4 h-4 text-blue-600" />;
      case "rejected":
        return <XCircle className="w-4 h-4 text-red-600" />;
      case "offer":
        return <CheckCircle className="w-4 h-4 text-yellow-600" />;
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />;
    }
  };

  const handleApplyClick = (job: Job) => {
    window.open(job.url, "_blank");
    localStorage.setItem("pendingApplicationJobId", job.id);
  };

  return (
    <div className="space-y-4">
      {jobs.map((job) => (
        <div
          key={job.id}
          className={`p-4 rounded border transition ${
            darkMode
              ? "bg-gray-800 border-gray-700 hover:bg-gray-700"
              : "bg-white border-gray-200 hover:bg-gray-50"
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-3 mb-1">
                <h3 className="font-semibold text-lg">{job.title}</h3>
                {job.applied && (
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                    ✅ Applied
                  </span>
                )}
                {job.saved && (
                  <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">
                    💾 Saved
                  </span>
                )}
              </div>
              <div
                className={`flex items-center space-x-4 text-sm ${
                  darkMode ? "text-gray-400" : "text-gray-500"
                }`}
              >
                <span className="flex items-center">
                  <Building className="w-4 h-4 mr-1" />
                  {job.company || "Unknown"}
                </span>
                <span className="flex items-center">
                  <MapPin className="w-4 h-4 mr-1" />
                  {job.job_location || "Remote"}
                </span>
                <span className="flex items-center">
                  <Calendar className="w-4 h-4 mr-1" />
                  {new Date(job.date).toLocaleDateString()}
                </span>
              </div>
            </div>

            <div className="flex items-center space-x-2 ml-4">
              <button
                onClick={() => {
                  setSelectedJob(job);
                  setShowModal(true);
                }}
                className={`p-2 rounded ${
                  darkMode
                    ? "hover:bg-gray-700 text-gray-400"
                    : "hover:bg-gray-100 text-gray-500"
                }`}
              >
                <Eye className="w-4 h-4" />
              </button>

              <button
                onClick={() => handleApplyClick(job)}
                className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                <ExternalLink className="w-4 h-4 inline mr-1" />
                Apply
              </button>

              <button
                onClick={() => onJobUpdate(job.id, { saved: !job.saved })}
                className={`p-2 rounded ${
                  job.saved
                    ? "text-blue-600"
                    : darkMode
                    ? "text-gray-400 hover:text-blue-400"
                    : "text-gray-500 hover:text-blue-600"
                }`}
              >
                <Save className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      ))}

      {/* Modal */}
      {showModal && selectedJob && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 p-4">
          <div
            className={`w-full max-w-2xl rounded-lg p-6 overflow-y-auto max-h-[90vh] ${
              darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"
            }`}
          >
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold">{selectedJob.title}</h3>
              <button
                onClick={() => setShowModal(false)}
                className={`rounded px-2 py-1 text-sm ${
                  darkMode
                    ? "bg-gray-700 hover:bg-gray-600"
                    : "bg-gray-100 hover:bg-gray-200"
                }`}
              >
                Close
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <p><strong>Company:</strong> {selectedJob.company}</p>
              <p><strong>Location:</strong> {selectedJob.job_location}</p>
              <p><strong>Status:</strong> {selectedJob.status || "Pending"}</p>
              <p><strong>Site:</strong> {selectedJob.site || "N/A"}</p>
            </div>

            {selectedJob.salary && (
              <p className="mt-4 text-sm"><strong>Salary:</strong> {selectedJob.salary}</p>
            )}

            {selectedJob.search_term && (
              <p className="mt-2 text-sm"><strong>Search Term:</strong> {selectedJob.search_term}</p>
            )}

            {selectedJob.job_description && (
              <div className="mt-6">
                <p className="text-sm font-medium mb-1">Job Description</p>
                <div className="text-sm whitespace-pre-line leading-relaxed mt-2">
                  {selectedJob.job_description}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobApplicationTracker;