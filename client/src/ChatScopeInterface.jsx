import React, { useState, useRef, useEffect } from 'react';
import { useWorkspace } from './WorkspaceContext';
// { useState, useRef, useEffect } from 'react';

const ChatScopeInterface = () => {
  const [messages, setMessages] = useState([]);
  const { apiFetch, activeWorkspaceId } = useWorkspace();
  const [chatId, setChatId] = useState(null);
  const [projectId, setProjectId] = useState(null);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [mobileTab, setMobileTab] = useState('chat'); // 'chat' or 'preview'
  const [projectDetails, setProjectDetails] = useState({
    name: '',
    description: '',
    tech_stack: []
  });
  
  
  useEffect(() => {
    const initialize = async () => {
      try {
        let currentProjectId = null;
        let currentChatId = null;

        const projRes = await apiFetch('/api/v1/projects');
        if (projRes.ok) {
          const projs = await projRes.json();
          if (projs.length > 0) {
            currentProjectId = projs[0].id;
            setProjectId(currentProjectId);
            setProjectDetails({
              name: projs[0].name,
              description: projs[0].description,
              tech_stack: projs[0].tech_stack || []
            });
          } else {
            const newProjRes = await apiFetch('/api/v1/projects', {
              method: 'POST',
              body: JSON.stringify({ name: 'New Project', description: '', tech_stack: [] })
            });
            if (newProjRes.ok) {
              const newProj = await newProjRes.json();
              currentProjectId = newProj.id;
              setProjectId(currentProjectId);
            }
          }
        }

        const chatRes = await apiFetch('/api/v1/chat');
        if (chatRes.ok) {
          const chats = await chatRes.json();
          if (chats.length > 0) {
            currentChatId = chats[0].id;
            setChatId(currentChatId);
            const chatDetailsRes = await apiFetch(`/api/v1/chat/${currentChatId}`);
            if (chatDetailsRes.ok) {
              const chatDetails = await chatDetailsRes.json();
              if (chatDetails.messages && chatDetails.messages.length > 0) {
                setMessages(chatDetails.messages);
              }
            }
          } else {
            const newChatRes = await apiFetch('/api/v1/chat', {
              method: 'POST',
              body: JSON.stringify({ project_id: currentProjectId, name: 'Scoping Chat' })
            });
            if (newChatRes.ok) {
              const newChat = await newChatRes.json();
              currentChatId = newChat.id;
              setChatId(currentChatId);
            }
          }
        }
      } catch (error) {
        console.error('Failed to initialize chat scope:', error);
      }
    };
    if (activeWorkspaceId) {
      initialize();
    }
  }, [apiFetch, activeWorkspaceId]);

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
      if (chatId) {
        await apiFetch(`/api/v1/chat/${chatId}/messages`, {
          method: 'POST',
          body: JSON.stringify(userMessage)
        });
      }

      const response = await apiFetch('/api/v1/chat/scope', {
        method: 'POST',
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const assistantMessage = { role: 'assistant', content: data.chat_response || data.response || "No response" };
      
      if (chatId) {
        await apiFetch(`/api/v1/chat/${chatId}/messages`, {
          method: 'POST',
          body: JSON.stringify(assistantMessage)
        });
      }

      setMessages((prev) => [...prev, assistantMessage]);
      
      const extraction = data.extraction || data.extracted_details;
      if (extraction) {
        setProjectDetails(extraction);
        if (projectId) {
          await apiFetch(`/api/v1/projects/${projectId}`, {
            method: 'PUT',
            body: JSON.stringify({
              name: extraction.name || 'New Project',
              description: extraction.description || '',
              tech_stack: extraction.tech_stack || []
            })
          });
        }
      }

    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [...prev, { role: 'system', content: 'Error: Could not reach the server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const [rightPanelTab, setRightPanelTab] = useState('details'); // details, prd, spec, tasks
  const [generatedDocs, setGeneratedDocs] = useState({
    prd: '',
    spec: '',
    tasks: ''
  });

  const fileInputRef = useRef(null);
  
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file || !chatId) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await apiFetch(`/api/v1/chat/${chatId}/documents/upload`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) throw new Error('Upload failed');
      const data = await response.json();
      
      const extraction = data.extraction || data.extracted_details || data;
      
      const systemMessage = { role: 'system', content: `Successfully ingested '${file.name}'. Context has been updated.` };
      setMessages(prev => [...prev, systemMessage]);
      
      if (extraction) {
        setProjectDetails(prev => ({
          name: extraction.name || prev.name,
          description: extraction.description ? `${prev.description}\n\n[Ingested Data]:\n${extraction.description}` : prev.description,
          tech_stack: [...new Set([...(prev.tech_stack || []), ...(extraction.tech_stack || [])])]
        }));
      }
    } catch (error) {
      console.error('File upload error:', error);
      setMessages(prev => [...prev, { role: 'system', content: `Error: Failed to upload ${file.name}` }]);
    } finally {
      setIsLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleGenerateDocument = async (docType) => {
    setIsLoading(true);
    try {
      const response = await apiFetch(`/api/v1/chat/${chatId || 1}/generate/${docType}`, {
        method: 'POST',
        
        body: JSON.stringify({ doc_type: docType, context: projectDetails })
      });
      if (!response.ok) throw new Error('Generation failed');
      const data = await response.json();
      setGeneratedDocs(prev => ({ ...prev, [docType]: data.content || `Generated ${docType} content placeholder...` }));
      setRightPanelTab(docType);
    } catch (error) {
      console.error(error);
      setGeneratedDocs(prev => ({ ...prev, [docType]: `# Error generating ${docType}\n\nPlease try again.` }));
      setRightPanelTab(docType);
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

        <form onSubmit={handleSendMessage} className="p-4 border-t border-gray-200 bg-white flex shrink-0 items-center">
          <input
            type="file"
            accept=".txt,.md,.pdf"
            hidden
            ref={fileInputRef}
            onChange={handleFileUpload}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-2 mr-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors disabled:text-gray-300"
            disabled={isLoading || !chatId}
            title="Upload Document"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="m18.375 12.739-7.693 7.693a4.5 4.5 0 0 1-6.364-6.364l10.94-10.94A3 3 0 1 1 19.5 7.372L8.552 18.32m.009-.01-.01.01m5.699-9.941-7.81 7.81a1.5 1.5 0 0 0 2.112 2.13" />
            </svg>
          </button>
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            aria-label="Project scope description input"
            placeholder="What would you like to build?"
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
          <button onClick={() => setRightPanelTab('details')} className={`pb-1 ${rightPanelTab === 'details' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}>Project Details</button>
          <button onClick={() => setRightPanelTab('prd')} className={`pb-1 ${rightPanelTab === 'prd' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}>Draft PRD</button>
          <button onClick={() => setRightPanelTab('spec')} className={`pb-1 ${rightPanelTab === 'spec' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}>Tech Spec</button>
          <button onClick={() => setRightPanelTab('tasks')} className={`pb-1 ${rightPanelTab === 'tasks' ? 'font-bold border-b-2 border-blue-600' : 'text-gray-500 hover:text-gray-700'}`}>Task List</button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 md:p-6">
          {rightPanelTab === 'details' ? (
          <div className="bg-white rounded-md border border-gray-200 p-5 shadow-sm space-y-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold text-gray-800">Project Extraction</h2>
              <div className="flex gap-2">
                <button onClick={() => handleGenerateDocument('prd')} className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded border border-indigo-200 hover:bg-indigo-100">Gen PRD</button>
                <button onClick={() => handleGenerateDocument('spec')} className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded border border-indigo-200 hover:bg-indigo-100">Gen Spec</button>
                <button onClick={() => handleGenerateDocument('tasks')} className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-medium rounded border border-indigo-200 hover:bg-indigo-100">Gen Tasks</button>
              </div>
            </div>
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
          ) : (
            <div className="bg-white rounded-md border border-gray-200 p-5 shadow-sm space-y-4 h-full">
               <h2 className="text-lg font-bold text-gray-800 capitalize">{rightPanelTab}</h2>
               <div className="text-sm text-gray-700 whitespace-pre-wrap font-mono bg-gray-50 p-4 rounded border">
                 {generatedDocs[rightPanelTab] || `Click 'Gen ${rightPanelTab}' from the Project Details tab to generate this document.`}
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatScopeInterface;
