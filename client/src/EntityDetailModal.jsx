import React, { useState, useEffect } from 'react';
import { X, Plus, CheckCircle2, ShieldAlert, Loader2 } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';
import { AgentApprovalModal } from './AgentApprovalModal';

export const EntityDetailModal = ({ entity, onClose }) => {
  const { apiFetch } = useWorkspace();
  const [isElevating, setIsElevating] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [showApprovalModal, setShowApprovalModal] = useState(false);
  const [draftAgent, setDraftAgent] = useState(null);
  const [draftCapabilities, setDraftCapabilities] = useState([]);

  useEffect(() => {
    let interval;
    if (isElevating && jobId) {
      interval = setInterval(async () => {
        try {
          const res = await apiFetch(`/api/v1/agents/jobs/${jobId}`);
          if (res.ok) {
            const data = await res.json();
            if (data.status === 'completed') {
              setIsElevating(false);
              setJobId(null);
              clearInterval(interval);
              
              // Fetch capabilities for the draft agent
              const capRes = await apiFetch(`/api/v1/agents/${data.agent_id}/capabilities`);
              if (capRes.ok) {
                const capData = await capRes.json();
                setDraftAgent({ id: data.agent_id, name: entity.name });
                setDraftCapabilities(capData.required_mcp_skills || []);
                setShowApprovalModal(true);
              }
            } else if (data.status === 'failed') {
              setIsElevating(false);
              setJobId(null);
              clearInterval(interval);
              alert('Agent upscaling failed.');
            }
          }
        } catch (err) {
          console.error('Error polling job status:', err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isElevating, jobId, apiFetch, entity.name]);

  const handleInstall = async () => {
    setIsElevating(true);
    try {
      const res = await apiFetch('/api/v1/agents/import', {
        method: 'POST',
        body: JSON.stringify({ template_id: entity.id })
      });
      if (res.ok) {
        const data = await res.json();
        setJobId(data.job_id);
      } else {
        setIsElevating(false);
        alert('Failed to initiate agent installation.');
      }
    } catch (err) {
      setIsElevating(false);
      console.error(err);
      alert('Error during installation.');
    }
  };

  const handleApprove = async (approvedSkills) => {
    try {
      const res = await apiFetch(`/api/v1/agents/${draftAgent.id}/approve`, {
        method: 'POST',
        body: JSON.stringify({ approved_skills: approvedSkills })
      });
      if (res.ok) {
        alert('Agent activated successfully!');
        setShowApprovalModal(false);
        onClose();
      } else {
        alert('Failed to approve agent.');
      }
    } catch (err) {
      console.error(err);
      alert('Error during approval.');
    }
  };

  if (!entity) return null;

  return (
    <>
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
            disabled={isElevating}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-full transition-colors disabled:opacity-50"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 overflow-y-auto flex-grow relative">
          {isElevating && (
            <div className="absolute inset-0 bg-white/80 backdrop-blur-sm z-10 flex flex-col items-center justify-center">
              <Loader2 className="w-12 h-12 text-indigo-600 animate-spin mb-4" />
              <h3 className="text-xl font-bold text-gray-900 mb-2">Elevating Agent...</h3>
              <p className="text-gray-600 text-center max-w-md">
                The Upscaler Meta-Agent is processing this template, generating custom YAML frontmatter, domain-specific few-shot prompting, and identifying required MCP skills.
              </p>
            </div>
          )}
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
            disabled={isElevating}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 font-medium transition-colors disabled:opacity-50"
          >
            Cancel
          </button>
          <button 
            onClick={handleInstall}
            disabled={isElevating}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 font-medium transition-colors flex items-center space-x-2 disabled:opacity-50"
          >
            {isElevating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Plus className="w-4 h-4" />}
            <span>{isElevating ? 'Installing...' : 'Install to Workspace'}</span>
          </button>
        </div>
      </div>
    </div>
    {showApprovalModal && (
      <AgentApprovalModal 
        agent={draftAgent}
        capabilities={draftCapabilities}
        onApprove={handleApprove}
        onCancel={() => { setShowApprovalModal(false); onClose(); }}
      />
    )}
    </>
  );
};
