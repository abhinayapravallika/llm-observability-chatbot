import "./App.css";
import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [sessions, setSessions] = useState([]);

  const chatEndRef = useRef(null);

  // Auto Scroll
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [chat]);

  // Load conversation history when app starts
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/conversations"
      );

      setSessions(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  const loadConversation = async (id) => {
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/conversation/${id}`
      );

      const messages = response.data;

      const formatted = [];

      for (let i = 0; i < messages.length; i += 2) {
        formatted.push({
          user: messages[i]?.content || "",
          bot: messages[i + 1]?.content || "",
        });
      }

      setChat(formatted);
      setSessionId(id);
    } catch (error) {
      console.log(error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;

    setMessage("");
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: userMessage,
          session_id: sessionId,
        }
      );

      if (!sessionId && response.data.session_id) {
        setSessionId(response.data.session_id);
      }

      setChat((prev) => [
        ...prev,
        {
          user: userMessage,
          bot: response.data.response || response.data.error,
        },
      ]);

      // Refresh sidebar history
      loadSessions();
    } catch (error) {
      console.error(error);

      setChat((prev) => [
        ...prev,
        {
          user: userMessage,
          bot: "Backend connection failed.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearConversation = () => {
    setChat([]);
    setSessionId(null);
  };

  return (
    <div className="app-layout">
      {/* Sidebar */}

      <div className="sidebar">
        <button
          className="new-btn"
          onClick={clearConversation}
        >
          + New Chat
        </button>

        <div className="history-list">
          <h3>Conversation History</h3>

          {sessions.length === 0 ? (
            <p>No conversations</p>
          ) : (
            sessions.map((session, index) => (
              <div
                key={index}
                className="history-item"
                onClick={() => loadConversation(session.session_id)}
              >
                {session.title}
              </div>
            ))
          )}
        </div>
      </div>

      {/* Chat Area */}

      <div className="container">
        <h1 className="title">Chatbot</h1>

        <div className="chat-box">
          {chat.map((item, index) => (
            <div key={index} className="message">
              <div className="user-msg">
                {item.user}
              </div>

              <div className="bot-msg">
                <ReactMarkdown>
                  {item.bot}
                </ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && (
            <p className="loading">
              Bot is typing...
            </p>
          )}

          <div ref={chatEndRef}></div>
        </div>

        <div className="input-area">
          <input
            type="text"
            value={message}
            placeholder="Ask something..."
            onChange={(e) =>
              setMessage(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            className="input-box"
          />

          <button
            onClick={sendMessage}
            className="send-btn"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;