import React from 'react';
import { X, Plus, CheckCircle2, ShieldAlert } from 'lucide-react';

export const EntityDetailModal = ({ entity, onClose }) => {
  if (!entity) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm">
      <div className="bg-white rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-start bg-gray-50/50">
          <div>
            <div className="flex items-center space-x-3 mb-1">
              <h2 className="text-2xl font-bold text-gray-900">{entity.name}</h2>
              <span className="px-2.5 py-1 bg-indigo-100 text-indigo-700 text-xs rounded-md font-semibold capitalize">
                {entity.template_type || entity.type || 'Agent'}
              </span>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>By {entity.author || 'AgencyOS Core'}</span>
              <span>•</span>
              <span>Version {entity.version || '1.0.0'}</span>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto flex-grow">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-8">
              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Overview</h3>
                <p className="text-gray-600 leading-relaxed">
                  {entity.full_description || entity.description || 'No detailed description provided.'}
                </p>
              </section>

              <section>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Capabilities</h3>
                <ul className="space-y-2">
                  {(entity.capabilities || ['Text Generation', 'Data Analysis']).map((cap, i) => (
                    <li key={i} className="flex items-start space-x-2 text-gray-700">
                      <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
                      <span>{cap}</span>
                    </li>
                  ))}
                </ul>
              </section>
            </div>

            <div className="space-y-6">
              <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
                <h4 className="font-semibold text-gray-900 mb-4 flex items-center space-x-2">
                  <ShieldAlert className="w-4 h-4 text-amber-500" />
                  <span>Required Permissions</span>
                </h4>
                <ul className="space-y-3 text-sm">
                  <li className="flex items-start space-x-2 text-gray-600">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                    <span>Workspace Read Access</span>
                  </li>
                  <li className="flex items-start space-x-2 text-gray-600">
                    <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
                    <span>External API Execution</span>
                  </li>
                </ul>
              </div>

              <div className="bg-gray-50 rounded-xl p-5 border border-gray-100">
                 <h4 className="font-semibold text-gray-900 mb-4">Dependencies</h4>
                 <div className="text-sm text-gray-600">
                    {entity.dependencies ? (
                        <ul className="list-disc pl-4 space-y-1">
                            {entity.dependencies.map((dep, i) => <li key={i}>{dep}</li>)}
                        </ul>
                    ) : (
                        <p>None</p>
                    )}
                 </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex justify-end space-x-3">
          <button 
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 font-medium transition-colors"
          >
            Cancel
          </button>
          <button 
            onClick={() => {
              alert(`Installing ${entity.name}...`);
              onClose();
            }}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors flex items-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>Install to Workspace</span>
          </button>
        </div>
      </div>
    </div>
  );
};
