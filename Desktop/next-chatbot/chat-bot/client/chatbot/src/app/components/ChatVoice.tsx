import { useState } from "react";

export default function ChatVoice() {
  const [query, setQuery] = useState("");
  const [audioUrl, setAudioUrl] = useState("");

  const playAudio = async () => {
    const res = await fetch(`http://127.0.0.1:8000/chat-voice?query=${encodeURIComponent(query)}`);
    const data = await res.json();
    if (data.audio) {
      setAudioUrl(data.audio);
    }
  };

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask me something..." />
      <button onClick={playAudio}>🔊 Generate & Play Audio</button>

      {audioUrl && <audio controls src={audioUrl}></audio>}
    </div>
  );
}
