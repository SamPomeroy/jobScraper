"use client";

import React, { useState, useRef } from "react";
import { FileText, Upload, Trash2, Eye, Star } from "lucide-react";
import { Resume } from "../../types/resume";
import type { AuthUser } from "../../types/auth";

interface ResumeTabProps {
  user: AuthUser;
  darkMode: boolean;
}

export const ResumeTab: React.FC<ResumeTabProps> = ({ user, darkMode }) => {
  const [resumes, setResumes] = useState<Resume[]>([
    {
      id: "1",
      name: "Senior Developer Resume",
      file_name: "senior-dev-resume.pdf",
      file_url: "#",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      is_default: true,
    },
  ]);
  const [uploading, setUploading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ): Promise<void> => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    // Simulate an upload delay
    setTimeout(() => {
      const newResume: Resume = {
        id: Date.now().toString(),
        name: file.name.replace(/\.(pdf|doc|docx)$/i, ""),
        file_name: file.name,
        file_url: URL.createObjectURL(file),
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        is_default: false,
      };
      setResumes((prev) => [...prev, newResume]);
      setUploading(false);
    }, 2000);
  };

  const setDefaultResume = (id: string): void => {
    setResumes((prev) =>
      prev.map((resume) => ({
        ...resume,
        is_default: resume.id === id,
      }))
    );
  };

  const deleteResume = (id: string): void => {
    setResumes((prev) => prev.filter((resume) => resume.id !== id));
  };

  return (
    <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow p-6`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className={`text-2xl font-bold flex items-center ${
          darkMode ? "text-gray-100" : "text-gray-900"
        }`}>
          <FileText className="w-6 h-6 mr-2" />
          Resume Management
        </h2>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          <Upload className="w-4 h-4 mr-2" />
          {uploading ? "Uploading..." : "Upload Resume"}
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx"
          className="hidden"
          onChange={handleFileUpload}
        />
      </div>

      <div className="grid gap-4">
        {resumes.map((resume) => (
          <div
            key={resume.id}
            className={`border rounded-lg p-4 hover:shadow-md transition-shadow ${
              darkMode 
                ? "border-gray-600 hover:bg-gray-700" 
                : "border-gray-200 hover:bg-gray-50"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="w-8 h-8 text-blue-600" />
                <div>
                  <h3 className={`font-medium flex items-center ${
                    darkMode ? "text-gray-100" : "text-gray-900"
                  }`}>
                    {resume.name}
                    {resume.is_default && (
                      <Star className="w-4 h-4 text-yellow-500 ml-2 fill-current" />
                    )}
                  </h3>
                  <p className={`text-sm ${
                    darkMode ? "text-gray-400" : "text-gray-500"
                  }`}>
                    Updated {new Date(resume.updated_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => window.open(resume.file_url, "_blank")}
                  className={`p-2 hover:text-blue-600 transition-colors ${
                    darkMode ? "text-gray-400" : "text-gray-600"
                  }`}
                  title="View Resume"
                >
                  <Eye className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setDefaultResume(resume.id)}
                  className={`p-2 transition-colors ${
                    resume.is_default
                      ? "text-yellow-500"
                      : `hover:text-yellow-500 ${
                          darkMode ? "text-gray-400" : "text-gray-600"
                        }`
                  }`}
                  title="Set as Default"
                >
                  <Star className="w-4 h-4" />
                </button>
                <button
                  onClick={() => deleteResume(resume.id)}
                  className={`p-2 hover:text-red-600 transition-colors ${
                    darkMode ? "text-gray-400" : "text-gray-600"
                  }`}
                  title="Delete Resume"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
