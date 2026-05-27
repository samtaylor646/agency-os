import React from 'react';

const getAgentColor = (role) => {
  const colors = {
    'Architect': 'bg-blue-100 text-blue-800 border-blue-300',
    'Developer': 'bg-green-100 text-green-800 border-green-300',
    'QA': 'bg-yellow-100 text-yellow-800 border-yellow-300',
    'Manager': 'bg-purple-100 text-purple-800 border-purple-300',
    'User': 'bg-gray-100 text-gray-800 border-gray-300',
    'System': 'bg-red-100 text-red-800 border-red-300',
  };
  return colors[role] || 'bg-indigo-100 text-indigo-800 border-indigo-300';
};

const getAvatarInitial = (name) => {
  return name ? name.charAt(0).toUpperCase() : '?';
};

export default function AgentMessageBubble({ message, agentName, agentRole, timestamp, isUser }) {
  const isSystem = agentRole === 'System';
  
  if (isSystem) {
    return (
      <div className="flex justify-center my-4">
        <div className="bg-gray-50 border border-gray-200 text-gray-500 text-xs px-3 py-1 rounded-full shadow-sm">
          {message}
        </div>
      </div>
    );
  }

  const alignClass = isUser ? 'justify-end' : 'justify-start';
  const bubbleColor = getAgentColor(agentRole);

  return (
    <div className={`flex w-full mb-4 ${alignClass}`}>
      {!isUser && (
        <div className="flex-shrink-0 mr-3">
          <div className={`h-8 w-8 rounded-full flex items-center justify-center font-bold text-sm shadow-sm ${bubbleColor}`}>
            {getAvatarInitial(agentName)}
          </div>
        </div>
      )}
      
      <div className={`max-w-[75%] flex flex-col ${isUser ? 'items-end' : 'items-start'}`}>
        {!isUser && (
          <div className="flex items-baseline space-x-2 mb-1">
            <span className="font-semibold text-sm text-gray-700">{agentName}</span>
            <span className="text-xs text-gray-500">{agentRole}</span>
          </div>
        )}
        
        <div className={`px-4 py-2 rounded-xl shadow-sm border ${bubbleColor} ${isUser ? 'bg-blue-600 text-white border-blue-700 rounded-br-sm' : 'rounded-bl-sm'}`}>
          <div className="text-sm whitespace-pre-wrap">{message}</div>
        </div>
        
        <div className="text-xs text-gray-400 mt-1">
          {new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
}
