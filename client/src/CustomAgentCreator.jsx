import React, { useState, useEffect } from 'react';
import { Plus, Check, Loader2, Bot, AlertCircle, ArrowRight, ArrowLeft } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export default function CustomAgentCreator() {
  const { activeWorkspace, apiFetch } = useWorkspace();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    color: 'blue',
    emoji: '🤖',
    vibe: '',
    intro_paragraph: '',
    role: '',
    personality: '',
    memory: '',
    experience: '',
    mission: '',
    rules: '',
    deliverables: '',
    communication: '',
    learning: '',
    success_metrics: '',
    advanced_capabilities: '',
    instructions_reference: '',
    domain: 'specialized',
    base_model: 'gpt-4o'
  });

  const fetchAgents = async () => {
    if (!activeWorkspace || !activeWorkspace.id) {
      console.log('⏳ Workspace not loaded yet, skipping agent fetch');
      return;
    }
    
    try {
      const res = await apiFetch('/api/v1/custom_agents');
      
      if (res.ok) {
        const data = await res.json();
        setAgents(data);
        console.log('✅ Fetched agents:', data.length);
      } else {
        console.error('❌ Failed to fetch agents:', res.status, await res.text());
      }
    } catch (err) {
      console.error('❌ Error fetching agents:', err);
    }
  };

  useEffect(() => {
    if (activeWorkspace) {
      fetchAgents();
    }
  }, [activeWorkspace]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  
  const handleAutoFill = () => {
    setFormData({
      name: 'Backend Architect',
      description: 'Senior backend architect specializing in scalable system design, database architecture, API development, and cloud infrastructure.',
      color: 'blue',
      emoji: '🏗️',
      vibe: 'Designs the systems that hold everything up — databases, APIs, cloud, scale.',
      intro_paragraph: 'You are **Backend Architect**, a senior backend architect who specializes in scalable system design, database architecture, and cloud infrastructure. You build robust, secure, and performant server-side applications that can handle massive scale while maintaining reliability and security.',
      role: 'System architecture and server-side development specialist',
      personality: 'Strategic, security-focused, scalability-minded, reliability-obsessed',
      memory: 'You remember successful architecture patterns, performance optimizations, and security frameworks',
      experience: 'You\'ve seen systems succeed through proper architecture and fail through technical shortcuts',
      mission: '### Data/Schema Engineering Excellence\n- Define and maintain data schemas and index specifications\n- Design efficient data structures for large-scale datasets (100k+ entities)\n- Implement ETL pipelines for data transformation and unification\n- Create high-performance persistence layers with sub-20ms query times\n- Stream real-time updates via WebSocket with guaranteed ordering\n- Validate schema compliance and maintain backwards compatibility\n\n### Design Scalable System Architecture\n- Create microservices architectures that scale horizontally and independently\n- Design database schemas optimized for performance, consistency, and growth\n- Implement robust API architectures with proper versioning and documentation\n- Build event-driven systems that handle high throughput and maintain reliability\n- **Default requirement**: Include comprehensive security measures and monitoring in all systems\n\n### Ensure System Reliability\n- Implement proper error handling, circuit breakers, and graceful degradation\n- Design backup and disaster recovery strategies for data protection\n- Create monitoring and alerting systems for proactive issue detection\n- Build auto-scaling systems that maintain performance under varying loads\n\n### Optimize Performance and Security\n- Design caching strategies that reduce database load and improve response times\n- Implement authentication and authorization systems with proper access controls\n- Create data pipelines that process information efficiently and reliably\n- Ensure compliance with security standards and industry regulations',
      rules: '### Security-First Architecture\n- Implement defense in depth strategies across all system layers\n- Use principle of least privilege for all services and database access\n- Encrypt data at rest and in transit using current security standards\n- Design authentication and authorization systems that prevent common vulnerabilities\n\n### Performance-Conscious Design\n- Design for horizontal scaling from the beginning\n- Implement proper database indexing and query optimization\n- Use caching strategies appropriately without creating consistency issues\n- Monitor and measure performance continuously',
      deliverables: '### System Architecture Design\n```markdown\n# System Architecture Specification\n\n## High-Level Architecture\n**Architecture Pattern**: [Microservices/Monolith/Serverless/Hybrid]\n**Communication Pattern**: [REST/GraphQL/gRPC/Event-driven]\n**Data Pattern**: [CQRS/Event Sourcing/Traditional CRUD]\n**Deployment Pattern**: [Container/Serverless/Traditional]\n\n## Service Decomposition\n### Core Services\n**User Service**: Authentication, user management, profiles\n- Database: PostgreSQL with user data encryption\n- APIs: REST endpoints for user operations\n- Events: User created, updated, deleted events\n```\n\n### Database Architecture\n```sql\n-- Example: E-commerce Database Schema Design\n\n-- Users table with proper indexing and security\nCREATE TABLE users (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    email VARCHAR(255) UNIQUE NOT NULL,\n    password_hash VARCHAR(255) NOT NULL,\n    first_name VARCHAR(100) NOT NULL,\n    last_name VARCHAR(100) NOT NULL,\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),\n    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),\n    deleted_at TIMESTAMP WITH TIME ZONE NULL\n);\n```',
      communication: '- **Be strategic**: "Designed microservices architecture that scales to 10x current load"\n- **Focus on reliability**: "Implemented circuit breakers and graceful degradation for 99.9% uptime"\n- **Think security**: "Added multi-layer security with OAuth 2.0, rate limiting, and data encryption"\n- **Ensure performance**: "Optimized database queries and caching for sub-200ms response times"',
      learning: 'Remember and build expertise in:\n- **Architecture patterns** that solve scalability and reliability challenges\n- **Database designs** that maintain performance under high load\n- **Security frameworks** that protect against evolving threats\n- **Monitoring strategies** that provide early warning of system issues\n- **Performance optimizations** that improve user experience and reduce costs',
      success_metrics: "You're successful when:\n- API response times consistently stay under 200ms for 95th percentile\n- System uptime exceeds 99.9% availability with proper monitoring\n- Database queries perform under 100ms average with proper indexing\n- Security audits find zero critical vulnerabilities\n- System successfully handles 10x normal traffic during peak loads",
      advanced_capabilities: '### Microservices Architecture Mastery\n- Service decomposition strategies that maintain data consistency\n- Event-driven architectures with proper message queuing\n- API gateway design with rate limiting and authentication\n- Service mesh implementation for observability and security\n\n### Database Architecture Excellence\n- CQRS and Event Sourcing patterns for complex domains\n- Multi-region database replication and consistency strategies\n- Performance optimization through proper indexing and query design\n- Data migration strategies that minimize downtime\n\n### Cloud Infrastructure Expertise\n- Serverless architectures that scale automatically and cost-effectively\n- Container orchestration with Kubernetes for high availability\n- Multi-cloud strategies that prevent vendor lock-in\n- Infrastructure as Code for reproducible deployments',
      instructions_reference: 'Your detailed architecture methodology is in your core training - refer to comprehensive system design patterns, database optimization techniques, and security frameworks for complete guidance.',
      domain: 'engineering',
      base_model: 'gpt-4o'
    });
  };

  const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, 8));
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    // CRITICAL FIX 1: Check if workspace is loaded before proceeding
    if (!activeWorkspace || !activeWorkspace.id) {
      setError('Workspace not loaded. Please wait and try again.');
      setLoading(false);
      return;
    }

    // CRITICAL FIX 2: Clean payload with proper defaults to match Pydantic schema
    const payload = {
      identity: {
        name: formData.name,
        role: formData.role,
        domain: formData.domain || 'specialized',
        base_model: formData.base_model || 'gpt-4o',
        description: formData.description || '',
        color: formData.color || 'blue',
        emoji: formData.emoji || '🤖',
        vibe: formData.vibe || '',
        intro_paragraph: formData.intro_paragraph || ''
      },
      system_rules: {
        mission: formData.mission || '',
        rules: formData.rules || '',
        personality: formData.personality || '',
        memory: formData.memory || '',
        experience: formData.experience || '',
        deliverables: formData.deliverables || '',
        communication: formData.communication || '',
        learning: formData.learning || '',
        success_metrics: formData.success_metrics || '',
        advanced_capabilities: formData.advanced_capabilities || '',
        instructions_reference: formData.instructions_reference || ''
      },
      capabilities: [],
      constraints: [],
      system_prompt: formData.mission || ''
    };

    try {
      console.log('Creating agent with payload:', JSON.stringify(payload, null, 2));
      console.log('Using workspace ID:', activeWorkspace.id);

      const res = await apiFetch('/api/v1/custom_agents', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      // CRITICAL FIX 4: Log the full error response for debugging
      if (!res.ok) {
        const errorText = await res.text();
        console.error('❌ Server response status:', res.status);
        console.error('❌ Server response body:', errorText);
        
        let errorMessage = 'Failed to create custom agent';
        try {
          const errorJson = JSON.parse(errorText);
          if (errorJson.detail) {
            if (Array.isArray(errorJson.detail)) {
              // Pydantic validation errors
              errorMessage = `Validation Error: ${JSON.stringify(errorJson.detail, null, 2)}`;
            } else {
              errorMessage = errorJson.detail;
            }
          }
        } catch {
          errorMessage = errorText || errorMessage;
        }
        
        setError(errorMessage);
        setLoading(false);
        return;
      }

      setSuccess('Custom agent created successfully!');
      setFormData({
        name: '',
        description: '',
        color: 'blue',
        emoji: '🤖',
        vibe: '',
        intro_paragraph: '',
        role: '',
        personality: '',
        memory: '',
        experience: '',
        mission: '',
        rules: '',
        deliverables: '',
        communication: '',
        learning: '',
        success_metrics: '',
        advanced_capabilities: '',
        instructions_reference: '',
        domain: 'specialized',
        base_model: 'gpt-4o'
      });
      setCurrentStep(1);
      fetchAgents();
    } catch (err) {
      console.error('❌ Caught error during agent creation:', err);
      setError(err.message || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  const renderStepIndicator = () => {
    const steps = ['Meta', 'Identity', 'Mission', 'Rules', 'Deliverables', 'Comms', 'Metrics', 'Review'];
    return (
      <div className="flex items-center justify-between mb-8 overflow-x-auto pb-4">
        {steps.map((step, index) => (
          <div key={index} className="flex flex-col items-center min-w-[60px] mx-1">
            <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold mb-1 transition-colors ${currentStep > index + 1 ? 'bg-green-500 text-white' : currentStep === index + 1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
              {currentStep > index + 1 ? <Check className="w-3 h-3" /> : index + 1}
            </div>
            <span className={`text-[10px] text-center ${currentStep === index + 1 ? 'font-semibold text-blue-600' : 'text-gray-500'}`}>{step}</span>
          </div>
        ))}
      </div>
    );
  };

  const generatePreview = () => {
    return `---
name: ${formData.name}
description: ${formData.description}
color: ${formData.color}
emoji: ${formData.emoji}
vibe: ${formData.vibe}
---

# ${formData.name} Agent Personality
${formData.intro_paragraph ? '\n' + formData.intro_paragraph + '\n' : ''}
## 🧠 Your Identity & Memory
- **Role**: ${formData.role}
- **Personality**: ${formData.personality}
- **Memory**: ${formData.memory}
- **Experience**: ${formData.experience}

## 🎯 Your Core Mission
${formData.mission}

## 🚨 Critical Rules You Must Follow
${formData.rules}

## 📋 Your Architecture Deliverables
${formData.deliverables}

## 💭 Your Communication Style
${formData.communication}

## 🔄 Learning & Memory
${formData.learning}

## 🎯 Your Success Metrics
${formData.success_metrics}

## 🚀 Advanced Capabilities
${formData.advanced_capabilities}

${formData.instructions_reference ? `---

**Instructions Reference**: ${formData.instructions_reference}` : ''}
`;
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-xl font-bold text-gray-800 mb-2 flex items-center">
          <Bot className="w-6 h-6 mr-2 text-blue-600" /> Custom Agent Wizard
        </h2>
        
        <div className="flex justify-between items-center mb-6">
          <p className="text-gray-600">Create a rich, specialized agent following the comprehensive standard template.</p>
          <button type="button" onClick={handleAutoFill} className="text-xs bg-blue-50 text-blue-600 hover:bg-blue-100 px-3 py-1.5 rounded-md font-medium border border-blue-200 transition-colors flex items-center">
            <Bot className="w-3.5 h-3.5 mr-1.5" /> Auto-Fill Architect
          </button>
        </div>

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
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 1: Meta Configuration</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Agent Name</label>
                  <input type="text" name="name" required value={formData.name} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. Backend Architect" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Emoji</label>
                  <input type="text" name="emoji" value={formData.emoji} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. 🏗️" />
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea name="description" rows={2} value={formData.description} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Short description of the agent's specialization" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Color</label>
                  <input type="text" name="color" value={formData.color} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. blue" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Vibe</label>
                  <input type="text" name="vibe" value={formData.vibe} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. Designs the systems that hold everything up" />
                </div>
                 <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Intro Paragraph / Personality Summary</label>
                  <textarea name="intro_paragraph" rows={3} value={formData.intro_paragraph} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. You are Backend Architect, a senior backend architect who specializes in..." />
                </div>

                 <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Base Model</label>
                  <select name="base_model" value={formData.base_model} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                    <option value="gemini-1.5-pro">Gemini 1.5 Pro</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Domain</label>
                  <select name="domain" value={formData.domain} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none">
                    <option value="specialized">Specialized</option>
                    <option value="marketing">Marketing</option>
                    <option value="finance">Finance</option>
                    <option value="engineering">Engineering</option>
                    <option value="design">Design</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 2: 🧠 Identity & Memory</h3>
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                  <input type="text" name="role" required value={formData.role} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. System architecture and server-side development specialist" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Personality</label>
                  <input type="text" name="personality" value={formData.personality} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. Strategic, security-focused, scalability-minded" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Memory</label>
                  <textarea name="memory" rows={2} value={formData.memory} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. You remember successful architecture patterns..." />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Experience</label>
                  <textarea name="experience" rows={2} value={formData.experience} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="e.g. You've seen systems succeed through proper architecture..." />
                </div>
              </div>
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 3: 🎯 Core Mission</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Mission Details (Markdown)</label>
                <textarea name="mission" rows={10} value={formData.mission} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="### Goal Category 1&#10;- specific objective 1&#10;- specific objective 2" />
              </div>
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 4: 🚨 Critical Rules</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Rules (Markdown)</label>
                <textarea name="rules" rows={10} value={formData.rules} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="### Rule Category 1&#10;- specific rule 1&#10;- specific rule 2" />
              </div>
            </div>
          )}

          {currentStep === 5 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 5: 📋 Deliverables</h3>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Deliverables (Markdown)</label>
                <textarea name="deliverables" rows={10} value={formData.deliverables} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="### Deliverable Type 1&#10;```markdown&#10;Example template&#10;```" />
              </div>
            </div>
          )}
          
          {currentStep === 6 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 6: 💭 Communication & Learning</h3>
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Communication Style (Markdown)</label>
                  <textarea name="communication" rows={5} value={formData.communication} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="- **Style**: Example..." />
                </div>
                 <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Learning & Memory (Markdown)</label>
                  <textarea name="learning" rows={5} value={formData.learning} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="Remember and build expertise in:&#10;- Topic 1..." />
                </div>
              </div>
            </div>
          )}
          
          {currentStep === 7 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 7: 🎯 Metrics & Capabilities</h3>
              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Success Metrics (Markdown)</label>
                  <textarea name="success_metrics" rows={5} value={formData.success_metrics} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="You're successful when:&#10;- Metric 1..." />
                </div>
                 <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Advanced Capabilities (Markdown)</label>
                  <textarea name="advanced_capabilities" rows={5} value={formData.advanced_capabilities} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="### Capability Area 1\n- specific skill 1..." />
                </div>
                 <div className="md:col-span-1">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Instructions Reference</label>
                  <textarea name="instructions_reference" rows={3} value={formData.instructions_reference} onChange={handleInputChange} className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none font-mono text-sm" placeholder="e.g. Your detailed architecture methodology is in your core training..." />
                </div>

              </div>
            </div>
          )}

          {currentStep === 8 && (
            <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-300">
              <h3 className="text-lg font-medium text-gray-800 border-b pb-2">Step 8: Review & Generate</h3>
              
              <div className="bg-gray-50 p-4 rounded-lg text-sm text-gray-700">
                <p className="font-semibold mb-2">Full Markdown Preview:</p>
                <pre className="bg-gray-800 text-gray-100 p-4 rounded overflow-auto text-xs font-mono h-96">
                  {generatePreview()}
                </pre>
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
            
            {currentStep < 8 ? (
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
                disabled={loading || !formData.name || !formData.role}
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
