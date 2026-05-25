import re

with open('client/src/AgencyPanel.jsx', 'r') as f:
    code = f.read()

# Fix sidebar toggle button
old_toggle = """<button 
              onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
              className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded hidden md:block"
            >"""
new_toggle = """<button 
              onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
              className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded hidden md:block focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-expanded={!isSidebarCollapsed}
              aria-controls="main-sidebar"
              aria-label={isSidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >"""
code = code.replace(old_toggle, new_toggle)

# Add id to sidebar
old_aside = "className={`fixed inset-y-0 left-0 z-50 ${isSidebarCollapsed ? 'w-20' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}"
new_aside = "id=\"main-sidebar\" className={`fixed inset-y-0 left-0 z-50 ${isSidebarCollapsed ? 'w-20' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}"
code = code.replace(old_aside, new_aside)

# Fix SidebarItem
old_item = """const SidebarItem = ({ icon: Icon, label, active, onClick, collapsed }) => (
  <button 
    onClick={onClick}
    className={`group relative w-full flex items-center ${collapsed ? 'justify-center px-0' : 'space-x-3 px-4'} py-3 rounded-lg mb-1 transition-colors ${
      active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600 hover:bg-gray-50'
    }`}
  >
    <Icon className="w-5 h-5 flex-shrink-0" />
    {!collapsed && <span className="truncate">{label}</span>}
    {collapsed && (
      <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50">
        {label}
      </div>
    )}
  </button>
);"""

new_item = """const SidebarItem = ({ icon: Icon, label, active, onClick, collapsed }) => (
  <button 
    onClick={onClick}
    className={`group relative w-full flex items-center ${collapsed ? 'justify-center px-0' : 'space-x-3 px-4'} py-3 rounded-lg mb-1 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 ${
      active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600 hover:bg-gray-50'
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
);"""
code = code.replace(old_item, new_item)

with open('client/src/AgencyPanel.jsx', 'w') as f:
    f.write(code)
