"use client";
import React, { useState } from "react";
import { Mail, Info } from "lucide-react";
import { useTheme } from '@/app/context/ThemeContext';

export default function ContactPage() {
  const { darkMode } = useTheme();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Simulate form submission
    setTimeout(() => {
      setLoading(false);
      setSuccess(true);
      setFormData({ name: "", email: "", subject: "", message: "" });
    }, 1000);
  };

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div 
      style={{
        backgroundColor: 'var(--bg-color)',
        color: 'var(--text-color)'
      }}
      className={`min-h-screen py-16 transition-colors duration-200 ${
        darkMode ? 'bg-gray-900' : 'bg-gray-50'
      }`}
    >
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 
            className={`text-4xl font-extrabold transition-colors duration-200 ${
              darkMode ? 'text-gray-100' : 'text-gray-900'
            }`}
          >
            Contact Us – Bayan Labs Job Application Platform
          </h1>
          <p 
            className={`mt-4 text-xl transition-colors duration-200 ${
              darkMode ? 'text-gray-400' : 'text-gray-600'
            }`}
          >
            Have questions? We'd love to hear from you.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Info */}
          <div>
            <h2 
              className={`text-2xl font-bold mb-6 transition-colors duration-200 ${
                darkMode ? 'text-gray-100' : 'text-gray-900'
              }`}
            >
              Get in Touch
            </h2>
            <div className="space-y-6">
              <div className="flex items-start">
                <Mail className="w-6 h-6 text-blue-600 mt-1" />
                <div className="ml-4">
                  <h3 
                    className={`text-lg font-medium transition-colors duration-200 ${
                      darkMode ? 'text-gray-200' : 'text-gray-900'
                    }`}
                  >
                    Email
                  </h3>
                  <p 
                    className={`transition-colors duration-200 ${
                      darkMode ? 'text-gray-400' : 'text-gray-600'
                    }`}
                  >
                    support@jobtracker.com
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <Info className="w-6 h-6 text-blue-600 mt-1" />
                <div className="ml-4">
                  <h3 
                    className={`text-lg font-medium transition-colors duration-200 ${
                      darkMode ? 'text-gray-200' : 'text-gray-900'
                    }`}
                  >
                    Support Hours
                  </h3>
                  <p 
                    className={`transition-colors duration-200 ${
                      darkMode ? 'text-gray-400' : 'text-gray-600'
                    }`}
                  >
                    Monday - Friday: 9:00 AM - 6:00 PM EST
                    <br />
                    Saturday - Sunday: 10:00 AM - 4:00 PM EST
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-8">
              <h3 
                className={`text-lg font-medium mb-4 transition-colors duration-200 ${
                  darkMode ? 'text-gray-200' : 'text-gray-900'
                }`}
              >
                Contact Us – Bayan Labs Job Application Platform
              </h3>
              <div className="space-y-4">
                <div>
                  <h4 
                    className={`font-medium transition-colors duration-200 ${
                      darkMode ? 'text-gray-300' : 'text-gray-800'
                    }`}
                  >
                    Bayan Labs Job Application Platform Welcome to the official
                    contact portal for the Bayan Labs Job Application Platform.
                    Whether you're a job seeker, recruiter, or curious visitor,
                    we'd love to hear from you. Our platform is designed to
                    streamline job discovery by intelligently scraping
                    opportunities from major job boards — securely and
                    efficiently
                  </h4>
                </div>
                <div>
                  <h4 
                    className={`font-medium transition-colors duration-200 ${
                      darkMode ? 'text-gray-300' : 'text-gray-800'
                    }`}
                  >
                    If you have questions, feedback, or need support, send us a
                    message below. Our team is committed to helping you navigate
                    the platform and ensure a smooth hiring or job-finding
                    experience
                  </h4>
                  <p 
                    className={`text-sm mt-2 transition-colors duration-200 ${
                      darkMode ? 'text-gray-500' : 'text-gray-600'
                    }`}
                  >
                    All messages are securely stored and monitored by our admin
                    team to ensure timely responses and ongoing platform
                    improvement.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div 
            className={`rounded-lg shadow-lg p-8 transition-colors duration-200 ${
              darkMode ? 'bg-gray-800' : 'bg-white'
            }`}
          >
            <h2 
              className={`text-2xl font-bold mb-6 transition-colors duration-200 ${
                darkMode ? 'text-gray-100' : 'text-gray-900'
              }`}
            >
              Send us a Message
            </h2>

            {success && (
              <div className="mb-6 bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md dark:bg-green-900/20 dark:border-green-800 dark:text-green-400">
                Thank you for your message! We'll get back to you soon.
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="name"
                  className={`block text-sm font-medium transition-colors duration-200 ${
                    darkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}
                >
                  Name
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 ${
                    darkMode 
                      ? 'border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400' 
                      : 'border-gray-300 bg-white text-gray-900'
                  }`}
                />
              </div>

              <div>
                <label
                  htmlFor="email"
                  className={`block text-sm font-medium transition-colors duration-200 ${
                    darkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}
                >
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 ${
                    darkMode 
                      ? 'border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400' 
                      : 'border-gray-300 bg-white text-gray-900'
                  }`}
                />
              </div>

              <div>
                <label
                  htmlFor="subject"
                  className={`block text-sm font-medium transition-colors duration-200 ${
                    darkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}
                >
                  Subject
                </label>
                <input
                  type="text"
                  id="subject"
                  name="subject"
                  required
                  value={formData.subject}
                  onChange={handleInputChange}
                  className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 ${
                    darkMode 
                      ? 'border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400' 
                      : 'border-gray-300 bg-white text-gray-900'
                  }`}
                />
              </div>

              <div>
                <label
                  htmlFor="message"
                  className={`block text-sm font-medium transition-colors duration-200 ${
                    darkMode ? 'text-gray-300' : 'text-gray-700'
                  }`}
                >
                  Message
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={4}
                  required
                  value={formData.message}
                  onChange={handleInputChange}
                  className={`mt-1 block w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 transition-colors duration-200 ${
                    darkMode 
                      ? 'border-gray-600 bg-gray-700 text-gray-100 placeholder-gray-400' 
                      : 'border-gray-300 bg-white text-gray-900'
                  }`}
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 transition-colors duration-200"
              >
                {loading ? "Sending..." : "Send Message"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}


// "use client";
// import React, { useState } from "react";
// import { Mail, Info } from "lucide-react";
// export default function ContactPage() {
//   const [formData, setFormData] = useState({
//     name: "",
//     email: "",
//     subject: "",
//     message: "",
//   });
//   const [loading, setLoading] = useState(false);
//   const [success, setSuccess] = useState(false);

//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);

//     // Simulate form submission
//     setTimeout(() => {
//       setLoading(false);
//       setSuccess(true);
//       setFormData({ name: "", email: "", subject: "", message: "" });
//     }, 1000);
//   };

//   const handleInputChange = (
//     e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
//   ) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   return (
//     <div className="min-h-screen bg-gray-50 py-16">
//       <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
//         <div className="text-center">
//           <h1 className="text-4xl font-extrabold text-gray-900">
//             Contact Us – Bayan Labs Job Application Platform
//           </h1>
//           <p className="mt-4 text-xl text-gray-600">
//             Have questions? We'd love to hear from you.
//           </p>
//         </div>

//         <div className="mt-16 grid grid-cols-1 lg:grid-cols-2 gap-12">
//           {/* Contact Info */}
//           <div>
//             <h2 className="text-2xl font-bold text-gray-900 mb-6">
//               Get in Touch
//             </h2>
//             <div className="space-y-6">
//               <div className="flex items-start">
//                 <Mail className="w-6 h-6 text-blue-600 mt-1" />
//                 <div className="ml-4">
//                   <h3 className="text-lg font-medium text-gray-900">Email</h3>
//                   <p className="text-gray-600">support@jobtracker.com</p>
//                 </div>
//               </div>
//               <div className="flex items-start">
//                 <Info className="w-6 h-6 text-blue-600 mt-1" />
//                 <div className="ml-4">
//                   <h3 className="text-lg font-medium text-gray-900">
//                     Support Hours
//                   </h3>
//                   <p className="text-gray-600">
//                     Monday - Friday: 9:00 AM - 6:00 PM EST
//                     <br />
//                     Saturday - Sunday: 10:00 AM - 4:00 PM EST
//                   </p>
//                 </div>
//               </div>
//             </div>

//             <div className="mt-8">
//               <h3 className="text-lg font-medium text-gray-900 mb-4">
//                 Contact Us – Bayan Labs Job Application Platform
//               </h3>
//               <div className="space-y-4">
//                 <div>
//                   <h4 className="font-medium text-gray-800">
//                     {" "}
//                     Bayan Labs Job Application Platform Welcome to the official
//                     contact portal for the Bayan Labs Job Application Platform.
//                     Whether you're a job seeker, recruiter, or curious visitor,
//                     we’d love to hear from you. Our platform is designed to
//                     streamline job discovery by intelligently scraping
//                     opportunities from major job boards — securely and
//                     efficiently
//                   </h4>
//                   <p className="text-sm text-gray-600">
                  
//                   </p>
//                 </div>
//                 <div>
//                   <h4 className="font-medium text-gray-800">
//                     If you have questions, feedback, or need support, send us a
//                     message below. Our team is committed to helping you navigate
//                     the platform and ensure a smooth hiring or job-finding
//                     experience
//                   </h4>
//                   <p className="text-sm text-gray-600">
//                     All messages are securely stored and monitored by our admin
//                     team to ensure timely responses and ongoing platform
//                     improvement.
//                   </p>
//                 </div>
//               </div>
//             </div>
//           </div>

//           {/* Contact Form */}
//           <div className="bg-white rounded-lg shadow-lg p-8">
//             <h2 className="text-2xl font-bold text-gray-900 mb-6">
//               Send us a Message
//             </h2>

//             {success && (
//               <div className="mb-6 bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-md">
//                 Thank you for your message! We'll get back to you soon.
//               </div>
//             )}

//             <form onSubmit={handleSubmit} className="space-y-6">
//               <div>
//                 <label
//                   htmlFor="name"
//                   className="block text-sm font-medium text-gray-700"
//                 >
//                   Name
//                 </label>
//                 <input
//                   type="text"
//                   id="name"
//                   name="name"
//                   required
//                   value={formData.name}
//                   onChange={handleInputChange}
//                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
//                 />
//               </div>

//               <div>
//                 <label
//                   htmlFor="email"
//                   className="block text-sm font-medium text-gray-700"
//                 >
//                   Email
//                 </label>
//                 <input
//                   type="email"
//                   id="email"
//                   name="email"
//                   required
//                   value={formData.email}
//                   onChange={handleInputChange}
//                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
//                 />
//               </div>

//               <div>
//                 <label
//                   htmlFor="subject"
//                   className="block text-sm font-medium text-gray-700"
//                 >
//                   Subject
//                 </label>
//                 <input
//                   type="text"
//                   id="subject"
//                   name="subject"
//                   required
//                   value={formData.subject}
//                   onChange={handleInputChange}
//                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
//                 />
//               </div>

//               <div>
//                 <label
//                   htmlFor="message"
//                   className="block text-sm font-medium text-gray-700"
//                 >
//                   Message
//                 </label>
//                 <textarea
//                   id="message"
//                   name="message"
//                   rows={4}
//                   required
//                   value={formData.message}
//                   onChange={handleInputChange}
//                   className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
//                 />
//               </div>

//               <button
//                 type="submit"
//                 disabled={loading}
//                 className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
//               >
//                 {loading ? "Sending..." : "Send Message"}
//               </button>
//             </form>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }
