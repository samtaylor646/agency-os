import React, { createContext, useContext, useState, useEffect } from 'react';

const WorkspaceContext = createContext(null);

export const WorkspaceProvider = ({ children }) => {
  const [workspaces, setWorkspaces] = useState([]);
  const [activeWorkspaceId, setActiveWorkspaceId] = useState(null);
  const [userRole, setUserRole] = useState('Agency Admin'); // Mocked user role for now

  // Intercept fetch calls to append tenant ID
  const apiFetch = async (url, options = {}) => {
    let token = localStorage.getItem('agency_os_token');
    
    // Auto-login for MVP if no token is found
    if (!token) {
      try {
        const tokenRes = await fetch('/api/v1/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            username: 'admin@agencyos.com',
            password: 'password123'
          })
        });
        if (tokenRes.ok) {
          const data = await tokenRes.json();
          token = data.access_token;
          localStorage.setItem('agency_os_token', token);
        }
      } catch (e) {
        console.error('Failed to auto-fetch token', e);
      }
    }

    const headers = {
      ...options.headers,
      ...(options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' }),
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };

    // Only add X-Tenant-ID if activeWorkspaceId is present, or if it's already set in options
    if (activeWorkspaceId && !headers['X-Tenant-ID']) {
      headers['X-Tenant-ID'] = activeWorkspaceId;
    }
    
    const res = await fetch(url, { ...options, headers });
    
    // Handle token expiry
    if (res.status === 401) {
      localStorage.removeItem('agency_os_token');
    }
    
    return res;
  };

  // Fetch workspaces on mount
  useEffect(() => {
    const fetchWorkspaces = async () => {
      try {
        // Fetch API workspaces
        const res = await apiFetch('/api/v1/workspaces');
        let fetchedWorkspaces = [];
        if (res.ok) {
          fetchedWorkspaces = await res.json();
          // Map backend IDs to strings to match frontend usage, or just keep as is if backend returns string IDs.
          // Backend returns integer IDs based on models.
          fetchedWorkspaces = fetchedWorkspaces.map(w => ({ ...w, id: String(w.id) }));
        }

        if (fetchedWorkspaces.length === 0) {
           fetchedWorkspaces = [
             { id: '1', name: 'Default Workspace (Fallback)' }
           ];
        }

        setWorkspaces(fetchedWorkspaces);
        
        // Retrieve last active from localStorage or default to first
        const saved = localStorage.getItem('activeWorkspaceId');
        if (saved && fetchedWorkspaces.find(w => w.id === saved)) {
          setActiveWorkspaceId(saved);
        } else if (fetchedWorkspaces.length > 0) {
          setActiveWorkspaceId(fetchedWorkspaces[0].id);
        }
      } catch (err) {
        console.error('Failed to fetch workspaces', err);
      }
    };
    
    fetchWorkspaces();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (activeWorkspaceId) {
      localStorage.setItem('activeWorkspaceId', activeWorkspaceId);
    }
  }, [activeWorkspaceId]);

  const activeWorkspace = workspaces.find(w => w.id === activeWorkspaceId);

  return (
    <WorkspaceContext.Provider value={{ 
      workspaces, 
      activeWorkspaceId, 
      setActiveWorkspaceId,
      activeWorkspace,
      userRole,
      setUserRole,
      apiFetch,
      setWorkspaces
    }}>
      {children}
    </WorkspaceContext.Provider>
  );
};

export const useWorkspace = () => {
  const context = useContext(WorkspaceContext);
  if (!context) {
    throw new Error('useWorkspace must be used within a WorkspaceProvider');
  }
  return context;
};
