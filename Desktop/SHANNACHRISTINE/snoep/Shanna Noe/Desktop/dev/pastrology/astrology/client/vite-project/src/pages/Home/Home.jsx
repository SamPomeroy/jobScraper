import { Link } from "react-router-dom";

const Home = () => {
    return (
        <div style={{ textAlign: "center", padding: "20px" }}>
            <h1>🌟 Welcome to Your Astrology App! 🌟</h1>
            <p>Select your zodiac sign to view today's horoscope.</p>

          
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

