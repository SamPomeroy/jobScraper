import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

const zodiac_signs = [
  "aries", "taurus", "gemini", "cancer", "leo", "virgo",
  "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
];

const Horoscope = ({ sign }) => {
  const [horoscope, setHoroscope] = useState({ daily: {}, monthly: {}, yearly: {} });
  const [activeTab, setActiveTab] = useState("daily");

  useEffect(() => {
    if (!sign) return;

    fetch("/horoscopes.json")
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched Horoscope Data:", data); // Debugging

        const cleanText = (text) => (text ? text.trim() : "Not available"); 

        setHoroscope({
          daily: {
            summary: cleanText(data[sign]?.daily?.summary),
            ratings: data[sign]?.daily?.ratings || {},
          },
          monthly: {
            overview: cleanText(data[sign]?.monthly?.overview),
            key_dates: data[sign]?.monthly?.key_dates || [],
          },
          yearly: {
            highlights: cleanText(data[sign]?.yearly?.highlights),
            forecast: cleanText(data[sign]?.yearly?.forecast),
          },
        });
      })
      .catch((error) => console.error("Error fetching horoscope:", error));
  }, [sign]);

  return (
    <div>
      <h2>{sign.charAt(0).toUpperCase() + sign.slice(1)} Horoscope</h2>

      <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
        <button onClick={() => setActiveTab("daily")}>🌟 Daily</button>
        <button onClick={() => setActiveTab("monthly")}>📅 Monthly</button>
        <button onClick={() => setActiveTab("yearly")}>📆 Yearly</button>
      </div>

      {activeTab === "daily" && (
        <div style={{ padding: "15px", borderRadius: "8px", background: "#f9f9f9", border: "1px solid #ccc" }}>
          <h3>🌟 Daily Horoscope</h3>
          <p>{horoscope.daily.summary}</p>
        </div>
      )}

      {activeTab === "monthly" && (
        <div style={{ padding: "15px", borderRadius: "8px", background: "#f5f5f5", border: "1px solid #bbb", marginTop: "10px" }}>
          <h3>📅 Monthly Horoscope</h3>
          <p>{horoscope.monthly.overview}</p>
          {horoscope.monthly.key_dates.length > 0 && (
            <ul>{horoscope.monthly.key_dates.map((date, index) => <li key={index}>{date}</li>)}</ul>
          )}
        </div>
      )}

      {activeTab === "yearly" && (
        <div style={{ padding: "15px", borderRadius: "8px", background: "#eef", border: "1px solid #aaa", marginTop: "10px" }}>
          <h3>📆 Yearly Horoscope</h3>
          <p><strong>Highlights:</strong> {horoscope.yearly.highlights}</p>
          <p><strong>Forecast:</strong> {horoscope.yearly.forecast}</p>
        </div>
      )}

      <div style={{ marginTop: "20px" }}>
        {zodiac_signs.map((zodiacSign) => (
          <Link key={zodiacSign} to={`/${zodiacSign}`}>
            <button>{zodiacSign.charAt(0).toUpperCase() + zodiacSign.slice(1)}</button>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Horoscope;


// import { useState, useEffect } from "react";
// import { Link } from "react-router-dom";

// const zodiac_signs = [
//   "aries", "taurus", "gemini", "cancer", "leo", "virgo",
//   "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
// ];

// const Horoscope = ({ sign }) => {
//   const [horoscope, setHoroscope] = useState({ daily: {}, monthly: {}, yearly: {} });
//   const [activeTab, setActiveTab] = useState("daily");

//   useEffect(() => {
//     if (!sign) return;

//     fetch("/horoscopes.json")
//       .then((response) => response.json())
//       .then((data) => {
//         console.log("Fetched Horoscope Data:", data); // Debugging

//         // Function to clean text and handle undefined values
//         const cleanText = (text) => {
//           if (!text) return "Not available."; // Prevents errors
//           return text.replace(/\u00a0/g, " ").replace(/\u2013/g, "-").trim();
//         };

//         // Format JSON before setting state
//         setHoroscope({
//           daily: {
//             summary: cleanText(data[sign]?.daily?.summary),
//             ratings: data[sign]?.daily?.ratings || {},
//           },
//           monthly: {
//             overview: cleanText(data[sign]?.monthly?.overview),
//             key_dates: data[sign]?.monthly?.key_dates || [],
//           },
//           yearly: {
//             highlights: cleanText(data[sign]?.yearly?.highlights),
//             forecast: cleanText(data[sign]?.yearly?.forecast),
//           },
//         });
//       })
//       .catch((error) => console.error("Error fetching horoscope:", error));
//   }, [sign]);

//   return (
//     <div>
//       <h2>{sign.charAt(0).toUpperCase() + sign.slice(1)} Horoscope</h2>

//       {/* Tabs for navigation */}
//       <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
//         <button onClick={() => setActiveTab("daily")}>🌟 Daily</button>
//         <button onClick={() => setActiveTab("monthly")}>📅 Monthly</button>
//         <button onClick={() => setActiveTab("yearly")}>📆 Yearly</button>
//       </div>

//       {/* Daily Horoscope */}
//       {activeTab === "daily" && (
//         <div style={{ padding: "15px", borderRadius: "8px", background: "#f9f9f9", border: "1px solid #ccc" }}>
//           <h3>🌟 Daily Horoscope</h3>
//           <p>{horoscope.daily.summary || "Horoscope not available."}</p>
//         </div>
//       )}

//       {/* Monthly Horoscope */}
//       {activeTab === "monthly" && (
//         <div style={{ padding: "15px", borderRadius: "8px", background: "#f5f5f5", border: "1px solid #bbb", marginTop: "10px" }}>
//           <h3>📅 Monthly Horoscope</h3>
//           <p>{horoscope.monthly.overview}</p>
//           {horoscope.monthly.key_dates.length > 0 && (
//             <>
//               <h4>🌙 Key Dates</h4>
//               <ul>
//                 {horoscope.monthly.key_dates.map((date, index) => (
//                   <li key={index}>{date}</li>
//                 ))}
//               </ul>
//             </>
//           )}
//         </div>
//       )}

//       {/* Yearly Horoscope */}
//       {activeTab === "yearly" && (
//         <div style={{ padding: "15px", borderRadius: "8px", background: "#eef", border: "1px solid #aaa", marginTop: "10px" }}>
//           <h3>📆 Yearly Horoscope</h3>
//           <p><strong>Highlights:</strong> {horoscope.yearly.highlights}</p>
//           <p><strong>Forecast:</strong> {horoscope.yearly.forecast}</p>
//         </div>
//       )}

//       {/* Zodiac Sign Navigation */}
//       <div style={{ marginTop: "20px" }}>
//         {zodiac_signs.map((zodiacSign) => (
//           <Link key={zodiacSign} to={`/${zodiacSign}`}>
//             <button>{zodiacSign.charAt(0).toUpperCase() + zodiacSign.slice(1)}</button>
//           </Link>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default Horoscope;


// import { useState, useEffect } from "react";
// import { Link } from "react-router-dom";

// const Horoscope = ({ sign }) => {
//     const zodiac_signs = [
//       "aries",
//       "taurus",
//       "gemini",
//       "cancer",
//       "leo",
//       "virgo",
//       "libra",
//       "scorpio",
//       "sagittarius",
//       "capricorn",
//       "aquarius",
//       "pisces",
//     ];
//   const [horoscope, setHoroscope] = useState({
//     daily: {},
//     monthly: {},
//     yearly: {},
//   });
//   const [activeTab, setActiveTab] = useState("daily");

//   useEffect(() => {
//     if (!sign) return;

//     fetch("/horoscopes.json")
//       .then((response) => response.json())
//       .then((data) => {
//         console.log("Fetched Horoscope Data:", data); // Debugging

//         // Function to clean text and handle undefined values
//         const cleanText = (text) => {
//           if (!text) return "Not available."; // Prevents errors
//           return text
//             .replace(/\u00a0/g, " ")
//             .replace(/\u2013/g, "-")
//             .trim();
//         };

//         // Format JSON before setting state
//         setHoroscope({
//           daily: {
//             summary: cleanText(data[sign]?.daily?.summary),
//             ratings: data[sign]?.daily?.ratings || {},
//           },
//           monthly: {
//             overview: cleanText(data[sign]?.monthly?.overview),
//             key_dates: data[sign]?.monthly?.key_dates || [],
//           },
//           yearly: {
//             highlights: cleanText(data[sign]?.yearly?.highlights),
//             forecast: cleanText(data[sign]?.yearly?.forecast),
//           },
//         });
//       })
//       .catch((error) => console.error("Error fetching horoscope:", error));
//   }, [sign]);

//   return (
//     <div>
//       <h2>{sign.charAt(0).toUpperCase() + sign.slice(1)} Horoscope</h2>

//       {/* Tabs for navigation */}
//       <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
//         <button onClick={() => setActiveTab("daily")}>🌟 Daily</button>
//         <button onClick={() => setActiveTab("monthly")}>📅 Monthly</button>
//         <button onClick={() => setActiveTab("yearly")}>📆 Yearly</button>
//       </div>

//       {/* Daily Horoscope Section */}
//       {activeTab === "daily" && (
//         <div
//           style={{
//             padding: "15px",
//             borderRadius: "8px",
//             background: "#f9f9f9",
//             border: "1px solid #ccc",
//           }}
//         >
//           <h3>🌟 Daily Horoscope</h3>
//           <p>{horoscope.daily.summary || "Horoscope not available."}</p>

//           {/* Ensure ratings exist before displaying */}
//           {horoscope.daily.ratings &&
//           Object.keys(horoscope.daily.ratings).length > 0 ? (
//             <>
//               <h4>🔹 Daily Ratings</h4>
//               <ul style={{ listStyleType: "none", paddingLeft: "0" }}>
//                 <li>
//                   <strong>Creativity:</strong>{" "}
//                   {horoscope.daily.ratings?.creativity || "Not rated"}
//                 </li>
//                 <li>
//                   <strong>Love:</strong>{" "}
//                   {horoscope.daily.ratings?.love || "Not rated"}
//                 </li>
//                 <li>
//                   <strong>Business:</strong>{" "}
//                   {horoscope.daily.ratings?.business || "Not rated"}
//                 </li>
//               </ul>
//             </>
//           ) : (
//             <p>Ratings not available.</p>
//           )}
//         </div>
//       )}

//       {/* Monthly Horoscope Section */}
//       {activeTab === "monthly" && (
//         <div
//           style={{
//             padding: "15px",
//             borderRadius: "8px",
//             background: "#f5f5f5",
//             border: "1px solid #bbb",
//             marginTop: "10px",
//           }}
//         >
//           <h3>📅 Monthly Horoscope</h3>
//           <p>{horoscope.monthly.overview}</p>

//           {/* Display Key Dates */}
//           {horoscope.monthly.key_dates.length > 0 ? (
//             <>
//               <h4>🌙 Key Dates</h4>
//               <ul style={{ listStyleType: "none", paddingLeft: "0" }}>
//                 {horoscope.monthly.key_dates.map((date, index) => (
//                   <li key={index}>{date}</li>
//                 ))}
//               </ul>
//             </>
//           ) : (
//             <p>No significant dates available.</p>
//           )}
//         </div>
//       )}

//       {/* Yearly Horoscope Section */}
//       {activeTab === "yearly" && (
//         <div
//           style={{
//             padding: "15px",
//             borderRadius: "8px",
//             background: "#eef",
//             border: "1px solid #aaa",
//             marginTop: "10px",
//           }}
//         >
//           <h3>📆 Yearly Horoscope</h3>
//           <p>
//             <strong>Highlights:</strong> {horoscope.yearly.highlights}
//           </p>
//           <p>
//             <strong>Forecast:</strong> {horoscope.yearly.forecast}
//           </p>
//         </div>
//       )}

//       {/* Zodiac Sign Navigation */}
//       <div style={{ marginTop: "20px" }}>
//         {zodiac_signs.map((zodiacSign) => (
//           <Link key={zodiacSign} to={`/${zodiacSign}`}>
//             <button>
//               {zodiacSign.charAt(0).toUpperCase() + zodiacSign.slice(1)}
//             </button>
//           </Link>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default Horoscope;
