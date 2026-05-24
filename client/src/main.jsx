import React from 'react'
import ReactDOM from 'react-dom/client'
import AgencyPanel from './AgencyPanel.jsx'
import { WorkspaceProvider } from './WorkspaceContext.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <WorkspaceProvider>
      <AgencyPanel />
    </WorkspaceProvider>
  </React.StrictMode>,
)