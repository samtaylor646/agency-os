import React, { useState, useEffect } from 'react';
import { useWorkspace } from './WorkspaceContext';
import { ContextSwitcher } from './ContextSwitcher';
import { Users, Settings, Activity, FileText, Share2, Plus, ArrowRight } from 'lucide-react';

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
            <button className="text-blue-600 text-sm font-medium hover:underline">Manage Keys</button>
          </div>
          <div className="p-4 border border-gray-200 rounded-lg">
            <h3 className="font-semibold text-gray-800 mb-2">Billing Context</h3>
            <p className="text-sm text-gray-500 mb-4">View usage limits for {activeWorkspace?.name}.</p>
            <button className="text-blue-600 text-sm font-medium hover:underline">View Usage</button>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-gray-800">Users & Invites</h2>
          <button className="flex items-center space-x-1 bg-blue-600 text-white px-3 py-1.5 rounded-md text-sm hover:bg-blue-700 transition-colors">
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
  
  // Listen for the custom event to simulate creating a workspace
  useEffect(() => {
    const handleOpenCreate = () => alert('Create Workspace Modal would open here.');
    document.addEventListener('open-create-workspace', handleOpenCreate);
    return () => document.removeEventListener('open-create-workspace', handleOpenCreate);
  }, []);

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">AgencyOS</span>
          </div>
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
              onClick={() => setActiveTab('dashboard')} 
            />
            {userRole === 'Agency Admin' && (
              <SidebarItem 
                icon={Settings} 
                label="Workspace Settings" 
                active={activeTab === 'settings'} 
                onClick={() => setActiveTab('settings')} 
              />
            )}
            <SidebarItem 
              icon={FileText} 
              label="Files & Assets" 
              active={activeTab === 'files'} 
              onClick={() => setActiveTab('files')} 
            />
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
      <main className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-8">
          <h1 className="text-xl font-semibold text-gray-800 capitalize">
            {activeTab === 'dashboard' ? (userRole === 'Agency Admin' ? 'Agency Overview' : 'Client Dashboard') : activeTab}
          </h1>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-500">Logged in as <strong className="text-gray-700">{userRole}</strong></span>
            <div className="w-8 h-8 bg-gray-200 rounded-full border border-gray-300"></div>
          </div>
        </header>
        
        <div className="flex-1 overflow-auto p-8">
          <div className="max-w-5xl mx-auto">
            {activeTab === 'dashboard' && (
              userRole === 'Agency Admin' ? (
                <div>
                  <h2 className="text-2xl font-bold text-gray-800 mb-6">Agency Overview: {activeWorkspace?.name}</h2>
                  <p className="text-gray-600">Select "Workspace Settings" to manage this tenant, or switch workspaces using the dropdown in the sidebar.</p>
                </div>
              ) : (
                <ClientPortalView />
              )
            )}
            {activeTab === 'settings' && userRole === 'Agency Admin' && (
              <WorkspaceManagementUI />
            )}
            {activeTab === 'files' && (
              <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm text-center py-12">
                <Share2 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-700 mb-1">File Manager</h3>
                <p className="text-gray-500">Tenant-isolated file storage would be implemented here.</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
