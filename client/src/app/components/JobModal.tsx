'use client';

import { X } from 'lucide-react';
import { useEffect } from 'react';
import Jobs from '../../../public/jobs.jpg'; // optional if using imported image

type Job = {
  title: string;
  company: string;
  job_location: string;
  job_state: string;
  date: string;
  site: string;
  job_description: string;
  salary: string;
  url: string;
};

export default function JobModal({
  job,
  onCloseAction,
}: {
  job: Job;
  onCloseAction: () => void;
}) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCloseAction();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onCloseAction]);

  return (
    <>
      
      <div
        className="fixed inset-0 bg-black bg-opacity-40 z-40"
        onClick={onCloseAction}
      />

     
      <div className="fixed inset-0 flex items-center justify-center z-50">
        <div
          className="relative bg-cover bg-center bg-no-repeat rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto"
          style={{ backgroundImage: "url('/jobs.jpg')" }} 
        >
       
          <div className="bg-white/80 backdrop-blur-sm p-6 rounded-lg relative z-10">
           
            <button
              onClick={onCloseAction}
              className="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
            >
              <X className="w-5 h-5" />
            </button>

          
            <h2 className="text-xl font-bold mb-2">{job.title}</h2>
            <p className="text-sm text-gray-600 mb-1">
              {job.company} • {job.job_location}
            </p>
            <p className="text-sm text-gray-500 mb-4">
              {job.date} • {job.site}
            </p>

            <h3 className="text-md font-semibold text-gray-800 mt-4 mb-1">
              Description
            </h3>
            <p className="text-sm whitespace-pre-line text-gray-700 mb-4">
              {job.job_description}
            </p>

            <h3 className="text-md font-semibold text-gray-800 mt-4 mb-1">
              Salary
            </h3>
            <p className="text-sm text-gray-700 mb-4">
              {job.salary || 'Not specified'}
            </p>

            <a
              href={job.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline text-sm"
            >
              View original posting
            </a>

         
            <div className="mt-6 flex justify-end">
              <button
                onClick={onCloseAction}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded hover:bg-gray-200 transition"
              >
                ← Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}