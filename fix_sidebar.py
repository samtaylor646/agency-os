import re

with open('client/src/AgencyPanel.jsx', 'r') as f:
    code = f.read()

# Replace the nav section
# We'll use regex to find the entire <nav> block

nav_pattern = re.compile(r'<nav className="flex-1 p-4 overflow-y-auto">.*?</nav>', re.DOTALL)

new_nav = """<nav className="flex-1 p-3 overflow-y-auto flex flex-col">
          {/* Top Actions */}
          <div className="mb-6">
            <button 
              onClick={() => { setActiveTab('home'); setIsMobileMenuOpen(false); }}
              className={`group relative flex items-center ${isSidebarCollapsed ? 'justify-center w-12 h-12 rounded-full mx-auto' : 'w-full px-4 py-3 rounded-full'} bg-gray-100 hover:bg-gray-200 text-gray-800 transition-colors focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500`}
              aria-label="New Chat"
            >
              <Plus className="w-5 h-5 flex-shrink-0" aria-hidden="true" />
              {!isSidebarCollapsed && <span className="ml-3 font-medium text-sm">New Chat</span>}
              {isSidebarCollapsed && (
                <div className="absolute left-full ml-2 px-2 py-1 bg-gray-800 text-white text-xs rounded opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all whitespace-nowrap z-50" aria-hidden="true">
                  New Chat
                </div>
              )}
            </button>
          </div>

          {/* Recent Section */}
          <div className="mb-6 flex-1">
            {!isSidebarCollapsed && <p className="px-4 text-xs font-semibold text-gray-500 mb-2">Recent</p>}
            <SidebarItem icon={MessageSquare} label="Marketing Campaign Plan" active={activeTab === 'scope'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }} />
            <SidebarItem icon={MessageSquare} label="Q3 Strategy Review" active={false} collapsed={isSidebarCollapsed} onClick={() => {}} />
            <SidebarItem icon={MessageSquare} label="Website Redesign Copy" active={false} collapsed={isSidebarCollapsed} onClick={() => {}} />
          </div>

          {/* Bottom Admin/Utility Section */}
          <div className="mt-auto pt-4 border-t border-gray-200">
            {userRole === 'Agency Admin' && (
              <>
                <SidebarItem icon={Settings} label="Settings" active={activeTab === 'settings'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('settings'); setIsMobileMenuOpen(false); }} />
                <SidebarItem icon={Users} label="Access Control" active={activeTab === 'rbac'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('rbac'); setIsMobileMenuOpen(false); }} />
                <SidebarItem icon={Database} label="Audit Logs" active={activeTab === 'audit'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('audit'); setIsMobileMenuOpen(false); }} />
              </>
            )}
            <SidebarItem icon={Cpu} label="Workflows" active={activeTab === 'workflows'} collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('workflows'); setIsMobileMenuOpen(false); }} />
          </div>
        </nav>"""

code = nav_pattern.sub(new_nav, code)

with open('client/src/AgencyPanel.jsx', 'w') as f:
    f.write(code)
