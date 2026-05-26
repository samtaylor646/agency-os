import React, { useState, useEffect } from 'react';
import { Store, Plus, Search, Filter } from 'lucide-react';
import { MarketplaceGrid } from './MarketplaceGrid';
import { EntityDetailModal } from './EntityDetailModal';

export const Marketplace = () => {
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [activeCategory, setActiveCategory] = useState('all');

  useEffect(() => {
    const fetchTemplates = async () => {
      setLoading(true);
      try {
        const res = await fetch('/api/v1/marketplace/templates');
        if (res.ok) {
          setTemplates(await res.json());
        } else {
            // Mock templates
            setTemplates([
                { id: 1, name: 'SEO Auditor', description: 'Automated SEO auditing for websites. Generates comprehensive reports on on-page and off-page factors.', full_description: 'The SEO Auditor agent automatically crawls specified domains, analyzing meta tags, keyword density, broken links, and site speed. It compiles these findings into a detailed markdown report, highlighting critical issues and actionable recommendations for improving search engine rankings.', template_type: 'agent', version: '1.0.0', author: 'Marketing Pod', category: 'marketing' },
                { id: 2, name: 'Content Writer', description: 'Generates blog posts based on topics.', full_description: 'A versatile agent that takes a topic, tone, and target audience to produce high-quality, engaging blog posts. It can also perform basic web research to include up-to-date statistics and references.', template_type: 'agent', version: '1.1.0', author: 'Creative Team', category: 'content' },
                { id: 3, name: 'Social Media Campaign', description: 'End-to-end social media workflow.', full_description: 'This pod template orchestrates multiple agents to handle a full social media campaign. It includes a Strategist to plan content, a Writer for drafting posts, a Designer for generating image prompts, and an Analyst for reviewing engagement metrics.', template_type: 'workflow', version: '2.0.0', author: 'AgencyOS Core', category: 'marketing' },
                { id: 4, name: 'Code Reviewer', description: 'Automated code review and linting.', full_description: 'An agent that analyzes pull requests for code quality, security vulnerabilities, and adherence to style guides. It leaves inline comments and a summary review.', template_type: 'agent', version: '1.0.5', author: 'DevOps Team', category: 'development' },
                { id: 5, name: 'Data Analyst', description: 'Processes CSVs and generates insights.', full_description: 'Upload your raw data files, and this agent will clean, process, and analyze the data to extract key trends. It can generate charts and write a summary report explaining the findings in plain English.', template_type: 'agent', version: '1.2.0', author: 'Data Science Pod', category: 'strategy' },
            ]);
        }
      } catch (err) {
        setTemplates([
            { id: 1, name: 'SEO Auditor', description: 'Automated SEO auditing for websites.', template_type: 'agent', version: '1.0.0', category: 'marketing' },
            { id: 2, name: 'Content Writer', description: 'Generates blog posts based on topics.', template_type: 'agent', version: '1.1.0', category: 'content' },
            { id: 3, name: 'Social Media Campaign', description: 'End-to-end social media workflow.', template_type: 'workflow', version: '2.0.0', category: 'marketing' },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchTemplates();
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
