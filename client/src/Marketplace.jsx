import React, { useState, useEffect } from 'react';
import { Store, Plus, Info } from 'lucide-react';

export const Marketplace = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTemplates = async () => {
      setLoading(true);
      try {
        const res = await fetch('/api/marketplace/templates');
        if (res.ok) {
          setTemplates(await res.json());
        } else {
            // Mock templates
            setTemplates([
                { id: 1, name: 'SEO Auditor', description: 'Automated SEO auditing for websites.', template_type: 'agent', version: '1.0.0' },
                { id: 2, name: 'Content Writer', description: 'Generates blog posts based on topics.', template_type: 'agent', version: '1.1.0' },
                { id: 3, name: 'Social Media Campaign', description: 'End-to-end social media workflow.', template_type: 'workflow', version: '2.0.0' },
            ]);
        }
      } catch (err) {
        setTemplates([
            { id: 1, name: 'SEO Auditor', description: 'Automated SEO auditing for websites.', template_type: 'agent', version: '1.0.0' },
            { id: 2, name: 'Content Writer', description: 'Generates blog posts based on topics.', template_type: 'agent', version: '1.1.0' },
            { id: 3, name: 'Social Media Campaign', description: 'End-to-end social media workflow.', template_type: 'workflow', version: '2.0.0' },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchTemplates();
  }, []);

  const handleInstall = (templateId) => {
    alert(`Template ${templateId} cloned to workspace.`);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <Store className="w-6 h-6 text-indigo-600" />
            <h2 className="text-xl font-bold text-gray-800">Agent Template Marketplace</h2>
          </div>
          <p className="text-gray-600">Browse and install pre-configured agents and workflows into your workspace.</p>
        </div>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center space-x-2">
          <Plus className="w-4 h-4" />
          <span>Publish Template</span>
        </button>
      </div>

      {loading ? (
        <p className="text-gray-500">Loading templates...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map(template => (
            <div key={template.id} className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-lg font-semibold text-gray-900">{template.name}</h3>
                <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded font-medium capitalize">
                  {template.template_type}
                </span>
              </div>
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{template.description}</p>
              
              <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-100">
                <span className="text-xs text-gray-400">v{template.version}</span>
                <div className="flex space-x-2">
                  <button 
                    onClick={() => handleInstall(template.id)}
                    className="flex items-center space-x-1 text-sm bg-gray-50 text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-100 font-medium border border-gray-200"
                  >
                    <span>Fork</span>
                  </button>
                  <button 
                    onClick={() => handleInstall(template.id)}
                    className="flex items-center space-x-1 text-sm bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-lg hover:bg-indigo-100 font-medium"
                  >
                    <Plus className="w-4 h-4" />
                    <span>Install</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
