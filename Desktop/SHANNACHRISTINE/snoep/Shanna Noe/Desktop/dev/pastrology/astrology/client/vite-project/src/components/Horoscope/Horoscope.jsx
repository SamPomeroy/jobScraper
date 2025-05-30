import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./Horoscope.css"; // Make sure this file contains the responsive styles

const zodiac_signs = [
  "aries",
  "taurus",
  "gemini",
  "cancer",
  "leo",
  "virgo",
  "libra",
  "scorpio",
  "sagittarius",
  "capricorn",
  "aquarius",
  "pisces",
];

const Horoscope = ({ sign }) => {
  const [horoscope, setHoroscope] = useState({
    daily: {},
    monthly: {},
    yearly: {},
  });
  const [activeTab, setActiveTab] = useState("daily");
useEffect(() => {
  if (!sign) return;

  fetch("/api/horoscope")// Cache-busting query param
    .then((response) => response.json())
    .then((data) => {
      console.log("Fetched Horoscope Data:", data);

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


  // useEffect(() => {
  //   if (!sign) return;

  //   fetch(`/horoscopes.json?timestamp=${new Date().getTime()}`)
  //     .then((response) => response.json())
  //     .then((data) => {
  //       console.log("Fetched Horoscope Data:", data);

  //       const cleanText = (text) => (text ? text.trim() : "Not available");

  //       setHoroscope({
  //         daily: {
  //           summary: cleanText(data[sign]?.daily?.summary),
  //           ratings: data[sign]?.daily?.ratings || {},
  //         },
  //         monthly: {
  //           overview: cleanText(data[sign]?.monthly?.overview),
  //           key_dates: data[sign]?.monthly?.key_dates || [],
  //         },
  //         yearly: {
  //           highlights: cleanText(data[sign]?.yearly?.highlights),
  //           forecast: cleanText(data[sign]?.yearly?.forecast),
  //         },
  //       });
  //     })
  //     .catch((error) => console.error("Error fetching horoscope:", error));
  // }, [sign]);

  return (
    <div className="horoscope-container">
     
      <h2 className="horoscope-title">
        {sign ? sign.charAt(0).toUpperCase() + sign.slice(1) : "Unknown"}{" "}
        Horoscope
      </h2>

      <div className="tab-buttons">
        <button onClick={() => setActiveTab("daily")}>🌟 Daily</button>
        <button onClick={() => setActiveTab("monthly")}>📅 Monthly</button>
        <button onClick={() => setActiveTab("yearly")}>📆 Yearly</button>
      </div>

      <div className="horoscope-content">
        {activeTab === "daily" && (
          <div className="daily-section">
            <h3>🌟 Daily Horoscope</h3>
            <p>{horoscope.daily.summary}</p>
          </div>
        )}

        {activeTab === "monthly" && (
          <div className="monthly-section">
            <h3>📅 Monthly Horoscope</h3>
            <p>{horoscope.monthly.overview}</p>
            {horoscope.monthly.key_dates.length > 0 && (
              <ul>
                {horoscope.monthly.key_dates.map((date, index) => (
                  <li key={index}>{date}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        {activeTab === "yearly" && (
          <div className="yearly-section">
            <h3>📆 Yearly Horoscope</h3>
            <p>
              <strong>Highlights:</strong> {horoscope.yearly.highlights}
            </p>
            <p>
              <strong>Forecast:</strong> {horoscope.yearly.forecast}
            </p>
          </div>
        )}
      </div>

  
      
    </div>
  );
};

export default Horoscope;
