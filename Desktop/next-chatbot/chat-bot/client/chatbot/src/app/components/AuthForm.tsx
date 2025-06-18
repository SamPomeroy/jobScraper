"use client";
import { useState, useEffect } from "react";
import { signUp, signIn, getUser } from "../api/auth/auth";
import { User } from "@supabase/supabase-js"; 

export default function AuthForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState<User | null>(null); 

  useEffect(() => {
    const fetchUser = async () => {
      const currentUser = await getUser();
      setUser(currentUser);
    };
    fetchUser();
  }, []);

  const handleSignup = async () => {
    await signUp(email, password);
    const currentUser = await getUser();
    setUser(currentUser);
  };

  const handleLogin = async () => {
    await signIn(email, password);
    const currentUser = await getUser();
    setUser(currentUser);
  };

  return (
    <div className="flex flex-col items-center p-8">
      <h1 className="text-xl font-bold">Authenticate</h1>
      {user ? (
        <p className="text-green-500">Logged in as: {user.email}</p>
      ) : (
        <>
          <input
            type="email"
            className="border p-2 rounded"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            className="border p-2 rounded mt-2"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleSignup} className="mt-2 p-2 bg-green-500 text-white rounded">
            Sign Up
          </button>
          <button onClick={handleLogin} className="mt-2 p-2 bg-blue-500 text-white rounded">
            Log In
          </button>
        </>
      )}
    </div>
  );
}
