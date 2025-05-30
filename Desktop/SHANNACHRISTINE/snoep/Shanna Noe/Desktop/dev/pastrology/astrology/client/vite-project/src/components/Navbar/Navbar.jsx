import { Link } from "react-router-dom";
import React from "react";
import "./Navbar.css";
import Logo from "../../assets/Dev.svg";

const zodiac_signs = [
  "aries", "taurus", "gemini", "cancer", "leo", "virgo",
  "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
];

const Navbar = () => {
  return (
    <div className="container-navbar">
      <div className="logo-container">
        <img src={Logo} alt="My Logo" className="logo" title="Portfolio coming soon" />
      </div>
      <nav className="navbar">
        {zodiac_signs.map((zodiacSign) => (
          <Link key={zodiacSign} to={`/${zodiacSign}`}>
            <button className="nav-button">
              {zodiacSign.charAt(0).toUpperCase() + zodiacSign.slice(1)}
            </button>
          </Link>
        ))}
      </nav>
    </div>
  );
};

export default Navbar;
