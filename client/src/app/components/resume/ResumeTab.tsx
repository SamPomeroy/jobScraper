"use client";

import React, { useState, useRef, useEffect } from "react";
import { FileText, Upload, Trash2, Eye, Star } from "lucide-react";

interface Resume {
  id: string;
  file_name: string;
  file_url: string;
  is_default: boolean;
  updated_at: string;
  resume_text?: string;
}

interface AuthUser {
  id: string;
  email: string;
}

interface ResumeTabProps {
  user: AuthUser;
  darkMode: boolean;
}

export const ResumeTab: React.FC<ResumeTabProps> = ({ user, darkMode }) => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [compareResults, setCompareResults] = useState<Record<string, { score: number; skills: string[] }>>({});
  const [showModal, setShowModal] = useState<{ id: string; visible: boolean }>({ id: "", visible: false });

  useEffect(() => {
    const stored = localStorage.getItem(`resumes-${user.id}`);
    if (stored) setResumes(JSON.parse(stored));
  }, [user.id]);

  const saveToLocal = (data: Resume[]) => {
    localStorage.setItem(`resumes-${user.id}`, JSON.stringify(data));
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);

    try {
      const reader = new FileReader();
      reader.onload = () => {
        const resumeText = reader.result?.toString() || "";

        const newResume: Resume = {
          id: `${Date.now()}-${Math.random()}`,
          file_name: file.name,
          file_url: URL.createObjectURL(file),
          is_default: false,
          updated_at: new Date().toISOString(),
          resume_text: resumeText,
        };

        const updated = [newResume, ...resumes];
        setResumes(updated);
        saveToLocal(updated);
        alert("Resume uploaded locally!");
      };

      reader.readAsText(file);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed.");
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleCompare = async (resumeId: string, resumeText: string) => {
    try {
      const response = await fetch("http://snoe.app.n8n.cloud/webhook-test/compare-resume ", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user.id, resume_text: resumeText }),
      });

      const result = await response.json();

      setCompareResults((prev) => ({
        ...prev,
        [resumeId]: {
          score: result.matchScore,
          skills: result.matchedSkills || [],
        },
      }));

      setShowModal({ id: resumeId, visible: true });
    } catch (err) {
      console.error("Compare failed:", err);
      alert("Error comparing resume.");
    }
  };

  const setDefaultResume = (id: string) => {
    const updated = resumes.map((r) => ({ ...r, is_default: r.id === id }));
    setResumes(updated);
    saveToLocal(updated);
  };

  const deleteResume = (id: string) => {
    const updated = resumes.filter((r) => r.id !== id);
    setResumes(updated);
    saveToLocal(updated);
  };

  return (
    <div className={`${darkMode ? "bg-gray-800" : "bg-white"} rounded-lg shadow p-6`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className={`text-2xl font-bold flex items-center ${darkMode ? "text-gray-100" : "text-gray-900"}`}>
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
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={handleFileUpload}
        />
      </div>

      <div className="grid gap-4">
        {resumes.map((resume) => (
          <div
            key={resume.id}
            className={`border rounded-lg p-4 hover:shadow-md transition-shadow ${
              darkMode ? "border-gray-600 hover:bg-gray-700" : "border-gray-200 hover:bg-gray-50"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="w-8 h-8 text-blue-600" />
                <div>
                  <h3 className={`font-medium flex items-center ${darkMode ? "text-gray-100" : "text-gray-900"}`}>
                    {resume.file_name}
                    {resume.is_default && <Star className="w-4 h-4 text-yellow-500 ml-2 fill-current" />}
                  </h3>
                  <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
                    Updated {new Date(resume.updated_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button onClick={() => window.open(resume.file_url, "_blank")} title="View Resume">
                  <Eye className="w-4 h-4 text-blue-600" />
                </button>
                <button onClick={() => setDefaultResume(resume.id)} title="Set as Default">
                  <Star
                    className={`w-4 h-4 ${
                      resume.is_default ? "text-yellow-500" : darkMode ? "text-gray-400" : "text-gray-600"
                    }`}
                  />
                </button>
                <button onClick={() => deleteResume(resume.id)} title="Delete Resume">
                  <Trash2 className="w-4 h-4 text-red-500" />
                </button>
                <button
                  onClick={() =>
                    resume.resume_text
                      ? handleCompare(resume.id, resume.resume_text)
                      : alert("Resume text not found for comparison.")
                  }
                  title="Compare Resume"
                >
                  <svg className="w-4 h-4 text-green-600" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                    <path d="M10 14L21 3m0 0v7m0-7h-7" />
                    <path d="M3 10v11h11" />
                  </svg>
                </button>
              </div>
            </div>
            {compareResults[resume.id] && (
              <div className={`mt-4 text-sm ${darkMode ? "text-green-300" : "text-green-700"}`}>
                ✅ Match Score: <strong>{compareResults[resume.id].score}%</strong> — Top Skills:{" "}
                {compareResults[resume.id].skills.slice(0, 5).join(", ") || "none"}
              </div>
            )}
          </div>
        ))}
      </div>

      {showModal.visible && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
          <div className={`rounded-lg max-w-lg w-full p-6 shadow-lg ${darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"}`}>
            <h2 className="text-xl font-bold mb-4">🧠 Résumé Match Results</h2>
            <p className="mb-2">
              <strong>Match Score:</strong> {compareResults[showModal.id]?.score ?? "—"}%
            </p>
            <p className="mb-2"><strong>Matched Skills:</strong></p>
            <div className="text-sm max-h-40 overflow-y-auto border rounded p-3 bg-gray-100 dark:bg-gray-700">
              {compareResults[showModal.id]?.skills?.length ? (
                <ul className="list-disc pl-5 space-y-1">
                  {compareResults[showModal.id].skills.map((skill, i) => (
                    <li key={i}>{skill}</li>
                  ))}
                </ul>
              ) : (
                <p>No significant skills matched.</p>
              )}
            </div>
            <div className="flex justify-end mt-4">
              <button
                onClick={() => setShowModal({ id: "", visible: false })}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};