"use client";

import React, { useState, useRef } from "react";
import { FileText, Upload, Trash2, Eye, Star } from "lucide-react";
import type { AuthUser } from "../../types/auth";

// Define the type for our resume objects
interface Resume {
  id: string;
  name: string;
  file_name: string;
  file_url: string;
  created_at: string;
  updated_at: string;
  is_default: boolean;
}

// Define the props for this component
interface ResumeManagementProps {
  user: AuthUser;
}

export const ResumeManagement: React.FC<ResumeManagementProps> = ({ user }) => {
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
  
  // Explicitly type the file input ref as HTMLInputElement or null
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Type the event as a React change event for an HTML input element
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
        name: file.name.replace(".pdf", ""),
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

  // Define helper functions with their parameter types

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
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <FileText className="w-6 h-6 mr-2" />
          Resume Management
        </h2>
        <button
          onClick={() => fileInputRef.current?.click()}
          disabled={uploading}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
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
            className="border rounded-lg p-4 hover:shadow-md transition-shadow"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="w-8 h-8 text-blue-600" />
                <div>
                  <h3 className="font-medium text-gray-900 flex items-center">
                    {resume.name}
                    {resume.is_default && (
                      <Star className="w-4 h-4 text-yellow-500 ml-2 fill-current" />
                    )}
                  </h3>
                  <p className="text-sm text-gray-500">
                    Updated {new Date(resume.updated_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => window.open(resume.file_url, "_blank")}
                  className="p-2 text-gray-600 hover:text-blue-600"
                  title="View Resume"
                >
                  <Eye className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setDefaultResume(resume.id)}
                  className={`p-2 ${
                    resume.is_default
                      ? "text-yellow-500"
                      : "text-gray-600 hover:text-yellow-500"
                  }`}
                  title="Set as Default"
                >
                  <Star className="w-4 h-4" />
                </button>
                <button
                  onClick={() => deleteResume(resume.id)}
                  className="p-2 text-gray-600 hover:text-red-600"
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
