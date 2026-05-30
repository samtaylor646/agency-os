import React, { useState } from 'react';
import { ShieldAlert, CheckCircle2, AlertTriangle, X } from 'lucide-react';

export const AgentApprovalModal = ({ agent, capabilities, onApprove, onCancel }) => {
  const [selectedSkills, setSelectedSkills] = useState(
    capabilities.reduce((acc, cap) => ({ ...acc, [cap]: false }), {})
  );

  const toggleSkill = (skill) => {
    setSelectedSkills(prev => ({
      ...prev,
      [skill]: !prev[skill]
    }));
  };

  const handleApprove = () => {
    const approvedSkills = Object.keys(selectedSkills).filter(skill => selectedSkills[skill]);
    onApprove(approvedSkills);
  };

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center p-4 bg-gray-900/75 backdrop-blur-sm">
      <div className="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl flex flex-col">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-amber-50">
          <div className="flex items-center space-x-3">
            <ShieldAlert className="w-6 h-6 text-amber-600" />
            <h2 className="text-xl font-bold text-gray-900">Human-in-the-Loop Security Gate</h2>
          </div>
          <button onClick={onCancel} className="text-gray-400 hover:text-gray-600 transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto">
          <div className="mb-6 flex items-start space-x-4 bg-blue-50 p-4 rounded-xl border border-blue-100">
            <div className="mt-1">
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
              </span>
            </div>
            <div>
              <h3 className="text-sm font-bold text-blue-900 mb-1">Agent in Draft Status</h3>
              <p className="text-sm text-blue-800">
                The agent <strong>{agent?.name}</strong> has been successfully upscaled but requires explicit approval for its Model Context Protocol (MCP) skills before activation.
              </p>
            </div>
          </div>

          <h3 className="text-lg font-semibold text-gray-900 mb-4">Review Required Capabilities</h3>
          <p className="text-sm text-gray-600 mb-4">
            Select the capabilities you wish to authorize for this agent. Unapproved skills will be strictly denied during execution.
          </p>

          <div className="space-y-3">
            {capabilities.length === 0 ? (
              <p className="text-sm text-gray-500 italic">No specific MCP skills required.</p>
            ) : (
              capabilities.map((cap, index) => (
                <label 
                  key={index} 
                  className={`flex items-start space-x-3 p-4 rounded-xl border transition-colors cursor-pointer ${
                    selectedSkills[cap] ? 'border-indigo-500 bg-indigo-50/50' : 'border-gray-200 bg-gray-50 hover:bg-gray-100'
                  }`}
                >
                  <div className="mt-0.5">
                    <input 
                      type="checkbox" 
                      className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500 focus:ring-offset-0"
                      checked={selectedSkills[cap] || false}
                      onChange={() => toggleSkill(cap)}
                    />
                  </div>
                  <div className="flex-1">
                    <div className="text-sm font-semibold text-gray-900">{cap}</div>
                    <div className="text-xs text-gray-500 mt-1">Allows the agent to execute tools related to {cap}.</div>
                  </div>
                </label>
              ))
            )}
          </div>

          <div className="mt-6 flex items-start space-x-2 text-sm text-amber-700 bg-amber-50/50 p-3 rounded-lg">
            <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
            <p>Ensure you trust the agent's author before granting access to sensitive workspace capabilities.</p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-100 bg-gray-50 flex justify-end space-x-3">
          <button 
            onClick={onCancel}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 font-medium transition-colors"
          >
            Deny & Cancel
          </button>
          <button 
            onClick={handleApprove}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors flex items-center space-x-2"
          >
            <CheckCircle2 className="w-4 h-4" />
            <span>Approve Capabilities & Activate</span>
          </button>
        </div>
      </div>
    </div>
  );
};
