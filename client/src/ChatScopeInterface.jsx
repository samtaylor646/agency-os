import React, { useState, useRef, useEffect } from 'react';

const ChatScopeInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mobileTab, setMobileTab] = useState('chat'); // 'chat' or 'preview'
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
    if (mobileTab === 'chat') {
      scrollToBottom();
    }
  }, [messages, mobileTab]);

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
      
      const assistantMessage = { role: 'assistant', content: data.chat_response || data.response || "No response" };
      setMessages((prev) => [...prev, assistantMessage]);
      
      if (data.extraction) {
        setProjectDetails(data.extraction);
      } else if (data.extracted_details) {
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
    <div className="flex flex-col md:flex-row h-full w-full bg-gray-50 text-gray-800 font-sans">
      
      {/* Mobile Tab Toggle */}
      <div className="md:hidden flex shrink-0 border-b border-gray-200 bg-white text-sm font-medium">
        <button 
          onClick={() => setMobileTab('chat')}
          className={`flex-1 py-3 text-center transition-colors ${mobileTab === 'chat' ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          Scoping Chat
        </button>
        <button 
          onClick={() => setMobileTab('preview')}
          className={`flex-1 py-3 text-center transition-colors border-l border-gray-200 ${mobileTab === 'preview' ? 'bg-blue-50 text-blue-600 border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'}`}
        >
          Project Details
        </button>
      </div>

      {/* Left Side: Chat Interface */}
      <div className={`${mobileTab === 'chat' ? 'flex' : 'hidden'} md:flex w-full md:w-1/2 flex-col border-r border-gray-200 bg-white overflow-hidden`}>
        <div className="hidden md:flex items-center px-4 py-3 border-b border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900 font-medium text-sm shrink-0">
          Scoping Chat
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-4 text-sm">
          {messages.length === 0 && (
            <div className="text-gray-500 text-center mt-10">
              Welcome! Describe your project requirements to get started.
            </div>
          )}
          {messages.map((msg, index) => (
            <div 
              key={index} 
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div 
                className={`max-w-[85%] p-3 rounded-md shadow-sm ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-tr-none' 
                    : msg.role === 'system'
                    ? 'bg-red-50 text-red-700 border border-red-200'
                    : 'bg-gray-50 text-gray-800 border border-gray-200 rounded-tl-none'
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-50 text-gray-500 border border-gray-200 rounded-md rounded-tl-none p-3 shadow-sm">
                <span className="animate-pulse">Typing...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 bg-white flex shrink-0">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type your message..."
            className="flex-1 p-2 bg-white border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent text-gray-800 text-sm mr-3 transition-shadow shadow-sm"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="bg-blue-600 text-white px-5 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:text-gray-500 transition-colors text-sm font-medium shadow-sm"
            disabled={isLoading}
          >
            Send
          </button>
        </form>
      </div>

      {/* Right Side: Extracted Details & Documents Preview */}
      <div className={`${mobileTab === 'preview' ? 'flex' : 'hidden'} md:flex w-full md:w-1/2 flex-col bg-gray-50 overflow-hidden`}>
        <div className="hidden md:flex items-center px-4 py-3 border-b border-blue-100 bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900 font-medium text-sm shrink-0 gap-4">
          <button className="font-bold border-b-2 border-blue-600 pb-1">Project Details</button>
          <button className="text-gray-500 hover:text-gray-700 pb-1">Draft PRD</button>
          <button className="text-gray-500 hover:text-gray-700 pb-1">Tech Spec</button>
          <button className="text-gray-500 hover:text-gray-700 pb-1">Task List</button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 md:p-6">
          <div className="bg-white rounded-md border border-gray-200 p-5 shadow-sm space-y-6">
            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Project Name</h3>
              <div className="text-base text-gray-900 font-medium">
                {projectDetails.name || <span className="text-gray-400 italic font-normal">Not specified</span>}
              </div>
            </div>

            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-1">Description</h3>
              <div className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
                {projectDetails.description || <span className="text-gray-400 italic">Not specified</span>}
              </div>
            </div>

            <div>
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Tech Stack</h3>
              {projectDetails.tech_stack && projectDetails.tech_stack.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                  {projectDetails.tech_stack.map((tech, index) => (
                    <span 
                      key={index} 
                      className="px-2.5 py-1 bg-gray-50 text-gray-700 border border-gray-200 rounded-md text-xs font-medium shadow-sm"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              ) : (
                <span className="text-gray-400 italic text-sm">None specified</span>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatScopeInterface;
