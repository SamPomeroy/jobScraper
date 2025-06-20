'use client'

import React, { useEffect, useState, useRef } from 'react';
import { supabase } from '../../utils/supabase/client';
import { fetchChatResponse } from '../api/chat';
import type { User } from '@supabase/supabase-js';


declare global {
  interface Window {
    SpeechRecognition: new () => SpeechRecognition;
    webkitSpeechRecognition: new () => SpeechRecognition;
    readonly speechSynthesis: SpeechSynthesis;
    SpeechSynthesisUtterance: typeof SpeechSynthesisUtterance;
    SpeechGrammarList: new () => SpeechGrammarList;
  }
  
  interface SpeechGrammarList {
    addFromString(string: string, weight?: number): void;
    addFromURI(src: string, weight?: number): void;
    item(index: number): SpeechGrammar;
    readonly length: number;
  }
  
  interface SpeechGrammar {
    src: string;
    weight: number;
  }
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  grammars: SpeechGrammarList;
  interimResults: boolean;
  lang: string;
  maxAlternatives: number;
  onaudioend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onaudiostart: ((this: SpeechRecognition, ev: Event) => any) | null;
  onend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => any) | null;
  onnomatch: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
  onsoundend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onsoundstart: ((this: SpeechRecognition, ev: Event) => any) | null;
  onspeechend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onspeechstart: ((this: SpeechRecognition, ev: Event) => any) | null;
  onstart: ((this: SpeechRecognition, ev: Event) => any) | null;
  serviceURI: string;
  start(): void;
  stop(): void;
  abort(): void;
}

interface SpeechRecognitionEvent extends Event {
  readonly resultIndex: number;
  readonly results: SpeechRecognitionResultList;
}

interface SpeechRecognitionErrorEvent extends Event {
  readonly error: string;
  readonly message: string;
}

declare var SpeechRecognition: {
  prototype: SpeechRecognition;
  new(): SpeechRecognition;
};

type Message = {
  role: 'user' | 'assistant';
  text: string;
  timestamp: Date;
  isVoice?: boolean;
};


const GUEST_USER: Partial<User> = {
  id: 'guest',
  email: 'guest@example.com',
  user_metadata: { display_name: 'Guest User' }
};

const VOICE_CONFIG = {
  speechRecognition: {
    lang: 'en-US',
    continuous: false,
    interimResults: false,
    maxAlternatives: 1
  },
  textToSpeech: {
    rate: 0.9,
    pitch: 1,
    volume: 1,
    lang: 'en-US'
  }
};


// const GOOGLE_TTS_API_KEY = process.env.key; 

