import React, { useState, useEffect } from 'react';
import ContextCard from './ContextCard';

export default function MemoryInspectorSidebar({ sessionId, isOpen, onClose }) {
  const [contextData, setContextData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('All');

  useEffect(() => {
    if (!isOpen) return;
    
    // Mock fetch for semantic memory/RAG context
    const fetchContext = async () => {
      setIsLoading(true);
      try {
        // Mocking API call for context since endpoints might not be ready yet
        // const response = await fetch(`/api/v1/agent_sessions/${sessionId}/context?agent=${selectedAgent}`);
        await new Promise(resolve => setTimeout(resolve, 500));
        
        setContextData([
          { id: 1, text: "The user prefers a dark mode interface for the analytics dashboard.", score: 0.95, metadata: { source: "User Preferences", timestamp: new Date().toISOString() }, agent: "Architect" },
          { id: 2, text: "Previous deployment failed due to missing Redis environment variables.", score: 0.88, metadata: { source: "Deployment Logs", timestamp: new Date(Date.now() - 86400000).toISOString() }, agent: "Developer" },
          { id: 3, text: "Marketplace components must use Tailwind CSS Grid layout.", score: 0.76, metadata: { source: "Tech Spec", timestamp: new Date(Date.now() - 172800000).toISOString() }, agent: "Architect" }
        ].filter(item => selectedAgent === 'All' || item.agent === selectedAgent));
      } catch (error) {
        console.error('Error fetching context:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchContext();
  }, [sessionId, isOpen, selectedAgent]);

  if (!isOpen) return null;

  return (
    <div className="w-80 border-l border-gray-200 bg-gray-50 flex flex-col h-full transition-all duration-300">
      <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-white">
        <h3 className="text-sm font-semibold text-gray-800">Memory Inspector</h3>
        <button onClick={onClose} className="text-gray-500 hover:text-gray-700">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div className="p-4 border-b border-gray-200 bg-white">
        <label className="block text-xs font-medium text-gray-700 mb-1">Filter by Agent</label>
        <select 
          className="w-full text-sm border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
          value={selectedAgent}
          onChange={(e) => setSelectedAgent(e.target.value)}
        >
          <option value="All">All Agents</option>
          <option value="Architect">Architect</option>
          <option value="Developer">Developer</option>
        </select>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {isLoading ? (
          <div className="flex justify-center py-8">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
          </div>
        ) : contextData.length > 0 ? (
          contextData.map((item) => (
            <ContextCard key={item.id} text={item.text} metadata={item.metadata} score={item.score} />
          ))
        ) : (
          <div className="text-center text-sm text-gray-500 py-8">
            No context retrieved for this selection.
          </div>
        )}
      </div>
    </div>
  );
}