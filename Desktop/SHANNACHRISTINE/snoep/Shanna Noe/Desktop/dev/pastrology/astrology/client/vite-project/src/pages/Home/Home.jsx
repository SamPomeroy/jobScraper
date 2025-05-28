import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>🌟 Welcome to Your Astrology App! 🌟</h1>
            <p>Select your zodiac sign to view today's horoscope.</p>

            {/* Zodiac Sign Buttons */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "10px", maxWidth: "300px", margin: "auto" }}>
                {[
                    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
                    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
                ].map((sign) => (
                    <Link key={sign} to={`/${sign}`}>
                        <button style={{ padding: "10px", fontSize: "16px", cursor: "pointer" }}>
                            {sign.charAt(0).toUpperCase() + sign.slice(1)}
                        </button>
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default Home;


// import React, { useEffect, useState } from "react";
// import axios from "axios";
// import "./Home.css";

// const Home = () => {
//     const [data, setData] = useState(null);
//     const [selectedSign, setSelectedSign] = useState("aries"); // Default Zodiac sign
// useEffect(() => {
//     fetch("/horoscopes.json")
//         .then(response => response.json())
//         .then(data => setData({ sign: selectedSign, horoscope: data[selectedSign] }));
// }, [selectedSign]);


//     return (
//         <>
//             <div className="home-container">Home Page</div>

//             {data ? (
//                 <ul className="home-ul-container">
//                     <li className="home-li-container">Sign: {data.sign}</li>
//                     <li className="home-li-container">Date: {data.date}</li>
//                     <li className="home-li-container">Horoscope: {data.horoscope}</li>
//                 </ul>
//             ) : (
//                 <p>Loading horoscope...</p>
//             )}

//             {/* Zodiac Buttons */}
//             {[
//                 "aquarius", "pisces", "aries", "taurus", "gemini", "cancer",
//                 "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"
//             ].map((sign) => (
//                 <button className="home-button-container" key={sign} onClick={() => setSelectedSign(sign)}>
//                     {sign.charAt(0).toUpperCase() + sign.slice(1)}
//                 </button>
//             ))}
//         </>
//     );
// };

// export default Home;


// import React, { useEffect, useState } from "react";
// import axios from "axios";
// import "./Home.css";

// const Home = () => {
//     const [data, setData] = useState(null);
//     const [selectedSign, setSelectedSign] = useState("aries"); // Default Zodiac sign

//     const fetchHoroscope = async (sign) => {
//         try {
//             const response = await axios.get(`https://ohmanda.com/api/horoscope/${sign.toLowerCase()}`);
//             console.log("Horoscope Data:", response.data);
//             setData(response.data);
//         } catch (error) {
//             console.error("Error fetching horoscope:", error);
//         }
//     };

//     useEffect(() => {
//         fetchHoroscope(selectedSign);
//     }, [selectedSign]);

//     return (
//         <>
//             <div className="home-container">Home Page</div>

//             {data ? (
//                 <ul className="home-ul-container">
//                     <li className="home-li-container">Sign: {data.sign}</li>
//                     <li className="home-li-container">Date: {data.date}</li>
//                     <li className="home-li-container">Horoscope: {data.horoscope}</li>
//                 </ul>
//             ) : (
//                 <p>Loading horoscope...</p>
//             )}

//             {/* Zodiac Buttons */}
//             {[
//                 "aquarius", "pisces", "aries", "taurus", "gemini", "cancer",
//                 "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"
//             ].map((sign) => (
//                 <button className="home-button-container" key={sign} onClick={() => setSelectedSign(sign)}>
//                     {sign.charAt(0).toUpperCase() + sign.slice(1)}
//                 </button>
//             ))}
//         </>
//     );
// };

// export default Home;


// import React, { useEffect, useState } from "react";
// import axios from 'axios';
// import './Home.css';

// import useAutoRefresh from "../../components/AutoRefresh/AutoRefresh";
// const Home = () => {
//     useAutoRefresh();
// axios.get("/api/horoscope/:sign", async (req, res) => {
//     console.log("horoscope", res.data)
//     try {
//         const sign = req.params.sign.toLowerCase();
//         const response = await axios.get(`https://ohmanda.com/api/horoscope/${sign}/`);
//         res.json(response.data);
//     } catch (error) {
//         res.status(500).json({ error: "Failed to fetch horoscope" });
//     }
// });

//     return (
//         <>
//       <Profile />
//         </>
//     );
// }; 

// export default Home;



// import React, { useEffect, useState } from "react";
// import axios from 'axios';
// import './Home.css'
// const Home = () => {
//     // const apiUrl = "https://aztro.sameerkumar.website";

// const [data, setData] = useState(null);
// const [selectedSign, setSelectedSign] = useState("aries"); // Default sign

// // const fetchHoroscope = async (sign) => {
// //     try {
// //         const url = `https://ohmanda.com/api/horoscope/${sign.toLowerCase()}`; // Dynamic URL based on selected sign
// //         const response = await axios.get(url);
// //         console.log("Horoscope Data:", response.data);
// //         setData(response.data);
// //     } catch (error) {
// //         console.error("Error fetching horoscope:", error);
// //     }
// // };
// const fetchHoroscope = async (sign) => {
//     try {
         
       
//          const response = await axios.get(`http://localhost:3000/api/horoscope/${sign}`);
//         console.log(response.data)
//         setData(response.data);
//     } catch (error) {
//         console.error("Error fetching horoscope:", error);
//     }
// };

// // Fetch horoscope when component mounts or when `selectedSign` changes
// useEffect(() => {
//     fetchHoroscope(selectedSign);
// }, [selectedSign]);




// return (
//         <>
//         <div className="home-container">Home Page</div>

//         {data ? (
//             <ul className="home-ul-container">
//                 <li className="home-li-container">Sign: {data.sign}</li>
//                 <li className="home-li-container">Date: {data.date}</li>
//                 <li className="home-li-container">Horoscope: {data.horoscope}</li>
//             </ul>
//         ) : (
//             <p>Loading horoscope...</p>
//         )}

//         {/* Zodiac Buttons */}
//         {[
//             "aquarius", "pisces", "aries", "taurus", "gemini", "cancer",
//             "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"
//         ].map((sign) => (
//             <button className="home-button-container" key={sign} onClick={() => setSelectedSign(sign)}>
//                 {sign.charAt(0).toUpperCase() + sign.slice(1)}
//             </button>
//         ))}
//     </>

// )
// }

// export default Home;





//          {[
    //         "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    //         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    //       ].map((sign) => (
        //         <button key={sign} onClick={() => setSelectedSign(sign)}>
        //           {sign}
        //         </button>
        //       ))}
        
        //             <div>Hme Page</div>
        //             {data && data.sun ? (
//   <ul>
//     <li>Current Date: {data.date}</li>
//     <li>Sun Sign: {data.sun.sign}</li>
//     <li>Element: {data.sun.element}</li>
//     <li>House: {data.sun.house}</li>
//     <li>Quality: {data.sun.quality}</li>
//   </ul>
// ) : (
//   <p>Loading horoscope...</p>
// )}




//             {/* {["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"].map((sign) => (
    //                 <button onClick={()=>{setSelectedSign(selectedSign)}}key={sign}>{data.sun.name}</button>
    //             ))} */}
    //         </>


// useEffect(() => {
      
    //     const fetchHoroscope = async () => {
    //         // const date = new Date();
    //         // const formattedDate = date.toISOString().split("T")[0]; // Extracts YYYY-MM-DD
    //         const today = new Date().toISOString().split("T")[0]; // Gets the current date in YYYY-MM-DD format
    //          console.log(today);
    
    //     const options = {
    //         method: 'POST',
    //         //  url: 'https://sameer-kumar-aztro-v1.p.rapidapi.com/',
    //         params: {
    //             sign: selectedSign,
    //           day: today // Uses formatted date instead of "today"
    //         },
    //         headers: {
    //           'x-rapidapi-key': '9fd4fe4735mshd39bd4ccf8afd80p172285jsnf1edd979dea8',
    //           'x-rapidapi-host': 'sameer-kumar-aztro-v1.p.rapidapi.com',
    //           'Content-Type': 'application/json'
    //         },
    //         data: {}
    //     }
    // }
    //   console.log(fetchHoroscope());
    
    // }, [selectedSign])
    // useEffect(() => {
        //     const fetchHoroscope = async () => {
    //         try {
        //             const today = new Date().toISOString().split("T")[0]; // Correct date format
        
        //             const options = {
            //                 method: "POST",
            //         // url: "https://daily-horoscope3.p.rapidapi.com/api/1.0/get_daily_horoscope.php", {

    //                 // method: "POST",
    //                 //  url: "https://sameer-kumar-aztro-v1.p.rapidapi.com/",
    //                 params: { sign: "Aries", day: today },
    //                 headers: {
    //                     'x-rapidapi-key': '9fd4fe4735mshd39bd4ccf8afd80p172285jsnf1edd979dea8',
    //                     "x-rapidapi-host": "sameer-kumar-aztro-v1.p.rapidapi.com",
    //                     "Content-Type": "application/json",
    //                 },
    //                 data: {},
    //             };
    
    //             const response = await axios.request(options);
    //             console.log("API Response:", response.data); // ✅ Logs actual API data
    //         } catch (error) {
        //             console.error("Error fetching horoscope:", error);
        //         }
    //     };
    
    //     fetchHoroscope();
    // }, []);
//     const fetchHoroscope = async () => {
    //         try {
//           const options = {
    //             method: "POST",
//    // url: "https://daily-horoscope3.p.rapidapi.com/api/1.0/get_daily_horoscope.php",
//             headers: {
    //               "x-rapidapi-key": "9fd4fe4735mshd39bd4ccf8afd80p172285jsnf1edd979dea8",
    //               "x-rapidapi-host": "daily-horoscope3.p.rapidapi.com",
    //               "Content-Type": "application/x-www-form-urlencoded"
    //             },
    //             data: new URLSearchParams({
        //               sign: "Aries",
        //               date: "2025-04-02",
        //               timezone: "5.5"
        //             })
        //           };
        
        //           const response = await axios.request(options);
        //           console.log("Horoscope Data:", response.data);
        //         } catch (error) {
//           console.error("Error fetching horoscope:", error);
//         }
//       };

//       fetchHoroscope();
// const fetchHoroscope = async (sign) => {
//     try {
//       const options = {
//         method: "GET",
//   //  url: "https://astrologer.p.rapidapi.com/api/v4/now", // ✅ Ensure URL is included
//         headers: {
//           "x-rapidapi-key": "9fd4fe4735mshd39bd4ccf8afd80p172285jsnf1edd979dea8",
//           "x-rapidapi-host": "astrologer.p.rapidapi.com",
//           Accept: "application/json"
//         }
//       };
  
//       const response = await axios.request(options);
//       console.log("Horoscope Data:", response.data);
//       setData(response.data)
//     //   setSelectedSign(response.data)
//     } catch (error) {
//       console.error("Error fetching horoscope:", error);
//     }
//   };
  
//   // Call the function to fetch horoscope data
// //   fetchHoroscope();

// useEffect(() => {
//     if (selectedSign) fetchHoroscope(selectedSign);
// }, [selectedSign]);

//         <>