'use client';


import { useTheme } from '../../context/ThemeContext';
import { Switch } from '@headlessui/react';
import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';
import { Search, FileText, Bell, Settings, LogOut, Home, Mail, Info, Shield } from 'lucide-react';
import type { AuthUser } from '../../types/auth';




const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL as string | undefined;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY as string | undefined;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Supabase environment variables are not set');
}
const supabase = createClient(supabaseUrl, supabaseAnonKey);
export default function Dashboard({ user }: { user: AuthUser }) {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [jobAlerts, setJobAlerts] = useState<Job[]>([]);
  const [scrapingStatus, setScrapingStatus] = useState<{ active: boolean; lastRun: string | null }>({
    active: false,
    lastRun: null
  });
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10;
  const { darkMode, toggleDarkMode } = useTheme();


  useEffect(() => {
    const fetchJobs = async (page: number) => {
      const from = (page - 1) * pageSize;
      const to = from + pageSize - 1;

      const { data, error } = await supabase
        .from('jobs')
        .select('*')
        .order('date', { ascending: false })
        .range(from, to);

      if (error) {
        console.error('Error fetching jobs:', error);
      } else {
        setJobAlerts(data || []);
        setScrapingStatus({
          active: true,
          lastRun: new Date().toLocaleString()
        });
      }
    };

    fetchJobs(currentPage);
  }, [currentPage]);

  useEffect(() => {
    document.body.style.overflow = selectedJob ? 'hidden' : '';
  }, [selectedJob]);

  const JobModal = ({ job, onClose }: { job: Job; onClose: () => void }) => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-start mb-4">
            <h2 className="text-xl font-bold text-gray-900">{job.title}</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600"
            >
              ✕
            </button>
          </div>
          <div className="space-y-3">
            <p><strong>Company:</strong> {job.company || 'N/A'}</p>
            <p><strong>Location:</strong> {job.job_location || 'N/A'}</p>
            <p><strong>Salary:</strong> {job.salary || 'Not specified'}</p>
            <p><strong>Site:</strong> {job.site}</p>
            <p><strong>Date:</strong> {job.date}</p>
            <p><strong>Status:</strong> {job.applied ? 'Applied' : 'Pending'}</p>
            {job.job_description && (
              <div>
                <strong>Description:</strong>
                <p className="mt-2 text-sm text-gray-600">{job.job_description}</p>
              </div>
            )}
            {job.url && (
              <a
                href={job.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                View Job Posting
              </a>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Tab Navigation */}
      <div className="flex space-x-6 border-b pb-2">
        {[
          { id: 'dashboard', label: 'Dashboard', icon: Search },
          { id: 'resumes', label: 'Resumes', icon: FileText },
          { id: 'settings', label: 'Settings', icon: Settings },
          { id: 'notifications', label: 'Notifications', icon: Bell }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center space-x-2 text-sm font-medium pb-2 border-b-2 ${
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
         
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Search className="w-6 h-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">Application Status</h3>
                  <p className={`text-sm ${scrapingStatus.active ? 'text-green-600' : 'text-red-600'}`}>
                    {scrapingStatus.active ? 'Active' : 'Inactive'}
                  </p>
                  {scrapingStatus.lastRun && (
                    <p className="text-xs text-gray-500 mt-2">Last run: {scrapingStatus.lastRun}</p>
                  )}
                </div>
              </div>
            </div>

            {/* Resume Placeholder */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <FileText className="w-6 h-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">Active Resumes</h3>
                  <p className="text-sm text-gray-600">Dynamic count can be passed via props</p>
                </div>
              </div>
            </div>

            {/* Applications Sent */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Bell className="w-6 h-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-semibold text-gray-900">Applications Sent</h3>
                  <p className="text-sm text-gray-600">
                    {jobAlerts.filter(j => j.applied).length} this week
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Job List & Modal */}
          {selectedJob && (
            <JobModal job={selectedJob} onClose={() => setSelectedJob(null)} />
          )}

          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b">
              <h2 className="text-lg font-semibold text-gray-900">Recent Job Matches</h2>
            </div>
            <div className="divide-y">
              {jobAlerts.map(job => (
                <div
                  key={job.id}
                  onClick={() => setSelectedJob(job)}
                  className="px-6 py-4 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition"
                >
                  <div>
                    <h3 className="font-medium text-gray-900">{job.title}</h3>
                    <p className="text-sm text-gray-500">
                      Found on {job.site} • {job.date}
                    </p>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs rounded-full ${
                      job.applied ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {job.applied ? 'Applied' : 'Pending'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-4">
            <button
              onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
              disabled={currentPage === 1}
              className="px-4 py-2 text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
            >
              ← Previous
            </button>
            <span className="text-sm text-gray-600">Page {currentPage}</span>
            <button
              onClick={() => setCurrentPage((p) => p + 1)}
              className="px-4 py-2 text-sm bg-gray-100 rounded hover:bg-gray-200"
              disabled={jobAlerts.length < pageSize}
            >
              Next →
            </button>
          </div>
        </>
      )}

      {/* Resumes Tab */}
      {activeTab === 'resumes' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900">Resumes</h2>
          <p className="text-sm text-gray-600">Resume management coming soon.</p>
        </div>
      )}

      {/* Settings Tab */}
      {activeTab === 'settings' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900">Settings</h2>
         
         <p className="text-sm text-gray-600">Settings panel coming soon.</p>
           <div>
     <label className="flex items-center justify-between mt-4">
  <span className="text-sm text-gray-700">Dark Mode</span>
  <Switch
    checked={darkMode}
    onChange={toggleDarkMode}
    className="w-10 h-6 bg-gray-300 rounded-full relative data-[state=checked]:bg-blue-600"
  >
    <span
      className={`block w-4 h-4 bg-white rounded-full shadow absolute top-1 transition-transform ${
        darkMode ? 'translate-x-4 left-5' : 'left-1'
      }`}
    />
  </Switch>
</label>

    </div>

        </div>
      )}

      {/* Notifications Tab */}
      {activeTab === 'notifications' && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900">Notifications</h2>
          <p className="text-sm text-gray-600">Notification center coming soon.</p>
        </div>
      )}
    </div>
  );
}
