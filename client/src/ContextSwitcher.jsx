import React from 'react';
import { useWorkspace } from './WorkspaceContext';
import { ChevronDown, Building2 } from 'lucide-react';

export const ContextSwitcher = () => {
  const { workspaces, activeWorkspaceId, setActiveWorkspaceId, userRole } = useWorkspace();

  if (workspaces.length === 0) return null;

  return (
    <div className="relative group inline-block">
      <button className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-md transition-colors border border-gray-200">
        <Building2 className="w-4 h-4 text-gray-500" />
        <span className="font-medium text-gray-700">
          {workspaces.find(w => w.id === activeWorkspaceId)?.name || 'Select Workspace'}
        </span>
        <ChevronDown className="w-4 h-4 text-gray-500" />
      </button>

      <div className="absolute left-0 mt-2 w-56 bg-white border border-gray-200 rounded-md shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
        <div className="p-2 border-b border-gray-100">
          <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Switch Workspace</p>
        </div>
        <ul className="py-1">
          {workspaces.map((workspace) => (
            <li key={workspace.id}>
              <button
                className={`w-full text-left px-4 py-2 text-sm hover:bg-blue-50 hover:text-blue-600 transition-colors ${
                  activeWorkspaceId === workspace.id ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-700'
                }`}
                onClick={() => setActiveWorkspaceId(workspace.id)}
              >
                {workspace.name}
              </button>
            </li>
          ))}
        </ul>
        {userRole === 'Agency Admin' && (
          <div className="border-t border-gray-100 p-1">
            <button 
              className="w-full text-left px-4 py-2 text-sm text-gray-600 hover:bg-gray-50 transition-colors rounded-sm"
              onClick={() => document.dispatchEvent(new CustomEvent('open-create-workspace'))}
            >
              + Create New Workspace
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
