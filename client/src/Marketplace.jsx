import React, { useState, useEffect } from 'react';
import { Store, Plus, Search, Filter } from 'lucide-react';
import { MarketplaceGrid } from './MarketplaceGrid';
import { EntityDetailModal } from './EntityDetailModal';
import { useWorkspace } from './WorkspaceContext';

export const Marketplace = () => {
  const { apiFetch } = useWorkspace();
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    const fetchTemplates = async () => {
      setLoading(true);
      try {
        const res = await apiFetch('/api/v1/marketplace/templates');
        if (res.ok) {
          const data = await res.json();
          // Normalize data structure if missing fields
          const normalized = data.map(t => ({
             ...t,
             category: t.category || 'marketing', // Default or fallback
             author: t.author || 'Community',
             full_description: t.full_description || t.description
          }));
          setTemplates(normalized);
        } else {
          setTemplates([]);
        }
      } catch (err) {
        setTemplates([]);
      } finally {
        setLoading(false);
      }
    };
    fetchTemplates();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const categories = [
    { id: 'all', name: 'All Categories' },
    { id: 'marketing', name: 'Marketing' },
    { id: 'content', name: 'Content Creation' },
    { id: 'development', name: 'Development' },
    { id: 'strategy', name: 'Strategy & Data' }
  ];

  const filteredTemplates = activeCategory === 'all' 
    ? templates 
    : templates.filter(t => t.category === activeCategory);

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-6 gap-4 shrink-0 px-6 pt-6">
        <div>
          <div className="flex items-center space-x-3 mb-2">
            <Store className="w-6 h-6 text-indigo-600" />
            <h2 className="text-xl font-bold text-gray-800">Agent Template Marketplace</h2>
          </div>
          <p className="text-gray-600">Browse and install pre-configured agents and workflows into your workspace.</p>
        </div>
        <div className="flex items-center space-x-3">
          <div className="relative">
             <Search className="w-4 h-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
             <input 
               type="text" 
               placeholder="Search templates..." 
               className="pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 w-64"
             />
          </div>
          <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center justify-center space-x-2 shrink-0">
            <Plus className="w-4 h-4" />
            <span>Publish Template</span>
          </button>
        </div>
      </div>

      <div className="flex flex-grow overflow-hidden px-6 pb-6 gap-6">
        {/* Sidebar */}
        <div className="w-64 shrink-0 flex flex-col space-y-6 overflow-y-auto pr-2">
          <div>
             <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center">
               <Filter className="w-3.5 h-3.5 mr-1.5" />
               Categories
             </h3>
             <ul className="space-y-1">
               {categories.map(cat => (
                 <li key={cat.id}>
                   <button
                     onClick={() => setActiveCategory(cat.id)}
                     className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                       activeCategory === cat.id 
                         ? 'bg-indigo-50 text-indigo-700' 
                         : 'text-gray-600 hover:bg-gray-100'
                     }`}
                   >
                     {cat.name}
                   </button>
                 </li>
               ))}
             </ul>
          </div>
        </div>

        {/* Main Grid */}
        <div className="flex-grow overflow-y-auto">
          {loading ? (
            <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
            </div>
          ) : (
            <MarketplaceGrid 
              items={filteredTemplates} 
              onEntityClick={(entity) => setSelectedEntity(entity)} 
            />
          )}
        </div>
      </div>

      {selectedEntity && (
        <EntityDetailModal 
          entity={selectedEntity} 
          onClose={() => setSelectedEntity(null)} 
        />
      )}
    </div>
  );
};
