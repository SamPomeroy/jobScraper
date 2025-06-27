// import { useState } from "react";
// import { AuthUser } from "@supabase/supabase-js";
// import { supabase } from "@/app/supabase/client";

// function LoginPage({
//   onSuccess,
//   setCurrentPage,
// }: {
//   onSuccess: (user: AuthUser) => void;
//   setCurrentPage: (page: string) => void;
// }) {
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState("");

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     setError("");

//     try {
//       const { data, error } = await supabase.auth.signInWithPassword({
//         email,
//         password,
//       });

//       if (error) throw error;

//       if (data.user) {
//         onSuccess(data.user as AuthUser);
//         setCurrentPage("dashboard");
//       }
//     } catch (error: any) {
//       setError(error.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div
//       style={{
//         backgroundColor: "var(--bg-color)",
//         color: "var(--text-color)",
//       }}
//       className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
//     >
//       <div className="max-w-md w-full space-y-8">
//         <div>
//           <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
//             Sign in to your account
//           </h2>
//           <p className="mt-2 text-center text-sm text-gray-600">
//             Don't have an account?{" "}
//             <button
//               onClick={() => setCurrentPage("register")}
//               className="font-medium text-blue-600 hover:text-blue-500"
//             >
//               Sign up
//             </button>
//           </p>
//         </div>

//         <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
//           <div className="space-y-4">
//             <div>
//               <label
//                 htmlFor="email"
//                 className="block text-sm font-medium text-gray-700"
//               >
//                 Email address
//               </label>
//               <input
//                 id="email"
//                 name="email"
//                 type="email"
//                 autoComplete="email"
//                 required
//                 value={email}
//                 onChange={(e) => setEmail(e.target.value)}
//                 className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
//                 placeholder="Enter your email"
//               />
//             </div>

//             <div>
//               <label
//                 htmlFor="password"
//                 className="block text-sm font-medium text-gray-700"
//               >
//                 Password
//               </label>
//               <input
//                 id="password"
//                 name="password"
//                 type="password"
//                 autoComplete="current-password"
//                 required
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
//                 placeholder="Enter your password"
//               />
//             </div>
//           </div>

//           {error && (
//             <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-md text-sm">
//               {error}
//             </div>
//           )}

//           <div>
//             <button
//               type="submit"
//               disabled={loading}
//               className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
//             >
//               {loading ? "Processing..." : "Sign in"}
//             </button>
//           </div>
//         </form>
//       </div>
//     </div>
//   );
// }

// export default LoginPage;
