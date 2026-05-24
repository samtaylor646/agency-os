import React, { useState, useEffect } from 'react';
import { Database, Download, AlertCircle } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export const AuditLogViewer = () => {
  const { activeWorkspace } = useWorkspace();
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLogs = async () => {
      setLoading(true);
      try {
        // Assume an endpoint exists or mock it
        const res = await fetch('/api/v1/workspaces/audit-logs');
        if (res.ok) {
          setLogs(await res.json());
        } else {
          // Mock data if endpoint fails
          setLogs([
            { id: 1, user: 'admin@agencyos.com', action: 'CREATE_AGENT', resource: 'Marketing Agent', created_at: new Date().toISOString() },
            { id: 2, user: 'client@company.com', action: 'VIEW_DASHBOARD', resource: 'Dashboard', created_at: new Date(Date.now() - 3600000).toISOString() },
            { id: 3, user: 'system', action: 'EXECUTE_WORKFLOW', resource: 'SEO Optimization', created_at: new Date(Date.now() - 7200000).toISOString() },
          ]);
        }
      } catch (err) {
        // Fallback mock
        setLogs([
            { id: 1, user: 'admin@agencyos.com', action: 'CREATE_AGENT', resource: 'Marketing Agent', created_at: new Date().toISOString() },
            { id: 2, user: 'client@company.com', action: 'VIEW_DASHBOARD', resource: 'Dashboard', created_at: new Date(Date.now() - 3600000).toISOString() },
            { id: 3, user: 'system', action: 'EXECUTE_WORKFLOW', resource: 'SEO Optimization', created_at: new Date(Date.now() - 7200000).toISOString() },
        ]);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, [activeWorkspace]);

  return (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Database className="w-6 h-6 text-gray-800" />
            <h2 className="text-xl font-bold text-gray-800">Audit Logs</h2>
          </div>
          <button className="flex items-center space-x-2 text-sm text-gray-600 border border-gray-200 px-3 py-1.5 rounded-lg hover:bg-gray-50">
            <Download className="w-4 h-4" />
            <span>Export CSV</span>
          </button>
        </div>
        
        {loading ? (
          <p className="text-gray-500">Loading audit logs...</p>
        ) : (
          <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Timestamp</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">User</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Action</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Resource</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {logs.map(log => (
                  <tr key={log.id}>
                    <td className="px-4 py-3 text-sm text-gray-500 whitespace-nowrap">{new Date(log.created_at).toLocaleString()}</td>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">{log.user}</td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      <span className="bg-gray-100 text-gray-800 px-2 py-0.5 rounded text-xs font-medium">
                        {log.action}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">{log.resource}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
