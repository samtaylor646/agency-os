import React, { useState, useRef, useEffect } from 'react';

const ChatScopeInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [projectDetails, setProjectDetails] = useState({
    name: '',
    description: '',
    tech_stack: []
  });
  
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user', content: inputValue };
    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/chat/scope', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const assistantMessage = { role: 'assistant', content: data.response };
      setMessages((prev) => [...prev, assistantMessage]);
      
      if (data.extracted_details) {
        setProjectDetails(data.extracted_details);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [...prev, { role: 'system', content: 'Error: Could not reach the server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-full w-full bg-gray-100 text-gray-800 font-sans">
      {/* Left Side: Chat Interface */}
      <div className="w-1/2 flex flex-col border-r border-gray-300 bg-white">
        <div className="p-4 border-b border-gray-200 bg-blue-600 text-white font-bold text-lg">
          Project Scoping Chat
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="text-gray-500 italic text-center mt-10">
              Start by describing the project you want to build...
            </div>
          )}
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`max-w-[80%] rounded-lg p-3 ${
                  msg.role === 'user' 
                    ? 'bg-blue-500 text-white rounded-br-none' 
                    : msg.role === 'system'
                    ? 'bg-red-100 text-red-800 border border-red-300'
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 text-gray-800 rounded-lg p-3 rounded-bl-none">
                <span className="animate-pulse">Typing...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 bg-gray-50 flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Describe your project..."
            className="flex-1 p-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="bg-blue-600 text-white px-4 py-2 rounded-r-md hover:bg-blue-700 disabled:bg-blue-300 transition-colors"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </div>

      {/* Right Side: Extracted Details Preview */}
      <div className="w-1/2 p-6 overflow-y-auto bg-gray-50 flex flex-col">
        <h2 className="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">Project Preview</h2>
        
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-6">
          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Project Name</h3>
            <div className="text-xl font-medium text-gray-900">
              {projectDetails.name || <span className="text-gray-400 italic">Not yet defined</span>}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-1">Description</h3>
            <div className="text-gray-700 whitespace-pre-wrap">
              {projectDetails.description || <span className="text-gray-400 italic">Not yet defined</span>}
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Tech Stack</h3>
            {projectDetails.tech_stack && projectDetails.tech_stack.length > 0 ? (
              <div className="flex flex-wrap gap-2">
                {projectDetails.tech_stack.map((tech, index) => (
                  <span 
                    key={index} 
                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full border border-blue-200"
                  >
                    {tech}
                  </span>
                ))}
              </div>
            ) : (
              <span className="text-gray-400 italic">Not yet defined</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatScopeInterface;
