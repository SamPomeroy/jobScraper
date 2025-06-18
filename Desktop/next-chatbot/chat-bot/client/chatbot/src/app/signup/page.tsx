// Enhanced SignUp Component
"use client";

import React, { useState } from "react";
import { signUp } from "../api/auth/auth";

export default function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const validatePassword = (password: string) => {
    if (password.length < 8) {
      return "Password must be at least 8 characters long";
    }
    if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password)) {
      return "Password must contain at least one uppercase letter, one lowercase letter, and one number";
    }
    return null;
  };

  const handleSignUp = async (e?: React.FormEvent) => {
    e?.preventDefault();
    setError(null);

    // Validation
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    setIsLoading(true);
    
    try {
      const user = await signUp(email.trim().toLowerCase(), password);
      if (!user) {
        setError("Sign-up failed. Please try again.");
      } else {
        // Success feedback
        const successMessage = document.createElement('div');
        successMessage.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
        successMessage.textContent = 'Account created successfully! Please check your email for confirmation. ✅';
        document.body.appendChild(successMessage);
        
        setTimeout(() => {
          document.body.removeChild(successMessage);
          window.location.href = "/signin";
        }, 3000);
        
        setEmail("");
        setPassword("");
        setConfirmPassword("");
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during sign-up. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const getPasswordStrength = (password: string) => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    return strength;
  };

  const passwordStrength = getPasswordStrength(password);
  const strengthColors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];
  const strengthLabels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 flex items-center justify-center p-4">
      {/* Animated background elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-1/2 -right-1/2 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute -bottom-1/2 -left-1/2 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-green-500/5 rounded-full blur-3xl animate-pulse delay-500"></div>
      </div>

      <div className="relative bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl p-8 w-full max-w-md border border-white/20">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-green-500 to-blue-600 rounded-2xl flex items-center justify-center mb-4 shadow-lg">
            <span className="text-2xl">✨</span>
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-slate-800 to-slate-600 bg-clip-text text-transparent mb-2">
            Join Us Today
          </h1>
          <p className="text-slate-600">Create your account and start learning</p>
        </div>

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 shadow-sm">
            <div className="flex items-center">
              <span className="mr-2">⚠️</span>
              <p className="text-sm font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSignUp} className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Email Address
            </label>
            <div className="relative">
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 pl-11 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
                required
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                📧
              </span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Create a strong password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 pl-11 pr-11 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
                required
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                🔒
              </span>
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors duration-200"
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
            
            {/* Password strength indicator */}
            {password && (
              <div className="mt-2">
                <div className="flex space-x-1 mb-1">
                  {[...Array(5)].map((_, index) => (
                    <div
                      key={index}
                      className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                        index < passwordStrength ? strengthColors[passwordStrength - 1] : 'bg-slate-200'
                      }`}
                    ></div>
                  ))}
                </div>
                <p className="text-xs text-slate-600">
                  Password strength: <span className="font-medium">{strengthLabels[passwordStrength - 1] || 'Very Weak'}</span>
                </p>
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-semibold text-slate-700 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <input
                type={showConfirmPassword ? "text" : "password"}
                placeholder="Confirm your password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full px-4 py-3 pl-11 pr-11 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 outline-none bg-white/80 backdrop-blur-sm"
                required
              />
              <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400">
                🔐
              </span>
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors duration-200"
              >
                {showConfirmPassword ? "🙈" : "👁️"}
              </button>
            </div>
            {confirmPassword && password !== confirmPassword && (
              <p className="text-red-500 text-xs mt-1">Passwords do not match</p>
            )}
            {confirmPassword && password === confirmPassword && confirmPassword.length > 0 && (
              <p className="text-green-500 text-xs mt-1">✓ Passwords match</p>
            )}
          </div>

          <button
            type="submit"
            disabled={isLoading || !email || !password || !confirmPassword || password !== confirmPassword}
            className="w-full bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 disabled:from-slate-400 disabled:to-slate-500 text-white font-semibold py-3 px-4 rounded-xl transition-all duration-300 transform hover:scale-[1.02] disabled:hover:scale-100 shadow-lg hover:shadow-green-500/25 disabled:shadow-none"
          >
            {isLoading ? (
              <div className="flex items-center justify-center space-x-2">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Creating Account...</span>
              </div>
            ) : (
              <div className="flex items-center justify-center space-x-2">
                <span>🚀</span>
                <span>Create Account</span>
              </div>
            )}
          </button>
        </form>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-slate-600">
            Already have an account?{" "}
            <a 
              href="/signin" 
              className="text-blue-600 hover:text-blue-700 font-semibold hover:underline transition-all duration-200"
            >
              Sign In
            </a>
          </p>
        </div>

        {/* Terms */}
        <div className="mt-6 text-center">
          <p className="text-xs text-slate-500">
            By creating an account, you agree to our{" "}
            <a href="#" className="text-blue-600 hover:underline">Terms of Service</a>
            {" and "}
            <a href="#" className="text-blue-600 hover:underline">Privacy Policy</a>
          </p>
        </div>

            {/* Decorative elements */}
            <div className="absolute -z-10 top-4 right-4 w-24 h-24 bg-gradient-to-br from-green-400/20 to-blue-500/20 rounded-full blur-xl"></div>
            <div className="absolute -z-10 bottom-4 left-4 w-16 h-16 bg-gradient-to-br from-blue-400/20 to-purple-500/20 rounded-full blur-xl"></div>
          </div>
        </div>
  )
}