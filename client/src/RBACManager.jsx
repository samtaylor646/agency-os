import React, { useState, useEffect } from 'react';
import { Shield, ShieldAlert, Check } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export const RBACManager = () => {
  const { activeWorkspace } = useWorkspace();
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [isAdding, setIsAdding] = useState(false);
  const [newRole, setNewRole] = useState({ name: '', description: '' });
  const [success, setSuccess] = useState(null);

  const fetchRBAC = async () => {
    setLoading(true);
    try {
      const [rolesRes, permsRes] = await Promise.all([
        fetch('/api/v1/rbac/roles'),
        fetch('/api/v1/rbac/permissions')
      ]);
      
      if (rolesRes.ok) setRoles(await rolesRes.json());
      if (permsRes.ok) setPermissions(await permsRes.json());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRBAC();
  }, [activeWorkspace]);

  const handleCreateRole = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    if (!newRole.name.trim()) {
      setError("Role name is required");
      return;
    }
    try {
      const res = await fetch('/api/v1/rbac/roles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newRole)
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => null);
        throw new Error(errData?.detail || "Failed to create role");
      }
      setSuccess("Role created successfully");
      setIsAdding(false);
      setNewRole({ name: '', description: '' });
      fetchRBAC();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <Shield className="w-6 h-6 text-indigo-600" />
              <h2 className="text-xl font-bold text-gray-800">Role-Based Access Control</h2>
            </div>
            <p className="text-gray-600">Manage custom roles and granular permissions for your workspace.</p>
          </div>
          <button 
            onClick={() => setIsAdding(!isAdding)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center space-x-2"
          >
            <Check className="w-4 h-4" />
            <span>{isAdding ? 'Cancel' : 'Create Role'}</span>
          </button>
        </div>
        
        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="mb-4 p-4 bg-green-50 text-green-700 rounded-lg flex items-center space-x-2">
            <Check className="w-5 h-5" />
            <span>{success}</span>
          </div>
        )}

        {isAdding && (
          <form onSubmit={handleCreateRole} className="mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Role Name</label>
                <input 
                  type="text" 
                  value={newRole.name}
                  onChange={(e) => setNewRole({...newRole, name: e.target.value})}
                  placeholder="e.g. Content Editor"
                  className="w-full border border-gray-300 rounded p-2 text-sm"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <input 
                  type="text" 
                  value={newRole.description}
                  onChange={(e) => setNewRole({...newRole, description: e.target.value})}
                  placeholder="Brief description"
                  className="w-full border border-gray-300 rounded p-2 text-sm"
                />
              </div>
            </div>
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700">
              Save Role
            </button>
          </form>
        )}

        {loading ? (
          <p className="text-gray-500">Loading roles and permissions...</p>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-800">Available Roles</h3>
              <div className="space-y-3">
                {roles.length === 0 ? <p className="text-sm text-gray-500">No roles found.</p> : null}
                {roles.map(role => (
                  <div key={role.id} className="p-4 border border-gray-200 rounded-lg bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900">{role.name}</h4>
                        <p className="text-sm text-gray-500 mt-1">{role.description || 'No description provided.'}</p>
                      </div>
                      <span className="px-2 py-1 bg-indigo-100 text-indigo-800 text-xs rounded-full font-medium">
                        {role.workspace_id ? 'Custom' : 'System'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 text-gray-800">System Permissions</h3>
              <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Permission</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {permissions.length === 0 ? (
                      <tr><td colSpan="2" className="px-4 py-3 text-sm text-gray-500 text-center">No permissions found.</td></tr>
                    ) : null}
                    {permissions.map(perm => (
                      <tr key={perm.id}>
                        <td className="px-4 py-3 text-sm font-medium text-gray-900">{perm.name}</td>
                        <td className="px-4 py-3 text-sm text-gray-500">{perm.description}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
