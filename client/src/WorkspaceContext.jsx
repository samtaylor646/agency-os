import React, { createContext, useContext, useState, useEffect } from 'react';

const WorkspaceContext = createContext(null);

export const WorkspaceProvider = ({ children }) => {
  const [workspaces, setWorkspaces] = useState([]);
  const [activeWorkspaceId, setActiveWorkspaceId] = useState(null);
  const [userRole, setUserRole] = useState('Agency Admin'); // Mocked user role for now

  // Fetch workspaces on mount
  useEffect(() => {
    const fetchWorkspaces = async () => {
      try {
        // Mock API call
        const mockWorkspaces = [
          { id: '1', name: 'Acme Corp' },
          { id: '2', name: 'Globex Inc' }
        ];
        setWorkspaces(mockWorkspaces);
        
        // Retrieve last active from localStorage or default to first
        const saved = localStorage.getItem('activeWorkspaceId');
        if (saved && mockWorkspaces.find(w => w.id === saved)) {
          setActiveWorkspaceId(saved);
        } else if (mockWorkspaces.length > 0) {
          setActiveWorkspaceId(mockWorkspaces[0].id);
        }
      } catch (err) {
        console.error('Failed to fetch workspaces', err);
      }
    };
    
    fetchWorkspaces();
  }, []);

  useEffect(() => {
    if (activeWorkspaceId) {
      localStorage.setItem('activeWorkspaceId', activeWorkspaceId);
    }
  }, [activeWorkspaceId]);

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
      'X-Tenant-ID': activeWorkspaceId,
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    };
    
    const res = await fetch(url, { ...options, headers });
    
    // Handle token expiry
    if (res.status === 401) {
      localStorage.removeItem('agency_os_token');
    }
    
    return res;
  };

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
