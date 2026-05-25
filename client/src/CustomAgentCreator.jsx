import React, { useState, useEffect } from 'react';
import { Plus, Check, Loader2, Bot, AlertCircle, ArrowRight, ArrowLeft } from 'lucide-react';

export default function CustomAgentCreator() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  
  const [formData, setFormData] = useState({
    identity_name: '',
    identity_role: '',
    identity_version: '1.0.0',
    system_rules_path: 'config/settings.md',
    system_rules_enforcement_level: 'strict',
    capabilities: '',
    constraints: '',
    system_prompt: ''
  });

  const fetchAgents = async () => {
    try {
      const res = await fetch('/api/v1/custom_agents');
      if (res.ok) {
        const data = await res.json();
        setAgents(data);
      }
    } catch (err) {
      console.error('Failed to fetch agents', err);
    }
  };

  useEffect(() => {
    fetchAgents();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, 4));
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  const parseMarkdownList = (text) => {
    if (!text) return [];
    return text.split('\n')
      .map(line => line.replace(/^-\s*/, '').trim())
      .filter(line => line.length > 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const payload = {
      identity: {
        name: formData.identity_name,
        role: formData.identity_role,
        version: formData.identity_version
      },
      system_rules: {
        path: formData.system_rules_path,
        enforcement_level: formData.system_rules_enforcement_level
      },
      capabilities: parseMarkdownList(formData.capabilities),
      constraints: parseMarkdownList(formData.constraints),
      system_prompt: formData.system_prompt
    };

    try {
      const res = await fetch('/api/v1/custom_agents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        throw new Error('Failed to create custom agent');
      }

      setSuccess('Custom agent created successfully!');
      setFormData({
        identity_name: '',
        identity_role: '',
        identity_version: '1.0.0',
        system_rules_path: 'config/settings.md',
        system_rules_enforcement_level: 'strict',
        capabilities: '',
        constraints: '',
        system_prompt: ''
      });
      setCurrentStep(1);
      fetchAgents();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderStepIndicator = () => {
    const steps = ['Identity', 'Rules & Constraints', 'Capabilities', 'Prompt & Review'];
    return (
      <div className="flex items-center justify-between mb-8">
        {steps.map((step, index) => (
          <div key={index} className="flex flex-col items-center w-1/4">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold mb-2 transition-colors ${currentStep > index + 1 ? 'bg-green-500 text-white' : currentStep === index + 1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
              {currentStep > index + 1 ? <Check className="w-5 h-5" /> : index + 1}
            </div>
            <span className={`text-xs text-center ${currentStep === index + 1 ? 'font-semibold text-blue-600' : 'text-gray-500'}`}>{step}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-xl font-bold text-gray-800 mb-2 flex items-center">
          <Bot className="w-6 h-6 mr-2 text-blue-600" /> Custom Agent Wizard
        </h2>
        <p className="text-gray-600 mb-6">Create a highly specialized agent following the standard configuration template.</p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 mr-2 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-50 text-green-700 rounded-lg flex items-center">
            <Check className="w-5 h-5 mr-2 flex-shrink-0" />
            <span>{success}</span>
          </div>
        )}

        {renderStepIndicator()}

        <form onSubmit={handleSubmit}>
          {currentStep === 1 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 1: Agent Identity</h3>
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Agent Name</label>
                  <input
                    type="text"
                    name="identity_name"
                    required
                    value={formData.identity_name}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    placeholder="e.g. Content Optimizer"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                  <input
                    type="text"
                    name="identity_role"
                    required
                    value={formData.identity_role}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    placeholder="e.g. SEO Specialist"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
                  <input
                    type="text"
                    name="identity_version"
                    required
                    value={formData.identity_version}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    placeholder="1.0.0"
                  />
                </div>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 2: Rules & Constraints</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">System Rules Path</label>
                  <input
                    type="text"
                    name="system_rules_path"
                    required
                    value={formData.system_rules_path}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Enforcement Level</label>
                  <select
                    name="system_rules_enforcement_level"
                    value={formData.system_rules_enforcement_level}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  >
                    <option value="strict">Strict</option>
                    <option value="moderate">Moderate</option>
                    <option value="relaxed">Relaxed</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Constraints (Markdown list)</label>
                <textarea
                  name="constraints"
                  required
                  rows={4}
                  value={formData.constraints}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                  placeholder="- Must not use black-hat SEO tactics&#10;- Ensure all suggestions are accessible"
                />
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 3: Capabilities</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Agent Capabilities (Markdown list)</label>
                <textarea
                  name="capabilities"
                  required
                  rows={6}
                  value={formData.capabilities}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                  placeholder="- Keyword research and analysis&#10;- Meta tag optimization&#10;- Competitor gap analysis"
                />
              </div>
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 4: System Prompt & Review</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">System Prompt</label>
                <textarea
                  name="system_prompt"
                  required
                  rows={6}
                  value={formData.system_prompt}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm"
                  placeholder="You are an expert SEO specialist tasked with optimizing web content..."
                />
              </div>
              
              <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700">
                <p className="font-semibold mb-2">Review Configuration:</p>
                <ul className="list-disc pl-5 space-y-1">
                  <li><strong>Name:</strong> {formData.identity_name || 'Not set'}</li>
                  <li><strong>Role:</strong> {formData.identity_role || 'Not set'}</li>
                  <li><strong>Capabilities:</strong> {parseMarkdownList(formData.capabilities).length} items</li>
                  <li><strong>Constraints:</strong> {parseMarkdownList(formData.constraints).length} items</li>
                </ul>
              </div>
            </div>
          )}

          <div className="flex justify-between mt-8 pt-4 border-t border-gray-100">
            <button
              type="button"
              onClick={prevStep}
              disabled={currentStep === 1 || loading}
              className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors ${currentStep === 1 ? 'opacity-0 pointer-events-none' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              <ArrowLeft className="w-4 h-4 mr-2" /> Back
            </button>
            
            {currentStep < 4 ? (
              <button
                type="button"
                onClick={nextStep}
                className="flex items-center bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                Next <ArrowRight className="w-4 h-4 ml-2" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={loading || !formData.identity_name || !formData.identity_role}
                className="flex items-center bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 font-medium"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <Check className="w-5 h-5 mr-2" />}
                Create Agent
              </button>
            )}
          </div>
        </form>
      </div>

      {agents.length > 0 && (
        <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Custom Agents Library</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {agents.map((agent) => (
              <div key={agent.id} className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition-colors bg-gray-50">
                <div className="flex items-start justify-between">
                  <div>
                    <h4 className="font-semibold text-gray-900">{agent.name}</h4>
                    <p className="text-xs text-blue-600 mb-2 font-medium">{agent.role}</p>
                  </div>
                  <Bot className="w-5 h-5 text-gray-400" />
                </div>
                <div className="mt-2 text-xs text-gray-500 truncate" title={agent.filepath}>
                  {agent.filepath}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
