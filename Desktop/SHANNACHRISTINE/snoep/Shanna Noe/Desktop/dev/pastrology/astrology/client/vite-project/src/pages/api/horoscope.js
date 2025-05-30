export default async function handler(req, res) {
  const response = await fetch("https://horoscope-d6jk8kvu9-snoecodes-projects.vercel.app/horoscopes.json");
  const data = await response.json();

  res.setHeader("Cache-Control", "no-store, max-age=0"); // Prevents caching
  res.status(200).json(data);
}

