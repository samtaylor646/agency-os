import re

with open('client/src/AgencyPanel.jsx', 'r') as f:
    code = f.read()

# Change initial state
code = code.replace("useState('dashboard')", "useState('home')")

# Change SidebarItem Dashboard to Home
code = code.replace('label="Dashboard"', 'label="Home"')
code = code.replace("activeTab === 'dashboard'", "activeTab === 'home'")
code = code.replace("setActiveTab('dashboard')", "setActiveTab('home')")

# Change background of the main wrapper from bg-gray-50 to bg-white
code = code.replace('className="flex h-screen bg-gray-50 font-sans overflow-hidden relative"', 'className="flex h-screen bg-white font-sans overflow-hidden relative"')

# Change sidebar background from bg-white to bg-gray-50
code = code.replace('bg-white border-r border-gray-200 flex flex-col', 'bg-gray-50 border-r border-gray-200 flex flex-col')

with open('client/src/AgencyPanel.jsx', 'w') as f:
    f.write(code)
