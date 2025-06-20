"use-client";
export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-gray-900">
            About Bayan Labs: JobTracker
          </h1>
          <p className="mt-4 text-xl text-gray-600">
            Empowering job seekers to stay focused, organized, and confidently
            pursue their careers
          </p>
        </div>

        <div className="mt-16 bg-white rounded-lg shadow-lg p-8">
          <div className="prose max-w-none">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Our Mission
            </h2>
            <p className="text-gray-600 mb-6">
              At Bayan Labs, we built JobTracker to simplify the job search
              process. From juggling application deadlines to following up with
              recruiters, staying organized is tough — and that’s the problem
              we’re solving.
            </p>

            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-gray-600 mb-6">
              At Bayan Labs, we built JobTracker to simplify the job search
              process. From juggling application deadlines to following up with
              recruiters, staying organized is tough — and that’s the problem
              we’re solving.
            </p>

            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Key Features
            </h2>
            <ul className="list-disc list-inside text-gray-600 mb-6 space-y-2">
              <li>Real-time job listings from trusted sources</li>
              <li>Personalized tracking of application status</li>
              <li>Document uploads and resume versioning</li>
              <li>Automated interview reminders and task notes</li>
              <li>Insights and stats to improve your search strategy</li>
              <li>
                Secure and scalable data infrastructure powered by Supabase
              </li>
            </ul>

            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Get Started Today
            </h2>
            <p className="text-gray-600">
              Ready to take control of your job search? Sign up today and
              experience the difference an organized approach can make in
              landing your next opportunity.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
