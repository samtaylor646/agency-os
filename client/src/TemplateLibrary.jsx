import React, { useState, useEffect } from 'react';
import { useWorkspace } from './WorkspaceContext';
import { Play, Copy, Trash2, Edit3, Grid, List } from 'lucide-react';

export const TemplateLibrary = () => {
  const { currentWorkspace, apiFetch } = useWorkspace();
  const [templates, setTemplates] = useState([]);
  const [viewMode, setViewMode] = useState('grid');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTemplates();
  }, [currentWorkspace]);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const res = await apiFetch('/api/v1/templates');
      if (res.ok) {
        const data = await res.json();
        setTemplates(data.templates || []);
      }
    } catch (e) {
      console.error("Failed to fetch templates", e);
    } finally {
      setLoading(false);
    }
  };

  const instantiateTemplate = async (templateId) => {
    try {
      const res = await apiFetch(`/api/v1/templates/${templateId}/instantiate`, { method: 'POST' });
      if (res.ok) {
        alert("Template instantiated successfully");
      } else {
        alert("Failed to instantiate template");
      }
    } catch (e) {
      console.error(e);
      alert("Error instantiating template");
    }
  };

  const deleteTemplate = async (templateId) => {
    if (!confirm('Are you sure you want to delete this template?')) return;
    try {
      const res = await apiFetch(`/api/v1/templates/${templateId}`, { method: 'DELETE' });
      if (res.ok) {
        fetchTemplates();
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) {
    return <div className="p-8 text-center text-gray-500">Loading templates...</div>;
  }

  return (
    <div className="flex flex-col h-full space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Template Library</h1>
          <p className="text-gray-500 mt-1">Browse and instantiate saved workflows and DAG configurations.</p>
        </div>
        <div className="flex items-center space-x-2 bg-white p-1 rounded-lg border border-gray-200">
          <button 
            onClick={() => setViewMode('grid')}
            className={`p-2 rounded-md ${viewMode === 'grid' ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <Grid className="w-5 h-5" />
          </button>
          <button 
            onClick={() => setViewMode('list')}
            className={`p-2 rounded-md ${viewMode === 'list' ? 'bg-blue-50 text-blue-600' : 'text-gray-400 hover:text-gray-600'}`}
          >
            <List className="w-5 h-5" />
          </button>
        </div>
      </div>

      {templates.length === 0 ? (
        <div className="bg-white rounded-xl border border-dashed border-gray-300 p-12 text-center">
          <Copy className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-1">No templates found</h3>
          <p className="text-gray-500">Save workflows as templates to see them here.</p>
        </div>
      ) : (
        <div className={viewMode === 'grid' ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" : "space-y-4"}>
          {templates.map(template => (
            <div key={template.id} className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow flex flex-col">
              <div className="flex justify-between items-start mb-4">
                <h3 className="font-semibold text-lg text-gray-900">{template.name}</h3>
                <span className="text-xs font-medium bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                  v{template.version || '1.0'}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-6 flex-1 line-clamp-3">
                {template.description || "No description provided."}
              </p>
              <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
                <div className="flex space-x-2">
                  <button 
                    onClick={() => deleteTemplate(template.id)}
                    className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    title="Delete"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
                <button
                  onClick={() => instantiateTemplate(template.id)}
                  className="flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Instantiate
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TemplateLibrary;