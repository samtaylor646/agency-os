import React, { useState, useEffect, useRef } from 'react';
import AgentMessageBubble from './AgentMessageBubble';
import MemoryInspectorSidebar from './MemoryInspectorSidebar';
import { useWorkspace } from './WorkspaceContext';

export default function PodChatContainer({ sessionId }) {
  const { apiFetch, currentWorkspace } = useWorkspace();
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [input, setInput] = useState('');
  const [isInspectorOpen, setIsInspectorOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Fetch initial messages for the pod session
    const fetchMessages = async () => {
      if (!sessionId) return;
      setIsLoading(true);
      try {
        const response = await apiFetch(`/api/v1/agent_sessions/${sessionId}/messages`);
        if (response.ok) {
          const data = await response.json();
          setMessages(data.messages || []);
        } else {
          console.error('Failed to fetch pod messages');
          setMessages([]);
        }
      } catch (error) {
        console.error('Error fetching messages:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchMessages();

    // Set up real-time streaming using WebSockets instead of SSE
    if (!sessionId || !currentWorkspace) return;
    const wsUrl = import.meta.env.VITE_WS_URL || (import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('http', 'ws') : 'ws://localhost:5000');
    const ws = new WebSocket(`${wsUrl}/ws/${currentWorkspace.id}`);

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'agent_message' || data.type === 'message') {
           setMessages((prev) => [...prev, data.message || data]);
        }
      } catch (e) {
        console.error("Failed to parse streamed message", e);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket failed:", error);
    };

    return () => {
      ws.close();
    };
  }, [sessionId, currentWorkspace]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      message: input,
      agentName: "User",
      agentRole: "User",
      timestamp: new Date().toISOString(),
      isUser: true,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');

    try {
      await apiFetch(`/api/v1/agent_sessions/${sessionId}/intervene`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
    } catch (error) {
      console.error('Failed to send user message:', error);
    }
  };

  return (
    <div className="flex flex-col h-full w-full max-w-4xl mx-auto bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gray-50 border-b border-gray-200 px-6 py-4 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold text-gray-800">Pod Execution Thread</h2>
          <p className="text-xs text-gray-500">Session ID: {sessionId || 'Demo Session'}</p>
        </div>
        <div className="flex space-x-2 items-center">
          {/* PodThreadTimeline (Mock visual indicator) */}
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-2">
            <span className="w-2 h-2 mr-1.5 bg-blue-600 rounded-full animate-pulse"></span>
            Active: Developer
          </span>
          <button 
            onClick={() => setIsInspectorOpen(!isInspectorOpen)}
            className={`p-1.5 rounded-md transition-colors ${isInspectorOpen ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
            title="Toggle Memory Inspector"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Main Chat Area */}
        <div className="flex flex-col flex-1 overflow-hidden relative">
          <div className="flex-1 overflow-y-auto p-6 bg-gray-50/50">
            {isLoading ? (
              <div className="flex justify-center items-center h-full">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <div className="space-y-2">
                {messages.map((msg) => (
                  <AgentMessageBubble key={msg.id} {...msg} />
                ))}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>

          {/* Input Bar */}
          <div className="bg-white border-t border-gray-200 p-4">
            <form onSubmit={handleSend} className="flex space-x-4">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Intervene or prompt the pod..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
              />
              <button
                type="submit"
                disabled={!input.trim()}
                className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm"
              >
                Send
              </button>
            </form>
          </div>
        </div>

        {/* Memory Inspector Sidebar */}
        <MemoryInspectorSidebar 
          sessionId={sessionId} 
          isOpen={isInspectorOpen} 
          onClose={() => setIsInspectorOpen(false)} 
        />
      </div>
    </div>
  );
}
