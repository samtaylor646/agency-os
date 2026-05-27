import React, { useState } from 'react';
import { X } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export default function CreateWorkspaceModal({ isOpen, onClose }) {
  const [workspaceName, setWorkspaceName] = useState('');
  const { workspaces, setWorkspaces, setActiveWorkspaceId, apiFetch } = useWorkspace();

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!workspaceName.trim()) return;

    try {
      const res = await apiFetch('/api/v1/workspaces', {
        method: 'POST',
        body: JSON.stringify({ name: workspaceName.trim(), settings_json: {} })
      });

      if (res.ok) {
        const data = await res.json();
        const newWorkspace = { ...data, id: String(data.id) };
        setWorkspaces([...workspaces, newWorkspace]);
        setActiveWorkspaceId(newWorkspace.id);
        setWorkspaceName('');
        onClose();
      } else {
        console.error('Failed to create workspace');
      }
    } catch (err) {
      console.error('Error creating workspace:', err);
    }
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900 bg-opacity-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-900">Create New Workspace</h2>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <form onSubmit={handleSubmit} className="p-6">
          <div className="mb-6">
            <label htmlFor="workspaceName" className="block text-sm font-medium text-gray-700 mb-2">
              Workspace Name
            </label>
            <input
              type="text"
              id="workspaceName"
              value={workspaceName}
              onChange={(e) => setWorkspaceName(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all"
              placeholder="e.g. Acme Corp"
              autoFocus
              required
            />
          </div>
          
          <div className="flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 transition-colors"
              disabled={!workspaceName.trim()}
            >
              Create Workspace
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
