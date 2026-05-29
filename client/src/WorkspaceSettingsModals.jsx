import React, { useState, useEffect } from 'react';
import { X, Plus, Trash2, Key, Save, Server } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export const GlobalApiSettingsModal = ({ isOpen, onClose, showNotification }) => {
  const { activeWorkspace, apiFetch } = useWorkspace();
  const [provider, setProvider] = useState('openai');
  const [apiKey, setApiKey] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSave = async () => {
    try {
      setLoading(true);
      const res = await apiFetch('/api/v1/credentials', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          provider: provider,
          api_key: apiKey 
        })
      });
      if (res.ok) {
        showNotification('API Settings saved successfully.');
        setApiKey(''); // clear on save for security
        onClose();
      } else {
        showNotification('Failed to save API Settings.');
      }
    } catch (e) {
      showNotification('Error saving API Settings.');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900 bg-opacity-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-800 flex items-center">
            <Server className="w-5 h-5 mr-2 text-blue-600" />
            Global API Settings
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>
        <div className="p-6">
          <p className="text-sm text-gray-500 mb-6">Configure the default API provider for this workspace.</p>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
            <select 
              className="w-full border border-gray-300 rounded-md p-2"
              value={provider} 
              onChange={(e) => setProvider(e.target.value)}
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="gemini">Google Gemini</option>
              <option value="local">Local Model (e.g. Ollama)</option>
            </select>
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
            <input 
              type="password" 
              placeholder="Enter API Key"
              className="w-full border border-gray-300 rounded-md p-2"
              value={apiKey} 
              onChange={(e) => setApiKey(e.target.value)}
            />
          </div>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancel</button>
            <button 
              onClick={handleSave} 
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 flex items-center disabled:opacity-50"
            >
              <Save className="w-4 h-4 mr-1" /> {loading ? 'Saving...' : 'Save Settings'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ApiKeysModal = ({ isOpen, onClose, showNotification }) => {
  const { activeWorkspace } = useWorkspace();
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(false);
  const [newKeyName, setNewKeyName] = useState('');
  const [newKey, setNewKey] = useState(null);

  const fetchKeys = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/api_keys', {
        headers: { 'X-Tenant-ID': activeWorkspace?.id?.toString() || '' }
      });
      if (res.ok) setKeys(await res.json());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchKeys();
      setNewKey(null);
      setNewKeyName('');
    }
  }, [isOpen, activeWorkspace]);

  const handleCreate = async () => {
    if (!newKeyName.trim()) return;
    try {
      const res = await fetch('/api/v1/api_keys', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Tenant-ID': activeWorkspace?.id?.toString() || ''
        },
        body: JSON.stringify({ name: newKeyName })
      });
      if (res.ok) {
        const data = await res.json();
        setNewKey(data.key); // show the unmasked key once
        setNewKeyName('');
        fetchKeys();
        showNotification('API Key generated successfully.');
      } else {
        showNotification('Failed to generate API Key.');
      }
    } catch (err) {
      showNotification('Error creating API Key.');
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Revoke this key?')) return;
    try {
      const res = await fetch(`/api/v1/api_keys/${id}`, {
        method: 'DELETE',
        headers: { 'X-Tenant-ID': activeWorkspace?.id?.toString() || '' }
      });
      if (res.ok) {
        fetchKeys();
        showNotification('API Key revoked.');
      }
    } catch (err) {
      showNotification('Error revoking API Key.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900 bg-opacity-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-800">Manage API Keys</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>
        <div className="p-6 overflow-y-auto">
          {newKey && (
            <div className="mb-6 p-4 bg-green-50 text-green-800 rounded-lg border border-green-200">
              <p className="font-semibold mb-2">Save this key now! It won't be shown again.</p>
              <div className="font-mono bg-white p-2 border border-green-200 rounded break-all">{newKey}</div>
            </div>
          )}

          <div className="flex gap-2 mb-6">
            <input 
              type="text" 
              placeholder="New Key Name (e.g. Production App)"
              className="flex-1 border border-gray-300 rounded-md p-2 text-sm"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
            />
            <button 
              onClick={handleCreate}
              className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 flex items-center"
            >
              <Plus className="w-4 h-4 mr-1" /> Generate
            </button>
          </div>

          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b border-gray-200 text-gray-500">
                <th className="py-2 font-medium">Name</th>
                <th className="py-2 font-medium">Prefix</th>
                <th className="py-2 font-medium">Created</th>
                <th className="py-2 font-medium">Action</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr><td colSpan="4" className="py-4 text-center text-gray-500">Loading...</td></tr>
              ) : keys.length === 0 ? (
                <tr><td colSpan="4" className="py-4 text-center text-gray-500">No API keys found.</td></tr>
              ) : (
                keys.map(k => (
                  <tr key={k.id} className="border-b border-gray-100">
                    <td className="py-3 font-medium text-gray-800">{k.name}</td>
                    <td className="py-3 font-mono text-xs text-gray-600">{k.key_prefix}...</td>
                    <td className="py-3 text-gray-500">{new Date(k.created_at).toLocaleDateString()}</td>
                    <td className="py-3">
                      <button onClick={() => handleDelete(k.id)} className="text-red-500 hover:text-red-700">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export const InviteUserModal = ({ isOpen, onClose, showNotification, onInviteSuccess }) => {
  const { activeWorkspace } = useWorkspace();
  const [email, setEmail] = useState('');
  const [roleId, setRoleId] = useState('');
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    if (isOpen) {
      setEmail('');
      setRoleId('');
      fetch('/api/v1/rbac/roles')
        .then(res => res.json())
        .then(data => {
          setRoles(data);
          if (data.length > 0) setRoleId(data[0].id.toString());
        });
    }
  }, [isOpen]);

  const handleInvite = async (e) => {
    e.preventDefault();
    if (!email.trim() || !roleId) return;
    try {
      const res = await fetch(`/api/v1/rbac/workspaces/${activeWorkspace?.id || 1}/invite`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, role_id: parseInt(roleId) })
      });
      if (res.ok) {
        showNotification('User invited successfully.');
        onInviteSuccess();
        onClose();
      } else {
        const err = await res.json();
        showNotification(err.detail || 'Failed to invite user.');
      }
    } catch (err) {
      showNotification('Error inviting user.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900 bg-opacity-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-800">Invite User</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>
        <form onSubmit={handleInvite} className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">Email Address</label>
            <input 
              type="email" required
              className="w-full border border-gray-300 rounded-md p-2"
              value={email} onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
            <select 
              className="w-full border border-gray-300 rounded-md p-2"
              value={roleId} onChange={(e) => setRoleId(e.target.value)}
            >
              {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
          </div>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancel</button>
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">Send Invite</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export const EditUserModal = ({ isOpen, onClose, user, showNotification, onUpdateSuccess }) => {
  const [roleId, setRoleId] = useState('');
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    if (isOpen && user) {
      fetch('/api/v1/rbac/roles')
        .then(res => res.json())
        .then(data => {
          setRoles(data);
          const currentRole = data.find(r => r.name === user.role_name);
          if (currentRole) setRoleId(currentRole.id.toString());
          else if (data.length > 0) setRoleId(data[0].id.toString());
        });
    }
  }, [isOpen, user]);

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (!user || !roleId) return;
    try {
      const res = await fetch(`/api/v1/rbac/members/${user.id}/role`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ role_id: parseInt(roleId) })
      });
      if (res.ok) {
        showNotification('User role updated successfully.');
        onUpdateSuccess();
        onClose();
      } else {
        const err = await res.json();
        showNotification(err.detail || 'Failed to update user.');
      }
    } catch (err) {
      showNotification('Error updating user.');
    }
  };

  if (!isOpen || !user) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900 bg-opacity-50">
      <div className="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-6 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-800">Edit User Role</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <X className="w-6 h-6" />
          </button>
        </div>
        <form onSubmit={handleUpdate} className="p-6">
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">User</label>
            <div className="text-gray-800 font-medium bg-gray-50 p-2 rounded border border-gray-200">{user.email || `User #${user.user_id}`}</div>
          </div>
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-1">New Role</label>
            <select 
              className="w-full border border-gray-300 rounded-md p-2"
              value={roleId} onChange={(e) => setRoleId(e.target.value)}
            >
              {roles.map(r => <option key={r.id} value={r.id}>{r.name}</option>)}
            </select>
          </div>
          <div className="flex justify-end space-x-3">
            <button type="button" onClick={onClose} className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800">Cancel</button>
            <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  );
};
