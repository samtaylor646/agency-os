import re

with open('client/src/AgencyPanel.jsx', 'r') as f:
    code = f.read()

# Update lucide-react imports
code = re.sub(
    r"from 'lucide-react';",
    "PanelLeftClose, PanelLeft, Tooltip } from 'lucide-react';",
    code
)
# Wait, Tooltip is not in lucide-react. Let's just use native title attribute or a simple group-hover tooltip.

code = code.replace("import { Users, Settings, Activity, FileText, Share2, Plus, ArrowRight, Play, CheckCircle, Clock, AlertCircle, Shield, Database, Store, BarChart2, Menu, X, Search, Send, MessageSquare, Bot, Cpu } from 'lucide-react';", "import { Users, Settings, Activity, FileText, Share2, Plus, ArrowRight, Play, CheckCircle, Clock, AlertCircle, Shield, Database, Store, BarChart2, Menu, X, Search, Send, MessageSquare, Bot, Cpu, PanelLeftClose, PanelLeft } from 'lucide-react';")

# Update SidebarItem
old_sidebar_item = """const SidebarItem = ({ icon: Icon, label, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg mb-1 transition-colors ${
      active ? 'bg-blue-50 text-blue-600 font-medium' : 'text-gray-600 hover:bg-gray-50'
    }`}
  >
    <Icon className="w-5 h-5" />
    <span>{label}</span>
  </button>
);"""

new_sidebar_item = """const SidebarItem = ({ icon: Icon, label, active, onClick, collapsed }) => (
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
code = code.replace(old_sidebar_item, new_sidebar_item)

# Add isSidebarCollapsed state
code = code.replace(
    "const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);",
    "const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);\n  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);"
)

# Update sidebar class
code = re.sub(
    r"className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 \$\{isMobileMenuOpen \? 'translate-x-0' : '-translate-x-full'\}`\}",
    "className={`fixed inset-y-0 left-0 z-50 ${isSidebarCollapsed ? 'w-20' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}",
    code
)

# Replace in case my regex didn't match exactly because of transition-transform vs transition-all
code = code.replace(
    "className={`fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 flex flex-col transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}",
    "className={`fixed inset-y-0 left-0 z-50 ${isSidebarCollapsed ? 'w-20' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transform transition-all duration-300 ease-in-out md:relative md:translate-x-0 ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}`}"
)


# Add toggle button in sidebar header
old_sidebar_header = """<div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">A</span>
            </div>
            <span className="text-xl font-bold text-gray-900">AgencyOS</span>
          </div>"""

new_sidebar_header = """<div className="flex items-center justify-between w-full">
            <div className={`flex items-center space-x-2 overflow-hidden transition-all duration-300 ${isSidebarCollapsed ? 'w-0 opacity-0' : 'w-auto opacity-100'}`}>
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-white font-bold text-xl">A</span>
              </div>
              <span className="text-xl font-bold text-gray-900 flex-shrink-0">AgencyOS</span>
            </div>
            <button 
              onClick={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
              className="p-1 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded hidden md:block"
            >
              {isSidebarCollapsed ? <PanelLeft className="w-5 h-5" /> : <PanelLeftClose className="w-5 h-5" />}
            </button>
          </div>"""
code = code.replace(old_sidebar_header, new_sidebar_header)

# Pass collapsed prop to SidebarItems
code = code.replace("onClick={() => { setActiveTab('dashboard'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('dashboard'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('scope'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('settings'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('settings'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('workflows'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('workflows'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('agents'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('agents'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('files'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('files'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('analytics'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('analytics'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('rbac'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('rbac'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('audit'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('audit'); setIsMobileMenuOpen(false); }}")
code = code.replace("onClick={() => { setActiveTab('marketplace'); setIsMobileMenuOpen(false); }}", "collapsed={isSidebarCollapsed} onClick={() => { setActiveTab('marketplace'); setIsMobileMenuOpen(false); }}")

# Handle section headers hiding when collapsed
code = code.replace(
    "<p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2\">Workspace</p>",
    "{!isSidebarCollapsed && <p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2\">Workspace</p>}"
)
code = code.replace(
    "<div className=\"px-2 mb-4\">\n              <ContextSwitcher />\n            </div>",
    "<div className=\"px-2 mb-4\">\n              {!isSidebarCollapsed ? <ContextSwitcher /> : <div className=\"w-full flex justify-center\"><div className=\"w-8 h-8 bg-blue-100 text-blue-800 rounded flex items-center justify-center font-bold\">W</div></div>}\n            </div>"
)
code = code.replace(
    "<p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2\">Menu</p>",
    "{!isSidebarCollapsed && <p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2\">Menu</p>}"
)
code = code.replace(
    "<p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider\">Administration</p>",
    "{!isSidebarCollapsed && <p className=\"px-4 text-xs font-semibold text-gray-400 uppercase tracking-wider\">Administration</p>}"
)

# hide role switcher when collapsed
code = code.replace(
    "<div className=\"p-4 border-t border-gray-200 bg-gray-50\">",
    "<div className={`p-4 border-t border-gray-200 bg-gray-50 transition-all ${isSidebarCollapsed ? 'hidden' : 'block'}`}>"
)

# padding left adjustment for main chat prompt box
code = code.replace(
    "md:pl-64",
    "${isSidebarCollapsed ? 'md:pl-20' : 'md:pl-64'}"
)

with open('client/src/AgencyPanel.jsx', 'w') as f:
    f.write(code)
