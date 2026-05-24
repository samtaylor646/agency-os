import React, { useState, useEffect } from 'react';
import { Shield, ShieldAlert, Check } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export const RBACManager = () => {
  const { activeWorkspace } = useWorkspace();
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRBAC = async () => {
      setLoading(true);
      try {
        const [rolesRes, permsRes] = await Promise.all([
          fetch('/api/rbac/roles'),
          fetch('/api/rbac/permissions')
        ]);
        
        if (rolesRes.ok) setRoles(await rolesRes.json());
        if (permsRes.ok) setPermissions(await permsRes.json());
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchRBAC();
  }, [activeWorkspace]);

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
          <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors flex items-center space-x-2">
            <Check className="w-4 h-4" />
            <span>Create Role</span>
          </button>
        </div>
        
        {error && (
          <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5" />
            <span>{error}</span>
          </div>
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
