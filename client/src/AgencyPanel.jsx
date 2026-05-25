import React, { useState, useEffect } from 'react';
import { useWorkspace } from './WorkspaceContext';
import { ContextSwitcher } from './ContextSwitcher';
import { CredentialsManager } from './CredentialsManager';
import { RBACManager } from './RBACManager';
import { AuditLogViewer } from './AuditLogViewer';
import { AnalyticsDashboard } from './AnalyticsDashboard';
import { Marketplace } from './Marketplace';
import CustomAgentCreator from './CustomAgentCreator';
import ChatScopeInterface from './ChatScopeInterface';
import PipelineExecutionViewer from './PipelineExecutionViewer';
import { Users, Settings, Activity, FileText, Share2, Plus, ArrowRight, Play, CheckCircle, Clock, AlertCircle, Shield, Database, Store, BarChart2, Menu, X, Search, Send, MessageSquare, Bot, Cpu } from 'lucide-react';

const SidebarItem = ({ icon: Icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg mb-1 transition-colors ${
      active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600 hover:bg-gray-50'
    }`}
  >
    <Icon className="w-5 h-5" />
    <span>{label}</span>
  </button>
);

// --- Workflows UI ---
const WorkflowManager = () => {
  const [running, setRunning] = useState(false);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const runWorkflow = async () => {
    setRunning(true);
    setStatus('Running workflow...');
    setError(null);
    setResults(null);

    const workflowPayload = {
      nodes: [
        { node_id: "step1", agent_name: "Strategy", task: "Plan the marketing campaign", required_inputs: [] },
        { node_id: "step2", agent_name: "Copywriter", task: "Write copy for the campaign", required_inputs: ["step1"] }
      ],
      edges: [
        { from_node: "step1", to_node: "step2" }
      ]
    };

    try {
      // Assuming a token might be needed in a real app, for MVP we just hit the endpoint.
      // Wait, let's just make the request. We might need a token if auth is required, but we can try without or just pass a dummy one if not enforced strictly.
      // Actually /workflows/run has current_user = Depends(auth.get_current_user)
      // For the sake of the MVP UI we'll just demonstrate the fetch.
      // We should probably get a token first.
      
      const tokenRes = await fetch('/api/v1/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: 'admin@agencyos.com',
          password: 'password123' // default pass from MVP specs
        })
      });
      
      let token = '';
      if (tokenRes.ok) {
        const tokenData = await tokenRes.json();
        token = tokenData.access_token;
      }

      const res = await fetch('/api/v1/workflows/run', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify(workflowPayload)
      });
      
      if (!res.ok) {
        throw new Error(`Failed to run workflow: ${res.statusText}`);
      }

      const data = await res.json();
      setResults(data.results);
      setStatus('Workflow completed successfully');
    } catch (err) {
      setError(err.message);
      setStatus('Workflow failed');
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-xl font-bold text-gray-800 mb-4">DAG Orchestrator Dashboard</h2>
        <p className="text-gray-600 mb-6">Run workflows and monitor agent tasks.</p>
        
        <button 
          onClick={runWorkflow}
          disabled={running}
          className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {running ? <Clock className="w-5 h-5 animate-spin" /> : <Play className="w-5 h-5" />}
          <span>{running ? 'Running Workflow...' : 'Run Test Workflow'}</span>
        </button>

        {status && (
          <div className={`mt-4 p-4 rounded-lg flex items-center space-x-3 ${error ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
            {error ? <AlertCircle className="w-5 h-5" /> : <CheckCircle className="w-5 h-5" />}
            <span>{status}</span>
          </div>
        )}

        {results && (
          <div className="mt-6">
            <h3 className="font-semibold text-gray-800 mb-2">Execution Results:</h3>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-auto border border-gray-200 text-sm">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
};

// --- Workspaces Admin View ---
const WorkspaceManagementUI = () => {
  const { activeWorkspace } = useWorkspace();
  
  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <h2 className="text-xl font-bold text-gray-800 mb-4">Workspace Settings: {activeWorkspace?.name}</h2>
        <p className="text-gray-600 mb-6">Manage settings and integrations for this specific client workspace.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 border border-gray-200 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">API Keys</h3>
            <p className="text-sm text-gray-500 mb-4">Manage API access for this workspace.</p>
            <button className="text-blue-600 text-sm font-medium hover:underline" onClick={() => alert("Manage Keys action triggered")}>Manage Keys</button>
          </div>
          <div className="p-4 border border-gray-200 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Billing Context</h3>
            <p className="text-sm text-gray-500 mb-4">View usage limits for {activeWorkspace?.name}.</p>
            <button className="text-blue-600 text-sm font-medium hover:underline" onClick={() => alert("View Usage action triggered")}>View Usage</button>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Users & Invites</h2>
          <button className="flex items-center space-x-1 bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm hover:bg-blue-700 transition-colors" onClick={() => alert("Invite User action triggered")}>
            <Plus className="w-4 h-4" />
            <span>Invite User</span>
          </button>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 text-sm">
                <th className="py-3 font-medium">User</th>
                <th className="py-3 font-medium">Role</th>
                <th className="py-3 font-medium">Status</th>
                <th className="py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-gray-100 text-sm">
                <td className="py-3 text-gray-800">admin@agency.com</td>
                <td className="py-3 text-gray-600">Agency Admin</td>
                <td className="py-3 text-green-600">Active</td>
                <td className="py-3"><button className="text-gray-400 hover:text-gray-600">Edit</button></td>
              </tr>
              <tr className="border-b border-gray-100 text-sm">
                <td className="py-3 text-gray-800">client@acme.com</td>
                <td className="py-3 text-gray-600">Client Approver</td>
                <td className="py-3 text-yellow-600">Pending</td>
                <td className="py-3"><button className="text-gray-400 hover:text-gray-600">Edit</button></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <CredentialsManager />
    </div>
  );
};

// --- Client Portal View ---
const ClientPortalView = () => {
  const { activeWorkspace } = useWorkspace();

  return (
    <div className="space-y-6">
      <div className="bg-blue-50 border border-blue-100 p-6 rounded-xl">
        <h2 className="text-xl font-bold text-blue-900 mb-2">Welcome back to {activeWorkspace?.name} Portal</h2>
        <p className="text-blue-700">View your active campaigns, approve content, and track performance.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-gray-700 mb-1">Pending Approvals</h3>
            <p className="text-3xl font-bold text-gray-900 mb-4">3</p>
            <p className="text-sm text-gray-500">2 Social Posts, 1 Blog Article</p>
          </div>
          <button className="mt-4 flex items-center text-blue-600 text-sm font-medium hover:underline">
            Review Now <ArrowRight className="w-4 h-4 ml-1" />
          </button>
        </div>
        
        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-gray-700 mb-1">Active Pipelines</h3>
            <p className="text-3xl font-bold text-gray-900 mb-4">2</p>
            <p className="text-sm text-green-600">All running smoothly</p>
          </div>
          <button className="mt-4 flex items-center text-blue-600 text-sm font-medium hover:underline">
            View Details <ArrowRight className="w-4 h-4 ml-1" />
          </button>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-100 shadow-sm flex flex-col justify-between">
          <div>
            <h3 className="font-semibold text-gray-700 mb-1">Recent Reports</h3>
            <p className="text-3xl font-bold text-gray-900 mb-4">Q2</p>
            <p className="text-sm text-gray-500">Performance Summary</p>
          </div>
          <button className="mt-4 flex items-center text-blue-600 text-sm font-medium hover:underline">
            Download <ArrowRight className="w-4 h-4 ml-1" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default function AgencyPanel() {
  const { userRole, setUserRole, activeWorkspace } = useWorkspace();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  
  // Listen for the custom event to simulate creating a workspace
  useEffect(() => {
    const handleOpenCreate = () => alert('Create Workspace Modal would open here.');
    document.addEventListener('open-create-workspace', handleOpenCreate);
    return () => document.removeEventListener('open-create-workspace', handleOpenCreate);
  }, []);

  return (
    <div className="flex h-screen bg-gray-50 font-sans overflow-hidden">
      {/* Mobile sidebar overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-900 bg-opacity-50 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 flex flex-col transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-6 border-b border-gray-100 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">AgencyOS</span>
          </div>
          <button 
            className="md:hidden text-gray-500 hover:text-gray-700"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <nav className="flex-1 p-4 overflow-y-auto">
          <div className="mb-6">
            <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Workspace</p>
            <div className="px-2 mb-4">
              <ContextSwitcher />
            </div>
          </div>

          <div className="mb-6">
            <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Menu</p>
            <SidebarItem 
              icon={Activity} 
              label="Dashboard" 
              active={activeTab === 'dashboard'} 
              onClick={() => { setActiveTab('dashboard'); setIsMobileMenuOpen(false); }} 
            />
            <SidebarItem 
              icon={MessageSquare} 
              label="Project Scope" 
              active={activeTab === 'scope'} 
              onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }} 
            />
            {userRole === 'Agency Admin' && (
              <SidebarItem 
                icon={Settings} 
                label="Workspace Settings" 
                active={activeTab === 'settings'} 
                onClick={() => { setActiveTab('settings'); setIsMobileMenuOpen(false); }} 
              />
            )}
            <SidebarItem 
              icon={Cpu} 
              label="Pipeline Execution" 
              active={activeTab === 'workflows'} 
              onClick={() => { setActiveTab('workflows'); setIsMobileMenuOpen(false); }} 
            />
            {userRole === 'Agency Admin' && (
              <SidebarItem 
                icon={Bot} 
                label="Custom Agents" 
                active={activeTab === 'agents'} 
                onClick={() => { setActiveTab('agents'); setIsMobileMenuOpen(false); }} 
              />
            )}
            <SidebarItem 
              icon={FileText} 
              label="Files & Assets" 
              active={activeTab === 'files'} 
              onClick={() => { setActiveTab('files'); setIsMobileMenuOpen(false); }} 
            />
            {userRole === 'Agency Admin' && (
              <>
                <div className="mt-6 mb-2">
                  <p className="px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider">Administration</p>
                </div>
                <SidebarItem 
                  icon={BarChart2} 
                  label="Analytics" 
                  active={activeTab === 'analytics'} 
                  onClick={() => { setActiveTab('analytics'); setIsMobileMenuOpen(false); }} 
                />
                <SidebarItem 
                  icon={Shield} 
                  label="Access Control" 
                  active={activeTab === 'rbac'} 
                  onClick={() => { setActiveTab('rbac'); setIsMobileMenuOpen(false); }} 
                />
                <SidebarItem 
                  icon={Database} 
                  label="Audit Logs" 
                  active={activeTab === 'audit'} 
                  onClick={() => { setActiveTab('audit'); setIsMobileMenuOpen(false); }} 
                />
                <SidebarItem 
                  icon={Store} 
                  label="Marketplace" 
                  active={activeTab === 'marketplace'} 
                  onClick={() => { setActiveTab('marketplace'); setIsMobileMenuOpen(false); }} 
                />
              </>
            )}
          </div>
        </nav>

        {/* Demo Role Switcher (For Development) */}
        <div className="p-4 border-t border-gray-200 bg-gray-50">
          <p className="text-xs text-gray-500 mb-2">Simulate Role:</p>
          <select 
            value={userRole}
            onChange={(e) => {
              setUserRole(e.target.value);
              setActiveTab('dashboard'); // Reset tab on role switch
            }}
            className="w-full text-sm p-2 border border-gray-300 rounded bg-white"
          >
            <option value="Agency Admin">Agency Admin</option>
            <option value="Client Approver">Client Approver</option>
          </select>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-4 sm:px-8">
          <div className="flex items-center">
            <button 
              className="md:hidden mr-3 text-gray-500 hover:text-gray-700"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-lg sm:text-xl font-semibold text-gray-800 capitalize truncate">
              {activeTab === 'dashboard' ? (userRole === 'Agency Admin' ? 'Agency Overview' : 'Client Dashboard') : activeTab}
            </h1>
          </div>
          <div className="flex items-center space-x-2 sm:space-x-4 ml-2">
            <span className="text-xs sm:text-sm text-gray-500 hidden sm:inline">Logged in as <strong className="text-gray-700">{userRole}</strong></span>
            <div className="w-8 h-8 bg-gray-200 rounded-full border border-gray-300 flex-shrink-0"></div>
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-4 sm:p-8 flex flex-col">
          <div className="max-w-5xl mx-auto w-full flex-1 mb-20">
            {activeTab === 'dashboard' && (
              userRole === 'Agency Admin' ? (
                <div>
                  <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6">Agency Overview: {activeWorkspace?.name}</h2>
                  <p className="text-gray-600">Select "Workspace Settings" to manage this tenant, or switch workspaces using the dropdown in the sidebar.</p>
                </div>
              ) : (
                <ClientPortalView />
              )
            )}
            {activeTab === 'scope' && (
              <div className="h-[calc(100vh-10rem)] w-full bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <ChatScopeInterface />
              </div>
            )}
            {activeTab === 'settings' && userRole === 'Agency Admin' && (
              <WorkspaceManagementUI />
            )}
            {activeTab === 'agents' && userRole === 'Agency Admin' && (
              <CustomAgentCreator />
            )}
            {activeTab === 'workflows' && (
              <PipelineExecutionViewer />
            )}
            {activeTab === 'files' && (
              <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center py-12">
                <Share2 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-700 mb-1">File Manager</h3>
                <p className="text-gray-500">Tenant-isolated file storage would be implemented here.</p>
              </div>
            )}
            {activeTab === 'analytics' && userRole === 'Agency Admin' && (
              <AnalyticsDashboard />
            )}
            {activeTab === 'rbac' && userRole === 'Agency Admin' && (
              <RBACManager />
            )}
            {activeTab === 'audit' && userRole === 'Agency Admin' && (
              <AuditLogViewer />
            )}
            {activeTab === 'marketplace' && userRole === 'Agency Admin' && (
              <Marketplace />
            )}
          </div>
          
          {/* Chat Prompt Box */}
          <div className="max-w-3xl mx-auto w-full mt-auto fixed bottom-6 left-0 right-0 md:pl-64 px-4 pointer-events-none">
            <div className="bg-white rounded-full shadow-lg border border-gray-200 p-2 flex items-center pointer-events-auto">
              <Search className="w-5 h-5 text-gray-400 ml-3 mr-2" />
              <input
                type="text"
                placeholder="Ask AgencyOS a question or generate a workflow..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 px-1 outline-none text-gray-800"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && chatInput) {
                    alert(`Message sent: ${chatInput}`);
                    setChatInput('');
                  }
                }}
              />
              <button 
                className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 transition-colors ml-2"
                onClick={() => {
                  if (chatInput) {
                    alert(`Message sent: ${chatInput}`);
                    setChatInput('');
                  }
                }}
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
