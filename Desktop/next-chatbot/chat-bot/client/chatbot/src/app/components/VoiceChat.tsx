import React, { useState, useEffect, useRef } from "react";

interface SpeechRecognition extends EventTarget {
  grammars: SpeechGrammarList;
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  maxAlternatives: number;
  serviceURI: string;
  onstart: () => void;
  onresult: (event: any) => void;
  onerror: (event: any) => void;
  onend: () => void;
  onaudiostart: () => void;
  onaudioend: () => void;
  onnomatch: () => void;
  onsoundstart: () => void;
  onsoundend: () => void;
  onspeechstart: () => void;
  onspeechend: () => void;
  abort: () => void;
  start: () => void;
  stop: () => void;
}

interface IWindow extends Window {
  webkitSpeechRecognition: new () => SpeechRecognition;
  SpeechRecognition: new () => SpeechRecognition;
}

declare let window: IWindow;

const VoiceChatWindow = ({
  onClose,
  isGuestMode,
}: {
  onClose: () => void;
  isGuestMode: boolean;
}) => {
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentText, setCurrentText] = useState("");
  const [speechError, setSpeechError] = useState<string | null>(null);
  const [animationIntensity, setAnimationIntensity] = useState(0);

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const animationRef = useRef<number | null>(null);

  useEffect(() => {
    const SpeechRecognitionClass =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognitionClass) {
      const recognition = new SpeechRecognitionClass();
      recognition.lang = "en-US";
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setIsListening(true);
        setSpeechError(null);
        setCurrentText("Listening...");
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setCurrentText(`You said: "${transcript}"`);
        handleVoiceInput(transcript);
      };

      recognition.onerror = (event) => {
        console.error("Speech recognition error:", event.error);
        setSpeechError(`Voice recognition error: ${event.error}`);
        setIsListening(false);
        setCurrentText("");
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
      if (audioRef.current) {
        audioRef.current.pause();
      }
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  const handleVoiceInput = async (transcript: string) => {
    setIsProcessing(true);
    setCurrentText("Processing your request...");

    try {
      const token = localStorage.getItem("sb-access-token");
      const headers: Record<string, string> = {
        "Content-Type": "application/json",
      };

      if (token && !isGuestMode) {
        headers["Authorization"] = `Bearer ${token}`;
      }

      const response = await fetch(
        `http://localhost:8000/chat_voice?query=${encodeURIComponent(
          transcript
        )}&include_audio=true`,
        {
          method: "GET",
          headers: headers,
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      setCurrentText(data.response);

      if (data.audio) {
        playAudioResponse(data.audio, data.response);
      } else {
        speakText(data.response);
      }
    } catch (error) {
      console.error("Error getting voice response:", error);
      setSpeechError("Failed to get AI response");
      setCurrentText("Sorry, I encountered an error. Please try again.");
    } finally {
      setIsProcessing(false);
    }
  };

  const playAudioResponse = (audioUrl: string, text: string) => {
    setIsSpeaking(true);
    setCurrentText(text);

    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    audio.onplay = () => {
      startVoiceAnimation();
    };

    audio.onended = () => {
      setIsSpeaking(false);
      stopVoiceAnimation();
      setCurrentText("Click the microphone to speak again");
    };

    audio.onerror = () => {
      console.error("Audio playback failed, falling back to browser TTS");
      setIsSpeaking(false);
      stopVoiceAnimation();
      speakText(text);
    };

    audio.play().catch((error) => {
      console.error("Audio play failed:", error);
      speakText(text);
    });
  };

  const speakText = (text: string) => {
    if (window.speechSynthesis) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.volume = 1;

      utterance.onstart = () => {
        setIsSpeaking(true);
        startVoiceAnimation();
      };

      utterance.onend = () => {
        setIsSpeaking(false);
        stopVoiceAnimation();
        setCurrentText("Click the microphone to speak again");
      };

      window.speechSynthesis.speak(utterance);
    }
  };

  const startVoiceAnimation = () => {
    const animate = () => {
      setAnimationIntensity((prev) => {
        const newIntensity = 0.3 + Math.random() * 0.7;
        return newIntensity;
      });
      animationRef.current = requestAnimationFrame(animate);
    };
    animate();
  };

  const stopVoiceAnimation = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current);
      animationRef.current = null;
    }
    setAnimationIntensity(0);
  };

  const startListening = () => {
    if (
      recognitionRef.current &&
      !isListening &&
      !isSpeaking &&
      !isProcessing
    ) {
      try {
        recognitionRef.current.start();
      } catch (error) {
        console.error("Failed to start speech recognition:", error);
        setSpeechError("Failed to start voice recognition");
      }
    }
  };

  const stopAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
    stopVoiceAnimation();
    setCurrentText("Click the microphone to speak again");
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-3xl p-8 max-w-md w-full mx-4 shadow-2xl">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">🎤 Voice Chat</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        <div className="text-center mb-8">
          <div className="relative mx-auto w-32 h-32 mb-4">
            <div
              className={`absolute inset-0 rounded-full transition-all duration-150 ${
                isSpeaking
                  ? "bg-blue-500"
                  : isListening
                  ? "bg-red-500"
                  : isProcessing
                  ? "bg-yellow-500"
                  : "bg-gray-300"
              }`}
              style={{
                transform: `scale(${1 + animationIntensity * 0.3})`,
                opacity: 0.8,
              }}
            />

            <div
              className={`absolute inset-0 rounded-full border-4 transition-all duration-150 ${
                isSpeaking
                  ? "border-blue-300"
                  : isListening
                  ? "border-red-300"
                  : isProcessing
                  ? "border-yellow-300"
                  : "border-gray-200"
              }`}
              style={{
                transform: `scale(${1.2 + animationIntensity * 0.5})`,
                opacity: 0.4,
              }}
            />

            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-4xl text-white">
                {isSpeaking
                  ? "🔊"
                  : isListening
                  ? "🎤"
                  : isProcessing
                  ? "⚡"
                  : "🤖"}
              </span>
            </div>
          </div>

          <div className="h-16 flex items-center justify-center">
            <p className="text-gray-600 text-center leading-relaxed">
              {currentText || "Click the microphone to start speaking"}
            </p>
          </div>
        </div>

        {speechError && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg text-sm">
            {speechError}
          </div>
        )}

        <div className="flex justify-center space-x-4">
          <button
            onClick={startListening}
            disabled={isListening || isSpeaking || isProcessing}
            className={`px-6 py-3 rounded-full font-semibold transition-all duration-200 ${
              isListening || isSpeaking || isProcessing
                ? "bg-gray-300 cursor-not-allowed"
                : "bg-blue-500 hover:bg-blue-600 text-white transform hover:scale-105"
            }`}
          >
            {isListening
              ? "Listening..."
              : isProcessing
              ? "Processing..."
              : "🎤 Speak"}
          </button>

          {isSpeaking && (
            <button
              onClick={stopAudio}
              className="px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-full font-semibold transition-all duration-200 transform hover:scale-105"
            >
              🛑 Stop
            </button>
          )}
        </div>

        <div className="mt-4 text-center">
          <div className="flex justify-center space-x-4 text-xs text-gray-500">
            {isListening && (
              <span className="flex items-center space-x-1 text-red-600">
                <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                <span>Recording</span>
              </span>
            )}
            {isSpeaking && (
              <span className="flex items-center space-x-1 text-blue-600">
                <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
                <span>Speaking</span>
              </span>
            )}
            {isProcessing && (
              <span className="flex items-center space-x-1 text-yellow-600">
                <span className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></span>
                <span>Thinking</span>
              </span>
            )}
          </div>
        </div>

        <div className="mt-6 text-center text-xs text-gray-400">
          <p>Speak naturally and I'll respond with voice!</p>
          <p>Make sure your backend is running on localhost:8000</p>
        </div>
      </div>
    </div>
  );
};

export default VoiceChatWindow;
