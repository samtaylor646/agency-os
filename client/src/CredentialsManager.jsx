import React, { useState, useEffect } from 'react';
import { useWorkspace } from './WorkspaceContext';
import { Plus, Trash2, Key, AlertCircle, CheckCircle, Minus } from 'lucide-react';

export const CredentialsManager = () => {
  const { activeWorkspace } = useWorkspace();
  const [credentials, setCredentials] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [newCred, setNewCred] = useState({ provider: 'openai', key: '' });
  const [token, setToken] = useState('');

  const fetchToken = async () => {
    try {
      const res = await fetch('/api/v1/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: 'admin@agencyos.com',
          password: 'password123'
        })
      });
      if (res.ok) {
        const data = await res.json();
        setToken(data.access_token);
        return data.access_token;
      }
    } catch (err) {
      console.error("Failed to fetch token", err);
    }
    return '';
  };

  const loadCredentials = async (currentToken) => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/credentials/', {
        headers: {
          'Authorization': `Bearer ${currentToken}`,
          'X-Tenant-ID': activeWorkspace?.id?.toString() || ''
        }
      });
      if (res.ok) {
        const data = await res.json();
        setCredentials(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (activeWorkspace) {
      fetchToken().then(t => {
        if (t) loadCredentials(t);
      });
    }
  }, [activeWorkspace]);

  const handleAdd = async (e) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    
    if (!newCred.key.trim()) {
      setError("Key is required");
      return;
    }
    
    try {
      const res = await fetch('/api/v1/credentials/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'X-Tenant-ID': activeWorkspace?.id?.toString() || ''
        },
        body: JSON.stringify(newCred)
      });
      
      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to add credential");
      }
      
      setSuccess("Credential added successfully");
      setIsAdding(false);
      setNewCred({ provider: 'openai', key: '' });
      loadCredentials(token);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Are you sure you want to delete this credential?")) return;
    
    setError(null);
    setSuccess(null);
    
    try {
      const res = await fetch(`/api/v1/credentials/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'X-Tenant-ID': activeWorkspace?.id?.toString() || ''
        }
      });
      
      if (!res.ok) {
        throw new Error("Failed to delete credential");
      }
      
      setSuccess("Credential deleted successfully");
      loadCredentials(token);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm mt-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-800">LLM Credentials Vault</h2>
          <p className="text-gray-600 text-sm mt-1">Securely manage API keys for LLM providers (encrypted at rest).</p>
        </div>
        <button 
          onClick={() => setIsAdding(!isAdding)}
          className="flex items-center justify-center space-x-1 bg-gray-100 text-gray-700 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-200 transition-colors w-full sm:w-auto shrink-0"
        >
          {isAdding ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
          <span>{isAdding ? 'Cancel' : 'Add Credential'}</span>
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-700 flex items-center text-sm">
          <AlertCircle className="w-4 h-4 mr-2" /> {error}
        </div>
      )}
      
      {success && (
        <div className="mb-4 p-3 rounded-lg bg-green-50 text-green-700 flex items-center text-sm">
          <CheckCircle className="w-4 h-4 mr-2" /> {success}
        </div>
      )}

      {isAdding && (
        <form onSubmit={handleAdd} className="mb-6 p-4 border border-gray-200 rounded-lg bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Provider</label>
              <select 
                value={newCred.provider} 
                onChange={(e) => setNewCred({...newCred, provider: e.target.value})}
                className="w-full border border-gray-300 rounded-md p-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow appearance-none"
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="google">Google (Gemini)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
              <input 
                type="password" 
                value={newCred.key}
                onChange={(e) => setNewCred({...newCred, key: e.target.value})}
                placeholder="sk-..."
                className="w-full border border-gray-300 rounded-md p-2.5 text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
              />
            </div>
          </div>
          <button type="submit" className="w-full md:w-auto bg-blue-600 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1">
            Save Credential
          </button>
        </form>
      )}

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-200 text-gray-500 text-sm">
              <th className="py-3 font-medium">Provider</th>
              <th className="py-3 font-medium">Masked Key</th>
              <th className="py-3 font-medium">Added</th>
              <th className="py-3 font-medium">Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="4" className="py-4 text-center text-gray-500 text-sm">Loading credentials...</td>
              </tr>
            ) : credentials.length === 0 ? (
              <tr>
                <td colSpan="4" className="py-4 text-center text-gray-500 text-sm">No credentials found for this workspace.</td>
              </tr>
            ) : (
              credentials.map(c => (
                <tr key={c.id} className="border-b border-gray-100 text-sm">
                  <td className="py-3 text-gray-800 capitalize flex items-center">
                    <Key className="w-4 h-4 mr-2 text-gray-400" />
                    {c.provider}
                  </td>
                  <td className="py-3 text-gray-600 font-mono text-xs">{c.masked_key}</td>
                  <td className="py-3 text-gray-500">{new Date(c.created_at).toLocaleDateString()}</td>
                  <td className="py-3">
                    <button 
                      onClick={() => handleDelete(c.id)}
                      className="text-red-500 hover:text-red-700"
                      title="Delete"
                    >
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
  );
};
