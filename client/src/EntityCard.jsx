import React from 'react';
import { Plus } from 'lucide-react';

export const EntityCard = ({ entity, onClick }) => {
  const handleInstall = (e) => {
    e.stopPropagation();
    alert(`Installing ${entity.name}...`);
  };

  return (
    <div 
      className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow cursor-pointer flex flex-col h-full"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-semibold text-gray-900 line-clamp-1">{entity.name}</h3>
        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded font-medium capitalize shrink-0 ml-2">
          {entity.template_type || entity.type || 'Agent'}
        </span>
      </div>
      <p className="text-gray-600 text-sm mb-4 line-clamp-2 flex-grow">{entity.description}</p>
      
      <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
        <div className="flex flex-col">
          <span className="text-xs text-gray-400">v{entity.version || '1.0.0'}</span>
          <span className="text-xs text-gray-500">{entity.author || 'AgencyOS Core'}</span>
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={handleInstall}
            className="flex items-center space-x-1 text-sm bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-100 font-medium"
          >
            <Plus className="w-4 h-4" />
            <span>Install</span>
          </button>
        </div>
      </div>
    </div>
  );
};
