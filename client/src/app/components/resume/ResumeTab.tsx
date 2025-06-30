"use client";

import React, { useState, useRef, useEffect } from "react";
import { FileText, Upload, Trash2, Eye, Star } from "lucide-react";
import { Resume } from "../../types/application";
import type { AuthUser } from "../../types/application";
import { supabase } from "../../supabase/client";

interface ResumeTabProps {
  user: AuthUser;
  darkMode: boolean;
}

export const ResumeTab: React.FC<ResumeTabProps> = ({ user, darkMode }) => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [uploading, setUploading] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [compareResults, setCompareResults] = useState<Record<
    string,
    { score: number; skills: string[] }
  >>({});

  const [showModal, setShowModal] = useState<{ id: string; visible: boolean }>({
    id: "",
    visible: false,
  });

  useEffect(() => {
    const fetchResumes = async () => {
      const { data, error } = await supabase
        .from("resumes")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", { ascending: false });

      if (data) setResumes(data);
      if (error) console.error("Fetch error:", error.message);
    };

    fetchResumes();
  }, [user.id]);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setUploading(true);
    const filePath = `user-${user.id}/${file.name}`;

    const { error: uploadError } = await supabase.storage
      .from("resumes")
      .upload(filePath, file, { upsert: true });

    if (uploadError) {
      console.error("Upload failed:", uploadError.message);
      setUploading(false);
      return;
    }

    const { data: publicUrlData } = supabase.storage
      .from("resumes")
      .getPublicUrl(filePath);

    const publicUrl = publicUrlData?.publicUrl;

    const { error: insertError } = await supabase.from("resumes").insert({
      user_id: user.id,
      file_name: file.name,
      file_path: publicUrl,
      is_default: false,
      updated_at: new Date().toISOString(),
    });

    if (insertError) {
      console.error("Insert failed:", insertError.message);
    } else {
      const { data: updatedResumes, error: fetchError } = await supabase
        .from("resumes")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", { ascending: false });

      if (updatedResumes) setResumes(updatedResumes);
      if (fetchError) console.error("Refresh failed:", fetchError.message);
    }

    setUploading(false);
  };

  const handleCompare = async (resumeId: string, resumeText: string) => {
    try {
      const response = await fetch("http://localhost:5678/compare-resume", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: user.id,
          resume_text: resumeText,
        }),
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
      alert("Something went wrong comparing this resume.");
    }
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
              darkMode ? "border-gray-600 hover:bg-gray-700" : "border-gray-200 hover:bg-gray-50"
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="w-8 h-8 text-blue-600" />
                <div>
                  <h3 className={`font-medium flex items-center ${darkMode ? "text-gray-100" : "text-gray-900"}`}>
                    {resume.file_name}
                    {resume.is_default && (
                      <Star className="w-4 h-4 text-yellow-500 ml-2 fill-current" />
                    )}
                  </h3>
                  <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
                    {resume.updated_at
                      ? `Updated ${new Date(resume.updated_at).toLocaleDateString()}`
                      : "Updated time unknown"}
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => window.open(resume.file_path, "_blank")}
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
                      : `hover:text-yellow-500 ${darkMode ? "text-gray-400" : "text-gray-600"}`
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
                <button
                  onClick={async () => {
                    const { data, error } = await supabase
                      .from("resumes")
                      .select("resume_text")
                      .eq("id", resume.id)
                      .single();

                    if (data?.resume_text) {
                      handleCompare(resume.id, data.resume_text);
                    } else {
                      alert("No résumé text available for this file.");
                    }
                  }}
                  className={`p-2 hover:text-green-600 transition-colors ${
                    darkMode ? "text-gray-400" : "text-gray-600"
                  }`}
                  title="Compare Resume"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
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
