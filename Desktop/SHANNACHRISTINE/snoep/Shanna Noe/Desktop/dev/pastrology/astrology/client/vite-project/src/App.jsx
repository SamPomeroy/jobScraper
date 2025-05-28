import {
  BrowserRouter as Router,
  Route,
  Routes,
  BrowserRouter,
} from "react-router-dom";
import Home from "./pages/Home/Home";
import Horoscope from "./components/Horoscope/Horoscope"; // Import the Horoscope component

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        {[
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
        ].map((sign) => (
          <Route
            key={sign}
            path={`/${sign}`}
            element={<Horoscope sign={sign} />}
          />
        ))}
      </Routes>
    </BrowserRouter>
  );
}

export default App;

{
  /* <Home/> */
}