export default function ChatBot() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [user, setUser] = useState<User | null>(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [isGuestMode, setIsGuestMode] = useState(false);
  

  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voiceSupported, setVoiceSupported] = useState(false);
  const [speechError, setSpeechError] = useState<string | null>(null);
  const [useGoogleTTS, setUseGoogleTTS] = useState(false);
  

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);


  useEffect(() => {
    const checkAuth = async () => {
      try {
        const { data: { session }, error } = await supabase.auth.getSession();
        
        if (error) {
          console.error('Auth error:', error);
          setUser(null);
        } else if (session?.user) {
          setUser(session.user);
          setIsGuestMode(false);
        } else {
        
          const guestMode = localStorage.getItem('guest-mode') === 'true';
          if (guestMode) {
            setUser(GUEST_USER as User);
            setIsGuestMode(true);
          } else {
            setUser(null);
          }
        }
      } catch (err) {
        console.error('Error checking auth:', err);
        setUser(null);
      } finally {
        setAuthLoading(false);
      }
    };


      const checkVoiceSupport = () => {
        if (typeof window !== 'undefined') {
          const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition;
          const speechSynthesis = window.speechSynthesis;
          
          if (SpeechRecognitionClass && speechSynthesis) {
            setVoiceSupported(true);
            initializeSpeechRecognition();
          } else {
            console.warn('Voice features not supported in this browser');
            setVoiceSupported(false);
          }
        } else {
          setVoiceSupported(false);
        }
      };

    checkAuth();
    checkVoiceSupport();


    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (session?.user) {
          setUser(session.user);
          setIsGuestMode(false);
          localStorage.removeItem('guest-mode');
        } else {
          const guestMode = localStorage.getItem('guest-mode') === 'true';
          if (guestMode) {
            setUser(GUEST_USER as User);
            setIsGuestMode(true);
          } else {
            setUser(null);
          }
        }
        setAuthLoading(false);
      }
    );

    return () => subscription.unsubscribe();
  }, []);


  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);


  useEffect(() => {
    if (isGuestMode) {
      const savedHistory = localStorage.getItem('guest-chat-history');
      if (savedHistory) {
        try {
          const history = JSON.parse(savedHistory);
          setMessages(history.map((msg: any) => ({
            ...msg,
            timestamp: new Date(msg.timestamp)
          })));
        } catch (err) {
          console.warn('Failed to load guest chat history:', err);
        }
      }
    }
  }, [isGuestMode]);


  useEffect(() => {
    if (isGuestMode && messages.length > 0) {
      localStorage.setItem('guest-chat-history', JSON.stringify(messages));
    }
  }, [messages, isGuestMode]);


  const initializeSpeechRecognition = () => {
    const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognitionClass) return;

    const recognition = new SpeechRecognitionClass();
    recognition.lang = VOICE_CONFIG.speechRecognition.lang;
    recognition.continuous = VOICE_CONFIG.speechRecognition.continuous;
    recognition.interimResults = VOICE_CONFIG.speechRecognition.interimResults;
    recognition.maxAlternatives = VOICE_CONFIG.speechRecognition.maxAlternatives;

    recognition.onstart = () => {
      setIsListening(true);
      setSpeechError(null);
    };

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      const transcript = event.results[0][0].transcript;
      setQuery(transcript);
      

      if (transcript.trim()) {
        handleSend(transcript, true);
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      console.error('Speech recognition error:', event.error);
      setSpeechError(`Voice recognition error: ${event.error}`);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
  };


  const startListening = () => {
    if (!voiceSupported || !recognitionRef.current) {
      setSpeechError('Voice recognition not available');
      return;
    }


    if (isSpeaking) {
      stopSpeaking();
    }

    try {
      recognitionRef.current.start();
    } catch (error) {
      console.error('Failed to start speech recognition:', error);
      setSpeechError('Failed to start voice recognition');
    }
  };


  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
    }
  };

  const speakWithGoogleTTS = async (text: string) => {
    if (!GOOGLE_TTS_API_KEY || GOOGLE_TTS_API_KEY === 'YOUR_GOOGLE_API_KEY') {
      console.warn('Google TTS API key not configured, falling back to browser TTS');
      speak(text);
      return;
    }

    try {
      setIsSpeaking(true);

      const response = await fetch(
        `https://texttospeech.googleapis.com/v1/text:synthesize?key=${GOOGLE_TTS_API_KEY}`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            input: { text },
            voice: { 
              languageCode: 'en-US', 
              name: 'en-US-Wavenet-D' 
            },
            audioConfig: { 
              audioEncoding: 'MP3',
              speakingRate: 0.9,
              pitch: 0
            },
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`Google TTS API error: ${response.status}`);
      }

      const data = await response.json();
      
      if (!data.audioContent) {
        throw new Error('No audio content received from Google TTS');
      }

      const audio = new Audio('data:audio/mp3;base64,' + data.audioContent);
      
      audio.onended = () => setIsSpeaking(false);
      audio.onerror = () => {
        console.error('Audio playback failed');
        setIsSpeaking(false);
      };
      
      await audio.play();

    } catch (error) {
      console.error('Google TTS error:', error);
      setIsSpeaking(false);
      
     
      speak(text);
    }
  };


  const speak = (text: string) => {
    if (!voiceSupported || !window.speechSynthesis) {
      console.warn('Text-to-speech not supported');
      return;
    }


    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = VOICE_CONFIG.textToSpeech.rate;
    utterance.pitch = VOICE_CONFIG.textToSpeech.pitch;
    utterance.volume = VOICE_CONFIG.textToSpeech.volume;
    utterance.lang = VOICE_CONFIG.textToSpeech.lang;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event);
      setIsSpeaking(false);
    };

    window.speechSynthesis.speak(utterance);
  };


  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };


  const handleSend = async (messageText?: string, isVoiceMessage = false) => {
    const textToSend = messageText || query;
    if (!textToSend.trim() || (!user && !isGuestMode)) return;
    
    setIsLoading(true);
    setSpeechError(null);

    const userMessage: Message = {
      role: 'user',
      text: textToSend,
      timestamp: new Date(),
      isVoice: isVoiceMessage
    };

    try {

      setMessages((prev) => [...prev, userMessage]);
      
     
      const reply = await fetchChatResponse(textToSend);
      
      const assistantMessage: Message = {
        role: 'assistant',
        text: reply,
        timestamp: new Date()
      };
      
      setMessages((prev) => [...prev, assistantMessage]);

    
      if (isVoiceMessage && voiceSupported) {
        setTimeout(() => {
          if (useGoogleTTS) {
            speakWithGoogleTTS(reply);
          } else {
            speak(reply);
          }
        }, 500);
      }

      if (!messageText) setQuery(''); // Only clear if not from voice
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: 'Sorry, something went wrong. Please try again.',
          timestamp: new Date()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSignOut = async () => {
    try {
      await supabase.auth.signOut();
      localStorage.removeItem("sb-access-token");
      if (isGuestMode) {
        localStorage.removeItem('guest-mode');
        localStorage.removeItem('guest-chat-history');
        setIsGuestMode(false);
      }
      setMessages([]);
     
      window.location.href = '/signin';
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  const startGuestMode = () => {
    localStorage.setItem('guest-mode', 'true');
    localStorage.setItem('guest-session-start', new Date().toISOString());
    setUser(GUEST_USER as User);
    setIsGuestMode(true);
  };

  if (authLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (!user && !isGuestMode) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="text-6xl mb-4">🔒</div>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to use the chatbot</h1>
          <p className="text-gray-600 mb-6">You need to be signed in to start chatting.</p>
          <div className="space-y-4">
            <a
              href="/signin"
              className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-200 transform hover:scale-105"
            >
              Go to Sign In
            </a>
            <div className="text-gray-500">or</div>
            <button
              onClick={startGuestMode}
              className="inline-block bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-200 transform hover:scale-105"
            >
              Continue as Guest
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex justify-between items-center mb-4">
            <h1 className="text-4xl font-bold text-gray-900">
              {voiceSupported ? '🎤' : '🤖'} Learning Assistant
            </h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome, {isGuestMode ? 'Guest' : user?.email}
                {isGuestMode && <span className="text-xs text-orange-600 ml-2">(Guest Mode)</span>}
              </span>
              {voiceSupported && (
                <div className="flex items-center space-x-2">
                  <label className="text-xs text-gray-600">
                    <input
                      type="checkbox"
                      checked={useGoogleTTS}
                      onChange={(e) => setUseGoogleTTS(e.target.checked)}
                      className="mr-1"
                    />
                    Google TTS
                  </label>
                </div>
              )}
              <button
                onClick={handleSignOut}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm transition duration-200"
              >
                {isGuestMode ? 'Exit Guest' : 'Sign Out'}
              </button>
            </div>
          </div>
          <p className="text-gray-600">
            Ask me anything and I'll help you learn!
            {voiceSupported && ' Click the microphone to speak or type your message.'}
          </p>
        </div>

        {speechError && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {speechError}
          </div>
        )}

        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="h-96 md:h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 mt-20">
                <div className="text-6xl mb-4">💬</div>
                <p className="text-lg">Start a conversation!</p>
                <p className="text-sm">
                  {voiceSupported 
                    ? 'Ask me anything you\'d like to learn about. Use voice or text!'
                    : 'Ask me anything you\'d like to learn about.'
                  }
                </p>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${
                    msg.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl px-4 py-3 rounded-2xl ${
                      msg.role === 'user'
                        ? 'bg-blue-600 text-white rounded-br-md'
                        : 'bg-white text-gray-800 shadow-md rounded-bl-md border'
                    }`}
                  >
                    <div className="flex items-start space-x-2">
                      <div
                        className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                          msg.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-green-500 text-white'
                        }`}
                      >
                        {msg.role === 'user' ? 'U' : '🤖'}
                      </div>
                      <div className="flex-1">
                        {msg.isVoice && (
                          <div className="flex items-center mb-1">
                            <span className="text-xs opacity-75">🎤 Voice</span>
                          </div>
                        )}
                        <p className="text-sm leading-relaxed">{msg.text}</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white shadow-md rounded-2xl rounded-bl-md border px-4 py-3 max-w-xs">
                  <div className="flex items-center space-x-2">
                    <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                      <span className="text-white text-xs">🤖</span>
                    </div>
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.1s' }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: '0.2s' }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

    
          <div className="p-6 bg-white border-t">
            <div className="flex items-center space-x-3">
           
              {voiceSupported && (
                <button
                  onClick={isListening ? stopListening : startListening}
                  disabled={isLoading || isSpeaking}
                  className={`p-3 rounded-full transition-all duration-200 ${
                    isListening
                      ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse'
                      : 'bg-blue-500 hover:bg-blue-600 text-white'
                  } ${(isLoading || isSpeaking) ? 'opacity-50 cursor-not-allowed' : ''}`}
                  title={isListening ? 'Stop listening' : 'Start voice input'}
                >
                  {isListening ? '🛑' : '🎤'}
                </button>
              )}

              <div className="flex-1">
                <textarea
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder={voiceSupported ? "Type or speak your message..." : "Type your message here..."}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none outline-none"
                  rows={1}
                  disabled={isLoading || isListening}
                />
              </div>

    
              <button
                onClick={() => handleSend()}
                disabled={isLoading || !query.trim() || isListening}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-xl transition duration-200 transform hover:scale-105 disabled:hover:scale-100 min-w-[80px]"
              >
                {isLoading ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto"></div>
                ) : (
                  'Send'
                )}
              </button>

          
              {isSpeaking && (
                <button
                  onClick={stopSpeaking}
                  className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-3 rounded-xl transition-all duration-200"
                  title="Stop speaking"
                >
                  🔇
                </button>
              )}
            </div>

 
            {voiceSupported && (
              <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                <div className="flex items-center space-x-4">
                  {isListening && (
                    <span className="flex items-center space-x-1 text-red-600">
                      <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                      <span>Listening...</span>
                    </span>
                  )}
                  {isSpeaking && (
                    <span className="flex items-center space-x-1 text-blue-600">
                      <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
                      <span>Speaking...</span>
                    </span>
                  )}
                </div>
                <div>
                  {voiceSupported ? '🎤 Voice ready' : '⌨️ Text only'}
                </div>
              </div>
            )}
          </div>
        </div>

       
        {isGuestMode && (
          <div className="mt-6 text-center text-sm text-gray-500">
            <p>
              Using guest mode • <a href="/signin" className="text-blue-600 hover:underline">Sign in</a> for full features and chat history
            </p>
          </div>
        )}
      </div>
    </div>
  );
}











// 'use client'

// import React, { useEffect, useState, useRef } from 'react';
// import { supabase } from '../../utils/supabase/client';
// import { fetchChatResponse } from '../api/chat';
// import type { User } from '@supabase/supabase-js';

// // Speech Recognition type declarations
// declare global {
//   interface Window {
//     SpeechRecognition: new () => SpeechRecognition;
//     webkitSpeechRecognition: new () => SpeechRecognition;
//     readonly speechSynthesis: SpeechSynthesis;
//     SpeechSynthesisUtterance: typeof SpeechSynthesisUtterance;
//     SpeechGrammarList: new () => SpeechGrammarList;
//   }
  
//   interface SpeechGrammarList {
//     addFromString(string: string, weight?: number): void;
//     addFromURI(src: string, weight?: number): void;
//     item(index: number): SpeechGrammar;
//     readonly length: number;
//   }
  
//   interface SpeechGrammar {
//     src: string;
//     weight: number;
//   }
// }

// interface SpeechRecognition extends EventTarget {
//   continuous: boolean;
//   grammars: SpeechGrammarList;
//   interimResults: boolean;
//   lang: string;
//   maxAlternatives: number;
//   onaudioend: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onaudiostart: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onend: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => any) | null;
//   onnomatch: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
//   onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
//   onsoundend: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onsoundstart: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onspeechend: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onspeechstart: ((this: SpeechRecognition, ev: Event) => any) | null;
//   onstart: ((this: SpeechRecognition, ev: Event) => any) | null;
//   serviceURI: string;
//   start(): void;
//   stop(): void;
//   abort(): void;
// }

// interface SpeechRecognitionEvent extends Event {
//   readonly resultIndex: number;
//   readonly results: SpeechRecognitionResultList;
// }

// interface SpeechRecognitionErrorEvent extends Event {
//   readonly error: string;
//   readonly message: string;
// }

// declare var SpeechRecognition: {
//   prototype: SpeechRecognition;
//   new(): SpeechRecognition;
// };

// type Message = {
//   role: 'user' | 'assistant';
//   text: string;
//   timestamp: Date;
//   isVoice?: boolean;
// };

// // Guest user configuration
// const GUEST_USER: Partial<User> = {
//   id: 'guest',
//   email: 'guest@example.com',
//   user_metadata: { display_name: 'Guest User' }
// };

// // Voice configuration
// const VOICE_CONFIG = {
//   speechRecognition: {
//     lang: 'en-US',
//     continuous: false,
//     interimResults: false,
//     maxAlternatives: 1
//   },
//   textToSpeech: {
//     rate: 0.9,
//     pitch: 1,
//     volume: 1,
//     lang: 'en-US'
//   }
// };

// // Google TTS Configuration - Replace with your API key
// const GOOGLE_TTS_API_KEY = process.env.key; 

// export default function ChatBot() {
//   const [query, setQuery] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [user, setUser] = useState<User | null>(null);
//   const [authLoading, setAuthLoading] = useState(true);
//   const [isGuestMode, setIsGuestMode] = useState(false);
  
//   // Voice-related state
//   const [isListening, setIsListening] = useState(false);
//   const [isSpeaking, setIsSpeaking] = useState(false);
//   const [voiceSupported, setVoiceSupported] = useState(false);
//   const [speechError, setSpeechError] = useState<string | null>(null);
//   const [useGoogleTTS, setUseGoogleTTS] = useState(false);
  
//   // Refs for voice functionality
//   const recognitionRef = useRef<SpeechRecognition | null>(null);
//   const messagesEndRef = useRef<HTMLDivElement>(null);

//   // Check authentication and voice support
//   useEffect(() => {
//     const checkAuth = async () => {
//       try {
//         const { data: { session }, error } = await supabase.auth.getSession();
        
//         if (error) {
//           console.error('Auth error:', error);
//           setUser(null);
//         } else if (session?.user) {
//           setUser(session.user);
//           setIsGuestMode(false);
//         } else {
//           // Check if user wants guest mode
//           const guestMode = localStorage.getItem('guest-mode') === 'true';
//           if (guestMode) {
//             setUser(GUEST_USER as User);
//             setIsGuestMode(true);
//           } else {
//             setUser(null);
//           }
//         }
//       } catch (err) {
//         console.error('Error checking auth:', err);
//         setUser(null);
//       } finally {
//         setAuthLoading(false);
//       }
//     };

//     // Check voice support
//       const checkVoiceSupport = () => {
//         if (typeof window !== 'undefined') {
//           const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition;
//           const speechSynthesis = window.speechSynthesis;
          
//           if (SpeechRecognitionClass && speechSynthesis) {
//             setVoiceSupported(true);
//             initializeSpeechRecognition();
//           } else {
//             console.warn('Voice features not supported in this browser');
//             setVoiceSupported(false);
//           }
//         } else {
//           setVoiceSupported(false);
//         }
//       };

//     checkAuth();
//     checkVoiceSupport();

//     // Listen for auth changes
//     const { data: { subscription } } = supabase.auth.onAuthStateChange(
//       async (event, session) => {
//         if (session?.user) {
//           setUser(session.user);
//           setIsGuestMode(false);
//           localStorage.removeItem('guest-mode');
//         } else {
//           const guestMode = localStorage.getItem('guest-mode') === 'true';
//           if (guestMode) {
//             setUser(GUEST_USER as User);
//             setIsGuestMode(true);
//           } else {
//             setUser(null);
//           }
//         }
//         setAuthLoading(false);
//       }
//     );

//     return () => subscription.unsubscribe();
//   }, []);

//   // Auto-scroll to bottom when new messages arrive
//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
//   }, [messages]);

//   // Load guest chat history on mount
//   useEffect(() => {
//     if (isGuestMode) {
//       const savedHistory = localStorage.getItem('guest-chat-history');
//       if (savedHistory) {
//         try {
//           const history = JSON.parse(savedHistory);
//           setMessages(history.map((msg: any) => ({
//             ...msg,
//             timestamp: new Date(msg.timestamp)
//           })));
//         } catch (err) {
//           console.warn('Failed to load guest chat history:', err);
//         }
//       }
//     }
//   }, [isGuestMode]);

//   // Save guest chat history when messages change
//   useEffect(() => {
//     if (isGuestMode && messages.length > 0) {
//       localStorage.setItem('guest-chat-history', JSON.stringify(messages));
//     }
//   }, [messages, isGuestMode]);

//   // Initialize speech recognition
//   const initializeSpeechRecognition = () => {
//     const SpeechRecognitionClass = window.SpeechRecognition || window.webkitSpeechRecognition;
    
//     if (!SpeechRecognitionClass) return;

//     const recognition = new SpeechRecognitionClass();
//     recognition.lang = VOICE_CONFIG.speechRecognition.lang;
//     recognition.continuous = VOICE_CONFIG.speechRecognition.continuous;
//     recognition.interimResults = VOICE_CONFIG.speechRecognition.interimResults;
//     recognition.maxAlternatives = VOICE_CONFIG.speechRecognition.maxAlternatives;

//     recognition.onstart = () => {
//       setIsListening(true);
//       setSpeechError(null);
//     };

//     recognition.onresult = (event: SpeechRecognitionEvent) => {
//       const transcript = event.results[0][0].transcript;
//       setQuery(transcript);
      
//       // Auto-send voice messages
//       if (transcript.trim()) {
//         handleSend(transcript, true);
//       }
//     };

//     recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
//       console.error('Speech recognition error:', event.error);
//       setSpeechError(`Voice recognition error: ${event.error}`);
//       setIsListening(false);
//     };

//     recognition.onend = () => {
//       setIsListening(false);
//     };

//     recognitionRef.current = recognition;
//   };

//   // Start listening for voice input
//   const startListening = () => {
//     if (!voiceSupported || !recognitionRef.current) {
//       setSpeechError('Voice recognition not available');
//       return;
//     }

//     // Stop any ongoing speech synthesis
//     if (isSpeaking) {
//       stopSpeaking();
//     }

//     try {
//       recognitionRef.current.start();
//     } catch (error) {
//       console.error('Failed to start speech recognition:', error);
//       setSpeechError('Failed to start voice recognition');
//     }
//   };

//   // Stop listening
//   const stopListening = () => {
//     if (recognitionRef.current && isListening) {
//       recognitionRef.current.stop();
//     }
//   };

//   // Google Text-to-Speech function
//   const speakWithGoogleTTS = async (text: string) => {
//     if (!GOOGLE_TTS_API_KEY || GOOGLE_TTS_API_KEY === 'YOUR_GOOGLE_API_KEY') {
//       console.warn('Google TTS API key not configured, falling back to browser TTS');
//       speak(text);
//       return;
//     }

//     try {
//       setIsSpeaking(true);

//       const response = await fetch(
//         `https://texttospeech.googleapis.com/v1/text:synthesize?key=${GOOGLE_TTS_API_KEY}`,
//         {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({
//             input: { text },
//             voice: { 
//               languageCode: 'en-US', 
//               name: 'en-US-Wavenet-D' 
//             },
//             audioConfig: { 
//               audioEncoding: 'MP3',
//               speakingRate: 0.9,
//               pitch: 0
//             },
//           }),
//         }
//       );

//       if (!response.ok) {
//         throw new Error(`Google TTS API error: ${response.status}`);
//       }

//       const data = await response.json();
      
//       if (!data.audioContent) {
//         throw new Error('No audio content received from Google TTS');
//       }

//       const audio = new Audio('data:audio/mp3;base64,' + data.audioContent);
      
//       audio.onended = () => setIsSpeaking(false);
//       audio.onerror = () => {
//         console.error('Audio playback failed');
//         setIsSpeaking(false);
//       };
      
//       await audio.play();

//     } catch (error) {
//       console.error('Google TTS error:', error);
//       setIsSpeaking(false);
      
//       // Fallback to browser TTS
//       speak(text);
//     }
//   };

//   // Browser Text-to-speech function
//   const speak = (text: string) => {
//     if (!voiceSupported || !window.speechSynthesis) {
//       console.warn('Text-to-speech not supported');
//       return;
//     }

//     // Stop any ongoing speech
//     window.speechSynthesis.cancel();

//     const utterance = new SpeechSynthesisUtterance(text);
//     utterance.rate = VOICE_CONFIG.textToSpeech.rate;
//     utterance.pitch = VOICE_CONFIG.textToSpeech.pitch;
//     utterance.volume = VOICE_CONFIG.textToSpeech.volume;
//     utterance.lang = VOICE_CONFIG.textToSpeech.lang;

//     utterance.onstart = () => setIsSpeaking(true);
//     utterance.onend = () => setIsSpeaking(false);
//     utterance.onerror = (event) => {
//       console.error('Speech synthesis error:', event);
//       setIsSpeaking(false);
//     };

//     window.speechSynthesis.speak(utterance);
//   };

//   // Stop speaking
//   const stopSpeaking = () => {
//     if (window.speechSynthesis) {
//       window.speechSynthesis.cancel();
//       setIsSpeaking(false);
//     }
//   };

//   // Handle sending messages
//   const handleSend = async (messageText?: string, isVoiceMessage = false) => {
//     const textToSend = messageText || query;
//     if (!textToSend.trim() || (!user && !isGuestMode)) return;
    
//     setIsLoading(true);
//     setSpeechError(null);

//     const userMessage: Message = {
//       role: 'user',
//       text: textToSend,
//       timestamp: new Date(),
//       isVoice: isVoiceMessage
//     };

//     try {
//       // Add user message immediately
//       setMessages((prev) => [...prev, userMessage]);
      
//       // Get AI response
//       const reply = await fetchChatResponse(textToSend);
      
//       const assistantMessage: Message = {
//         role: 'assistant',
//         text: reply,
//         timestamp: new Date()
//       };
      
//       setMessages((prev) => [...prev, assistantMessage]);

//       // Auto-speak assistant responses for voice conversations
//       if (isVoiceMessage && voiceSupported) {
//         setTimeout(() => {
//           if (useGoogleTTS) {
//             speakWithGoogleTTS(reply);
//           } else {
//             speak(reply);
//           }
//         }, 500);
//       }

//       if (!messageText) setQuery(''); // Only clear if not from voice
//     } catch (error) {
//       console.error('Error sending message:', error);
//       setMessages((prev) => [
//         ...prev,
//         {
//           role: 'assistant',
//           text: 'Sorry, something went wrong. Please try again.',
//           timestamp: new Date()
//         }
//       ]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   const handleKeyPress = (e: React.KeyboardEvent) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       handleSend();
//     }
//   };

//   const handleSignOut = async () => {
//     try {
//       await supabase.auth.signOut();
//       localStorage.removeItem("sb-access-token");
//       if (isGuestMode) {
//         localStorage.removeItem('guest-mode');
//         localStorage.removeItem('guest-chat-history');
//         setIsGuestMode(false);
//       }
//       setMessages([]);
//       // Redirect to sign in page
//       window.location.href = '/signin';
//     } catch (error) {
//       console.error('Error signing out:', error);
//     }
//   };

//   const startGuestMode = () => {
//     localStorage.setItem('guest-mode', 'true');
//     localStorage.setItem('guest-session-start', new Date().toISOString());
//     setUser(GUEST_USER as User);
//     setIsGuestMode(true);
//   };

//   // Show loading spinner while checking auth
//   if (authLoading) {
//     return (
//       <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
//         <div className="text-center">
//           <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
//           <p className="text-gray-600">Loading...</p>
//         </div>
//       </div>
//     );
//   }

//   // Show login prompt if not authenticated and not in guest mode
//   if (!user && !isGuestMode) {
//     return (
//       <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
//         <div className="text-center">
//           <div className="text-6xl mb-4">🔒</div>
//           <h1 className="text-2xl font-bold text-gray-900 mb-4">Please login to use the chatbot</h1>
//           <p className="text-gray-600 mb-6">You need to be signed in to start chatting.</p>
//           <div className="space-y-4">
//             <a
//               href="/signin"
//               className="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-200 transform hover:scale-105"
//             >
//               Go to Sign In
//             </a>
//             <div className="text-gray-500">or</div>
//             <button
//               onClick={startGuestMode}
//               className="inline-block bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 px-6 rounded-xl transition duration-200 transform hover:scale-105"
//             >
//               Continue as Guest
//             </button>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   // Main chat interface
//   return (
//     <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
//       <div className="max-w-4xl mx-auto">
//         <div className="text-center mb-8">
//           <div className="flex justify-between items-center mb-4">
//             <h1 className="text-4xl font-bold text-gray-900">
//               {voiceSupported ? '🎤' : '🤖'} Learning Assistant
//             </h1>
//             <div className="flex items-center space-x-4">
//               <span className="text-sm text-gray-600">
//                 Welcome, {isGuestMode ? 'Guest' : user?.email}
//                 {isGuestMode && <span className="text-xs text-orange-600 ml-2">(Guest Mode)</span>}
//               </span>
//               {voiceSupported && (
//                 <div className="flex items-center space-x-2">
//                   <label className="text-xs text-gray-600">
//                     <input
//                       type="checkbox"
//                       checked={useGoogleTTS}
//                       onChange={(e) => setUseGoogleTTS(e.target.checked)}
//                       className="mr-1"
//                     />
//                     Google TTS
//                   </label>
//                 </div>
//               )}
//               <button
//                 onClick={handleSignOut}
//                 className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm transition duration-200"
//               >
//                 {isGuestMode ? 'Exit Guest' : 'Sign Out'}
//               </button>
//             </div>
//           </div>
//           <p className="text-gray-600">
//             Ask me anything and I'll help you learn!
//             {voiceSupported && ' Click the microphone to speak or type your message.'}
//           </p>
//         </div>

//         {/* Error Display */}
//         {speechError && (
//           <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
//             {speechError}
//           </div>
//         )}

//         <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
//           <div className="h-96 md:h-[500px] overflow-y-auto p-6 space-y-4 bg-gray-50">
//             {messages.length === 0 ? (
//               <div className="text-center text-gray-500 mt-20">
//                 <div className="text-6xl mb-4">💬</div>
//                 <p className="text-lg">Start a conversation!</p>
//                 <p className="text-sm">
//                   {voiceSupported 
//                     ? 'Ask me anything you\'d like to learn about. Use voice or text!'
//                     : 'Ask me anything you\'d like to learn about.'
//                   }
//                 </p>
//               </div>
//             ) : (
//               messages.map((msg, i) => (
//                 <div
//                   key={i}
//                   className={`flex ${
//                     msg.role === 'user' ? 'justify-end' : 'justify-start'
//                   }`}
//                 >
//                   <div
//                     className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl px-4 py-3 rounded-2xl ${
//                       msg.role === 'user'
//                         ? 'bg-blue-600 text-white rounded-br-md'
//                         : 'bg-white text-gray-800 shadow-md rounded-bl-md border'
//                     }`}
//                   >
//                     <div className="flex items-start space-x-2">
//                       <div
//                         className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
//                           msg.role === 'user'
//                             ? 'bg-blue-500 text-white'
//                             : 'bg-green-500 text-white'
//                         }`}
//                       >
//                         {msg.role === 'user' ? 'U' : '🤖'}
//                       </div>
//                       <div className="flex-1">
//                         {msg.isVoice && (
//                           <div className="flex items-center mb-1">
//                             <span className="text-xs opacity-75">🎤 Voice</span>
//                           </div>
//                         )}
//                         <p className="text-sm leading-relaxed">{msg.text}</p>
//                       </div>
//                     </div>
//                   </div>
//                 </div>
//               ))
//             )}

//             {isLoading && (
//               <div className="flex justify-start">
//                 <div className="bg-white shadow-md rounded-2xl rounded-bl-md border px-4 py-3 max-w-xs">
//                   <div className="flex items-center space-x-2">
//                     <div className="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
//                       <span className="text-white text-xs">🤖</span>
//                     </div>
//                     <div className="flex space-x-1">
//                       <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
//                       <div
//                         className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
//                         style={{ animationDelay: '0.1s' }}
//                       ></div>
//                       <div
//                         className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
//                         style={{ animationDelay: '0.2s' }}
//                       ></div>
//                     </div>
//                   </div>
//                 </div>
//               </div>
//             )}
//             <div ref={messagesEndRef} />
//           </div>

//           {/* Input */}
//           <div className="p-6 bg-white border-t">
//             <div className="flex items-center space-x-3">
//               {/* Voice Button */}
//               {voiceSupported && (
//                 <button
//                   onClick={isListening ? stopListening : startListening}
//                   disabled={isLoading || isSpeaking}
//                   className={`p-3 rounded-full transition-all duration-200 ${
//                     isListening
//                       ? 'bg-red-500 hover:bg-red-600 text-white animate-pulse'
//                       : 'bg-blue-500 hover:bg-blue-600 text-white'
//                   } ${(isLoading || isSpeaking) ? 'opacity-50 cursor-not-allowed' : ''}`}
//                   title={isListening ? 'Stop listening' : 'Start voice input'}
//                 >
//                   {isListening ? '🛑' : '🎤'}
//                 </button>
//               )}

//               {/* Text Input */}
//               <div className="flex-1">
//                 <textarea
//                   value={query}
//                   onChange={(e) => setQuery(e.target.value)}
//                   onKeyPress={handleKeyPress}
//                   placeholder={voiceSupported ? "Type or speak your message..." : "Type your message here..."}
//                   className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none outline-none"
//                   rows={1}
//                   disabled={isLoading || isListening}
//                 />
//               </div>

//               {/* Send Button */}
//               <button
//                 onClick={() => handleSend()}
//                 disabled={isLoading || !query.trim() || isListening}
//                 className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold rounded-xl transition duration-200 transform hover:scale-105 disabled:hover:scale-100 min-w-[80px]"
//               >
//                 {isLoading ? (
//                   <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mx-auto"></div>
//                 ) : (
//                   'Send'
//                 )}
//               </button>

//               {/* Stop Speaking Button */}
//               {isSpeaking && (
//                 <button
//                   onClick={stopSpeaking}
//                   className="bg-orange-500 hover:bg-orange-600 text-white px-4 py-3 rounded-xl transition-all duration-200"
//                   title="Stop speaking"
//                 >
//                   🔇
//                 </button>
//               )}
//             </div>

//             {/* Status Indicators */}
//             {voiceSupported && (
//               <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
//                 <div className="flex items-center space-x-4">
//                   {isListening && (
//                     <span className="flex items-center space-x-1 text-red-600">
//                       <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
//                       <span>Listening...</span>
//                     </span>
//                   )}
//                   {isSpeaking && (
//                     <span className="flex items-center space-x-1 text-blue-600">
//                       <span className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></span>
//                       <span>Speaking...</span>
//                     </span>
//                   )}
//                 </div>
//                 <div>
//                   {voiceSupported ? '🎤 Voice ready' : '⌨️ Text only'}
//                 </div>
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Footer */}
//         {isGuestMode && (
//           <div className="mt-6 text-center text-sm text-gray-500">
//             <p>
//               Using guest mode • <a href="/signin" className="text-blue-600 hover:underline">Sign in</a> for full features and chat history
//             </p>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }



