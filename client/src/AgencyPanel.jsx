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
import CreateWorkspaceModal from './CreateWorkspaceModal';
import IntroPage from './IntroPage';
import { ApiKeysModal, InviteUserModal, EditUserModal } from './WorkspaceSettingsModals';
import { Users, Settings, Activity, FileText, Share2, Plus, ArrowRight, Play, CheckCircle, Clock, AlertCircle, Shield, Database, Store, BarChart2, Menu, X, Search, Send, MessageSquare, Bot, Cpu, PanelLeftClose, PanelLeft } from 'lucide-react';

const SidebarItem = ({ icon: Icon, label, active, onClick, collapsed }) => (
  <button 
    onClick={onClick}
    className={`group relative w-full flex items-center ${collapsed ? 'justify-center px-0' : 'space-x-3 px-3'} py-1.5 rounded-lg mb-0.5 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 ${
      active ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-600 hover:bg-gray-200 hover:text-gray-900'
    }`}
    aria-label={collapsed ? label : undefined}
    aria-current={active ? "page" : undefined}
  >
    <Icon className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
    {!collapsed && <span className="truncate">{label}</span>}
    {collapsed && (
      <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50" aria-hidden="true">
        {label}
      </div>
    )}
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
      const tokenRes = await fetch('/api/v1/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: 'admin@agencyos.com',
          password: 'password123'
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
const WorkspaceManagementUI = ({ showNotification }) => {
  const { activeWorkspace } = useWorkspace();
  const [members, setMembers] = useState([]);
  const [isApiKeysOpen, setIsApiKeysOpen] = useState(false);
  const [isInviteOpen, setIsInviteOpen] = useState(false);
  const [userToEdit, setUserToEdit] = useState(null);

  const fetchMembers = async () => {
    if (!activeWorkspace) return;
    try {
      const res = await fetch(`/api/v1/rbac/workspaces/${activeWorkspace.id}/members`);
      if (res.ok) {
        setMembers(await res.json());
      }
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchMembers();
  }, [activeWorkspace]);
  
  return (
    <div className="space-y-4 md:space-y-6">
      <ApiKeysModal isOpen={isApiKeysOpen} onClose={() => setIsApiKeysOpen(false)} showNotification={showNotification} />
      <InviteUserModal isOpen={isInviteOpen} onClose={() => setIsInviteOpen(false)} showNotification={showNotification} onInviteSuccess={fetchMembers} />
      <EditUserModal isOpen={!!userToEdit} onClose={() => setUserToEdit(null)} user={userToEdit} showNotification={showNotification} onUpdateSuccess={fetchMembers} />
      
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900 p-4 md:p-6 border-b border-gray-200 md:rounded-xl md:border md:border-gray-100 md:shadow-sm">
        <h2 className="text-lg md:text-xl font-bold text-gray-800 mb-4 tracking-tight">Workspace Settings: {activeWorkspace?.name}</h2>
        <p className="text-gray-600 mb-6">Manage settings and integrations for this specific client workspace.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4">
          <div className="p-3 md:p-4 border border-gray-200 rounded-xl flex flex-col items-start bg-gray-50 md:bg-transparent">
            <h3 className="font-medium text-gray-800 mb-1 md:mb-2 text-sm md:text-base">API Keys</h3>
            <p className="text-xs md:text-sm text-gray-500 mb-3 md:mb-4">Manage API access for this workspace.</p>
            <button className="w-full md:w-auto text-blue-600 bg-white md:bg-transparent border border-gray-200 md:border-transparent py-1.5 md:py-0 rounded-sm text-xs font-semibold md:text-sm md:font-medium hover:underline mt-auto uppercase tracking-wider md:tracking-normal md:normal-case" onClick={() => setIsApiKeysOpen(true)}>Manage Keys</button>
          </div>
          <div className="p-3 md:p-4 border border-gray-200 rounded-xl flex flex-col items-start bg-gray-50 md:bg-transparent">
            <h3 className="font-medium text-gray-800 mb-1 md:mb-2 text-sm md:text-base">Billing Context</h3>
            <p className="text-xs md:text-sm text-gray-500 mb-3 md:mb-4">View usage limits for {activeWorkspace?.name}.</p>
            <button className="w-full md:w-auto text-blue-600 bg-white md:bg-transparent border border-gray-200 md:border-transparent py-1.5 md:py-0 rounded-sm text-xs font-semibold md:text-sm md:font-medium hover:underline mt-auto uppercase tracking-wider md:tracking-normal md:normal-case" onClick={() => showNotification("Billing / Usage module not implemented yet")}>View Usage</button>
          </div>
        </div>
      </div>

      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900 p-4 md:p-6 border-b border-gray-200 md:rounded-xl md:border md:border-gray-100 md:shadow-sm">
        <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-4 gap-3">
          <h2 className="text-lg md:text-xl font-bold text-gray-800 tracking-tight">Users & Invites</h2>
          <button className="w-full md:w-auto flex items-center justify-center space-x-1 bg-blue-600 md:bg-blue-600 text-white px-3 py-2 md:py-1.5 rounded-sm md:rounded-md text-[10px] md:text-sm font-semibold uppercase tracking-wider md:tracking-normal md:normal-case md:font-normal hover:bg-blue-700 md:hover:bg-blue-700 transition-colors" onClick={() => setIsInviteOpen(true)}>
            <Plus className="w-4 h-4" />
            <span>Invite User</span>
          </button>
        </div>
        
        <div className="overflow-x-auto">
          {/* Desktop Table */}
          <table className="hidden md:table w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500 text-sm">
                <th className="py-3 font-medium">User</th>
                <th className="py-3 font-medium">Role</th>
                <th className="py-3 font-medium">Status</th>
                <th className="py-3 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody>
              {members.length === 0 && (
                <tr>
                  <td colSpan="4" className="py-4 text-center text-gray-500 text-sm">No members found</td>
                </tr>
              )}
              {members.map(member => (
                <tr key={member.id} className="border-b border-gray-100 text-sm">
                  <td className="py-3 text-gray-800">{member.email || `User #${member.user_id}`}</td>
                  <td className="py-3 text-gray-600">{member.role_name}</td>
                  <td className="py-3 text-green-600">Active</td>
                  <td className="py-3"><button className="text-gray-400 hover:text-gray-600" onClick={() => setUserToEdit(member)}>Edit</button></td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Mobile List View */}
          <div className="md:hidden divide-y divide-gray-200 border-t border-gray-200">
            {members.length === 0 && (
              <div className="py-4 text-center text-gray-500 text-sm">No members found</div>
            )}
            {members.map(member => (
              <div key={member.id} className="py-3 space-y-1">
                <div className="flex justify-between items-start">
                  <span className="font-mono text-sm text-blue-800">{member.email || `User #${member.user_id}`}</span>
                  <span className="font-mono text-[10px] uppercase tracking-wider text-emerald-600 bg-emerald-50 px-1.5 py-0.5 rounded-sm">Active</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-500 font-semibold">{member.role_name}</span>
                  <button className="text-blue-600 font-semibold uppercase tracking-wider text-[10px]" onClick={() => setUserToEdit(member)}>Edit</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      <CredentialsManager />
    </div>
  );
};

// --- Client Portal View ---
const ClientPortalView = () => {
  const { activeWorkspace } = useWorkspace();

  const handleDownload = () => {
    window.location.href = '/api/v1/analytics/export';
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 p-6 rounded-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-10">
          <Activity className="w-32 h-32 text-blue-900" />
        </div>
        <div className="relative z-10">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
            <h2 className="text-xl font-bold text-blue-900">System Status: {activeWorkspace?.name}</h2>
          </div>
          <p className="text-blue-700 text-sm">Real-time metrics, active campaigns, and required approvals.</p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
        {/* Metric 1 */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="p-3 md:p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 className="text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider">Pending Approvals</h3>
            <span className="flex items-center justify-center w-5 h-5 md:w-6 md:h-6 rounded-sm md:rounded-md bg-amber-100 text-amber-600">
              <CheckCircle className="w-3 h-3 md:w-3.5 md:h-3.5" />
            </span>
          </div>
          <div className="p-3 md:p-5 flex-1 flex flex-col">
            <div className="flex items-end space-x-2 mb-3 md:mb-4">
              <span className="text-3xl md:text-4xl font-mono text-blue-900 tracking-tight">3</span>
              <span className="text-xs md:text-sm font-medium text-amber-500 mb-1">Action Required</span>
            </div>
            
            <div className="space-y-2 mb-4 md:mb-6">
              <div className="flex justify-between text-[10px] md:text-xs text-slate-500">
                <span>Social Posts</span>
                <span className="font-mono text-slate-700">2</span>
              </div>
              <div className="w-full bg-slate-100 rounded-sm md:rounded-full h-1 md:h-1.5">
                <div className="bg-slate-400 h-1 md:h-1.5 rounded-sm md:rounded-full" style={{ width: '66%' }}></div>
              </div>
              <div className="flex justify-between text-[10px] md:text-xs text-slate-500">
                <span>Blog Articles</span>
                <span className="font-mono text-slate-700">1</span>
              </div>
              <div className="w-full bg-slate-100 rounded-sm md:rounded-full h-1 md:h-1.5">
                <div className="bg-slate-400 h-1 md:h-1.5 rounded-sm md:rounded-full" style={{ width: '33%' }}></div>
              </div>
            </div>
            
            <button className="mt-auto w-full py-1.5 md:py-2 bg-blue-600 text-white rounded-sm md:rounded text-xs md:text-sm font-medium hover:bg-blue-700 transition-colors flex items-center justify-center uppercase tracking-wider md:tracking-normal md:normal-case">
              Review <ArrowRight className="w-3 h-3 md:w-3.5 md:h-3.5 ml-1.5" />
            </button>
          </div>
        </div>

        {/* Metric 2 */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="p-3 md:p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 className="text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Pipelines</h3>
            <span className="flex items-center justify-center w-5 h-5 md:w-6 md:h-6 rounded-sm md:rounded-md bg-emerald-100 text-emerald-600">
              <Activity className="w-3 h-3 md:w-3.5 md:h-3.5" />
            </span>
          </div>
          <div className="p-3 md:p-5 flex-1 flex flex-col">
            <div className="flex items-end space-x-2 mb-3 md:mb-4">
              <span className="text-3xl md:text-4xl font-mono text-blue-900 tracking-tight">2</span>
              <span className="text-xs md:text-sm font-medium text-emerald-500 mb-1">Healthy</span>
            </div>
            
            <div className="h-10 md:h-16 flex items-end space-x-1 mb-4 md:mb-6 mt-auto">
              {[40, 70, 45, 90, 65, 100, 80].map((val, i) => (
                <div key={i} className="flex-1 bg-slate-100 rounded-t-sm relative group cursor-crosshair">
                  <div 
                    className="absolute bottom-0 left-0 right-0 bg-emerald-400 rounded-t-sm transition-all duration-300 group-hover:bg-emerald-500"
                    style={{ height: `${val}%` }}
                  />
                </div>
              ))}
            </div>
            
            <button className="mt-auto w-full py-1.5 md:py-2 border border-gray-200 text-slate-700 rounded-sm md:rounded text-xs md:text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center uppercase tracking-wider md:tracking-normal md:normal-case">
              Monitor <ArrowRight className="w-3 h-3 md:w-3.5 md:h-3.5 ml-1.5" />
            </button>
          </div>
        </div>

        {/* Metric 3 */}
        <div className="col-span-2 md:col-span-1 bg-white rounded-xl border border-gray-200 overflow-hidden flex flex-col">
          <div className="p-3 md:p-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
            <h3 className="text-[10px] md:text-xs font-semibold text-slate-500 uppercase tracking-wider">Performance Reports</h3>
            <span className="flex items-center justify-center w-5 h-5 md:w-6 md:h-6 rounded-sm md:rounded-md bg-indigo-100 text-indigo-600">
              <BarChart2 className="w-3 h-3 md:w-3.5 md:h-3.5" />
            </span>
          </div>
          <div className="p-3 md:p-5 flex-1 flex flex-col">
            <div className="flex items-end space-x-2 mb-3 md:mb-4">
              <span className="text-3xl md:text-4xl font-mono text-blue-900 tracking-tight">Q2</span>
              <span className="text-xs md:text-sm font-medium text-indigo-500 mb-1">Generated</span>
            </div>
            
            <div className="bg-gray-50 rounded-sm p-2 md:p-3 border border-gray-100 mb-4 md:mb-6">
              <div className="flex justify-between items-center mb-1">
                <span className="font-mono text-[10px] md:text-xs font-medium text-slate-700">Q2 Summary.pdf</span>
                <span className="font-mono text-[10px] md:text-xs text-slate-400">2.4 MB</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="font-mono text-[10px] md:text-xs text-slate-500">Generated: Today, 09:41 AM</span>
              </div>
            </div>
            
            <button onClick={handleDownload} className="mt-auto w-full py-1.5 md:py-2 border border-gray-200 text-slate-700 rounded-sm md:rounded text-xs md:text-sm font-medium hover:bg-gray-50 transition-colors flex items-center justify-center uppercase tracking-wider md:tracking-normal md:normal-case">
              Download <ArrowRight className="w-3 h-3 md:w-3.5 md:h-3.5 ml-1.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default function AgencyPanel() {
  const { userRole, setUserRole, activeWorkspace } = useWorkspace();
  const [activeTab, setActiveTab] = useState('home');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const [notification, setNotification] = useState(null);
  
  useEffect(() => {
    const handleOpenCreate = () => setIsCreateModalOpen(true);
    document.addEventListener('open-create-workspace', handleOpenCreate);
    return () => document.removeEventListener('open-create-workspace', handleOpenCreate);
  }, []);

  const showNotification = (message) => {
    setNotification(message);
    setTimeout(() => setNotification(null), 3000);
  };

  const handleSendPrompt = async (overridePrompt) => {
    const promptToSend = typeof overridePrompt === 'string' ? overridePrompt : chatInput;
    if (!promptToSend.trim()) return;
    
    showNotification(`Processing your request: "${promptToSend}"...`);
    
    try {
      const response = await fetch('/api/v1/chat/scope', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: promptToSend }),
      });
      if (response.ok) {
        showNotification("Request sent successfully to orchestration engine.");
      } else {
        showNotification("Failed to send request. Engine might be offline.");
      }
    } catch (err) {
      showNotification("Error: Could not reach the engine.");
    }

    setChatInput('');
  };

  return (
    <div className="flex h-screen bg-white font-sans overflow-hidden relative">
      {/* Toast Notification Layer */}
      {notification && (
        <div className="absolute top-4 right-4 z-[100] bg-gray-800 text-white px-4 py-3 rounded shadow-lg flex items-center space-x-2 transition-all">
          <AlertCircle className="w-5 h-5 text-blue-400" />
          <span className="text-sm font-medium">{notification}</span>
        </div>
      )}

      {/* Mobile sidebar overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-gray-900 bg-opacity-50 md:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside id="main-sidebar" className={`fixed inset-y-0 left-0 z-50 ${isSidebarCollapsed ? 'w-20' : 'w-64'} bg-gray-50 border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <div className="p-6 border-b border-gray-100 flex justify-between items-center">
          <div className="flex items-center justify-between w-full">
            <div className={`flex items-center space-x-2 overflow-hidden transition-all duration-300 ${isSidebarCollapsed ? 'w-0 opacity-0' : 'w-auto opacity-100'}`}>
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">A</span>
              </div>
              <span className="text-xl font-bold text-gray-900 flex-shrink-0">AgencyOS</span>
            </div>
            <button 
              onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
              className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded hidden md:block focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-expanded={!isSidebarCollapsed}
              aria-controls="main-sidebar"
              aria-label={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              {isSidebarCollapsed ? <PanelLeft className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
            </button>
          </div>
          <button 
            className="md:hidden text-gray-500 hover:text-gray-700"
            onClick={() => setIsMobileMenuOpen(false)}
          >
            <X className="w-6 h-6" />
          </button>
        </div>
        
        <nav className="flex-1 p-3 overflow-y-auto flex flex-col">
          {/* Top Actions */}
          <div className="mb-4">
            {(userRole === 'Agency Admin' || userRole === 'Agency Staff') && (
            <button 
              onClick={() => { setActiveTab('home'); setIsMobileMenuOpen(false); }}
              className={`group relative flex items-center ${isSidebarCollapsed ? 'justify-center w-10 h-10 rounded-full mx-auto' : 'w-full px-3 py-2.5 rounded-lg'} bg-white border border-gray-200 shadow-sm hover:bg-gray-50 text-gray-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500`}
              aria-label="New Chat"
            >
              <Plus className="w-4 h-4 flex-shrink-0" aria-hidden="true" />
              {!isSidebarCollapsed && <span className="ml-2.5 font-medium text-sm">New Chat</span>}
              {isSidebarCollapsed && (
                <div className="absolute left-full ml-4 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none" aria-hidden="true">
                  New Chat
                </div>
              )}
            </button>
            )}
            {/* If Client, replace New Chat with a simpler "Dashboard" home button */}
            {(userRole === 'Client Approver' || userRole === 'Client Viewer') && (
            <button 
              onClick={() => { setActiveTab('home'); setIsMobileMenuOpen(false); }}
              className={`group relative flex items-center ${isSidebarCollapsed ? 'justify-center w-10 h-10 rounded-full mx-auto' : 'w-full px-3 py-2.5 rounded-lg'} bg-blue-50 text-blue-700 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500`}
              aria-label="Dashboard"
            >
              <Activity className="w-4 h-4 flex-shrink-0" aria-hidden="true" />
              {!isSidebarCollapsed && <span className="ml-2.5 font-medium text-sm">Dashboard</span>}
              {isSidebarCollapsed && (
                <div className="absolute left-full ml-4 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none" aria-hidden="true">
                  Dashboard
                </div>
              )}
            </button>
            )}
          </div>

          {/* Recent Section */}
          {!isSidebarCollapsed && (
            <div className="mb-4">
              <p className="px-3 text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1.5">Recent</p>
              <SidebarItem icon={MessageSquare} label="Marketing Campaign Plan" active={activeTab === 'scope'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }} />
              <SidebarItem icon={MessageSquare} label="Q3 Strategy Review" active={false} collapsed={isSidebarCollapsed} onClick={() => {}} />
              <SidebarItem icon={MessageSquare} label="Website Redesign Copy" active={false} collapsed={isSidebarCollapsed} onClick={() => {}} />
            </div>
          )}

          {/* Workspace Tools Section */}
          <div className="mb-4 flex-1">
            {!isSidebarCollapsed && <p className="px-3 text-[11px] font-semibold text-gray-400 uppercase tracking-wider mb-1.5">Workspace Tools</p>}
            <SidebarItem icon={MessageSquare} label="Project Scope" active={activeTab === 'scope'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }} />
            {(userRole === 'Agency Admin' || userRole === 'Agency Staff') && (
              <SidebarItem icon={Bot} label="Agents" active={activeTab === 'agents'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('agents'); setIsMobileMenuOpen(false); }} />
            )}
            {userRole === 'Agency Admin' && (
              <>
                <SidebarItem icon={BarChart2} label="Analytics" active={activeTab === 'analytics'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('analytics'); setIsMobileMenuOpen(false); }} />
                <SidebarItem icon={Store} label="Marketplace" active={activeTab === 'marketplace'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('marketplace'); setIsMobileMenuOpen(false); }} />
              </>
            )}
            <SidebarItem icon={FileText} label="Files" active={activeTab === 'files'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('files'); setIsMobileMenuOpen(false); }} />
          </div>

          {/* Bottom Admin/Utility Section */}
          <div className="mt-auto pt-2 border-t border-gray-200">
            {userRole === 'Agency Admin' && (
              <>
                <SidebarItem icon={Users} label="Access Control" active={activeTab === 'rbac'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('rbac'); setIsMobileMenuOpen(false); }} />
                <SidebarItem icon={Database} label="Audit Logs" active={activeTab === 'audit'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('audit'); setIsMobileMenuOpen(false); }} />
              </>
            )}
            <SidebarItem icon={Cpu} label="Workflows" active={activeTab === 'workflows'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('workflows'); setIsMobileMenuOpen(false); }} />
          </div>
        </nav>

        {/* Persistent Utilities (Pinned Bottom) */}
        <div className="p-3 border-t border-gray-200 bg-white relative">
          <div className={`flex items-center ${isSidebarCollapsed ? 'justify-center flex-col space-y-4' : 'justify-between'}`}>
            
            <div className={`flex items-center ${isSidebarCollapsed ? 'justify-center' : 'flex-1 min-w-0'}`}>
              <div className="relative group">
                <button 
                  onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                  className={`w-8 h-8 flex-shrink-0 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold border border-blue-200 hover:ring-2 ring-blue-500 focus:outline-none transition-all ${isProfileMenuOpen ? 'ring-2 ring-blue-500 bg-blue-200' : ''}`}
                  aria-haspopup="true"
                  aria-expanded={isProfileMenuOpen}
                >
                  {userRole.charAt(0)}
                </button>
                
                {isSidebarCollapsed && !isProfileMenuOpen && (
                  <div className="absolute left-full top-1/2 -translate-y-1/2 ml-4 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none" aria-hidden="true">
                    Profile & Roles
                  </div>
                )}

                {isProfileMenuOpen && (
                  <div className={`absolute bottom-full mb-2 ${isSidebarCollapsed ? 'left-full ml-4' : 'left-0'} w-56 bg-white border border-gray-200 shadow-lg rounded-xl z-50 overflow-hidden`}>
                    <div className="p-4 border-b border-gray-100 bg-gray-50">
                      <p className="font-semibold text-sm text-gray-800 truncate">{userRole}</p>
                      <p className="text-xs text-gray-500 truncate">demo@agencyos.com</p>
                    </div>
                    
                    <div className="p-2">
                      <p className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wider">Simulate Role</p>
                      <div className="space-y-1 mt-1">
                        {['Agency Admin', 'Agency Staff', 'Client Approver', 'Client Viewer'].map(role => (
                          <button
                            key={role}
                            onClick={() => {
                              setUserRole(role);
                              setActiveTab('home');
                              setIsProfileMenuOpen(false);
                            }}
                            className={`w-full text-left px-2 py-1.5 text-sm rounded-md transition-colors ${userRole === role ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-100'}`}
                          >
                            {role}
                          </button>
                        ))}
                      </div>
                    </div>
                    
                    <div className="p-2 border-t border-gray-100">
                      <button 
                        onClick={() => {
                          setActiveTab('settings');
                          setIsProfileMenuOpen(false);
                        }}
                        className="w-full text-left px-2 py-1.5 text-sm text-gray-700 hover:bg-gray-100 rounded-md"
                      >
                        Account Settings
                      </button>
                      <button 
                        onClick={() => {
                          showNotification("Logout not implemented.");
                          setIsProfileMenuOpen(false);
                        }}
                        className="w-full text-left px-2 py-1.5 text-sm text-red-600 hover:bg-red-50 rounded-md"
                      >
                        Logout
                      </button>
                    </div>
                  </div>
                )}
              </div>
              
              {!isSidebarCollapsed && (
                <div className="ml-3 truncate cursor-pointer" onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}>
                  <p className="text-sm font-medium text-gray-700 truncate">{userRole}</p>
                </div>
              )}
            </div>
            
            <div className="relative group flex">
              <button 
                onClick={() => { setActiveTab('settings'); setIsMobileMenuOpen(false); }}
                className={`p-2 flex-shrink-0 text-gray-500 hover:text-gray-800 hover:bg-gray-200 rounded-lg transition-colors focus:outline-none ${activeTab === 'settings' ? 'bg-gray-200 text-gray-800' : ''}`}
                aria-label="Settings"
              >
                <Settings className="w-5 h-5" />
              </button>
              
              {isSidebarCollapsed && (
                <div className="absolute left-full top-1/2 -translate-y-1/2 ml-4 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50 pointer-events-none" aria-hidden="true">
                  Settings
                </div>
              )}
            </div>

          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <header className="bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-900 border-b border-gray-200 h-16 flex items-center justify-between px-4 sm:px-8">
          <div className="flex items-center">
            <button 
              className="md:hidden mr-3 text-gray-500 hover:text-gray-700"
              onClick={() => setIsMobileMenuOpen(true)}
            >
              <Menu className="w-6 h-6" />
            </button>
            <h1 className="text-lg sm:text-xl font-semibold text-gray-800 capitalize truncate">
              {activeTab === 'home' ? (userRole === 'Agency Admin' ? 'Agency Overview' : 'Client Dashboard') : activeTab}
            </h1>
          </div>
          <div className="flex items-center space-x-2 sm:space-x-4 ml-2">
            <span className="text-xs sm:text-sm text-gray-500 hidden sm:inline">Logged in as <strong className="text-gray-700">{userRole}</strong></span>
            <div className="w-8 h-8 bg-gray-200 rounded-full border border-gray-300 flex-shrink-0"></div>
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-4 sm:p-8 flex flex-col">
          <div className="max-w-5xl mx-auto w-full flex-1 mb-20 flex flex-col">
            {activeTab === 'home' && (
              (userRole === 'Agency Admin' || userRole === 'Agency Staff') ? (
                <IntroPage onPromptSubmit={(prompt) => {
                  setChatInput(prompt);
                  handleSendPrompt(prompt);
                  setActiveTab('scope');
                }} />
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
              <WorkspaceManagementUI showNotification={showNotification} />
            )}
            {activeTab === 'settings' && userRole !== 'Agency Admin' && (
              <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center py-12">
                <Settings className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-700 mb-1">User Settings</h3>
                <p className="text-gray-500">Personal account preferences and notifications will be managed here.</p>
              </div>
            )}
            {activeTab === 'agents' && (userRole === 'Agency Admin' || userRole === 'Agency Staff') && (
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
          {!(activeTab === 'home' && (userRole === 'Agency Admin' || userRole === 'Agency Staff')) && 
           userRole !== 'Client Viewer' && (
          <div className={`max-w-3xl mx-auto w-full mt-auto fixed bottom-0 md:bottom-6 left-0 right-0 ${isSidebarCollapsed ? 'md:pl-20' : 'md:pl-64'} md:px-4 pointer-events-none`}>
            <div className="bg-white/80 md:bg-white backdrop-blur-md md:backdrop-blur-none rounded-none md:rounded-full shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)] md:shadow-lg border-t md:border border-gray-200 p-2 md:p-2 flex items-center pointer-events-auto">
              <Search className="w-5 h-5 text-gray-400 ml-3 mr-2 hidden md:block" />
              <input
                type="text"
                aria-label="Universal search and command input"
                placeholder="Search, run commands, or ask questions..."
                className="flex-1 bg-transparent border-none focus:ring-0 text-sm py-2 md:py-2 px-3 md:px-1 outline-none text-gray-800 placeholder-gray-500"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleSendPrompt();
                  }
                }}
              />
              <button 
                className="bg-transparent md:bg-blue-600 text-blue-600 md:text-white p-2 md:p-2 rounded-sm md:rounded-full hover:bg-gray-100 md:hover:bg-blue-700 transition-colors ml-1 md:ml-2"
                onClick={handleSendPrompt}
              >
                <Send className="w-5 h-5 md:w-4 md:h-4" />
              </button>
            </div>
          </div>
          )}
        </div>
      </main>

      <CreateWorkspaceModal 
        isOpen={isCreateModalOpen} 
        onClose={() => setIsCreateModalOpen(false)} 
      />
    </div>
  );
}
