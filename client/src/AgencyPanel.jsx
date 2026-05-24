import React, { useState, useEffect } from 'react';
import { LayoutDashboard, Briefcase, Users, Zap } from 'lucide-react';

export default function AgencyPanel() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:5001/execute', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ task: 'get_agents' })
    })
      .then((res) => res.json())
      .then((data) => { setAgents(data.agents); setLoading(false); })
      .catch((err) => { console.error('Error:', err); setLoading(false); });
  }, []);

  return (
    <div className="flex h-screen bg-slate-50 text-slate-900 font-sans">
      <nav className="w-64 bg-white border-r border-slate-200 p-4 flex flex-col">
        <div className="text-xl font-bold mb-8 text-blue-700 flex items-center gap-2 px-2">
          <Zap className="text-blue-600 fill-current" /> AgencyOS
        </div>
        <div className="space-y-1">
          {[ { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard }, { id: 'projects', label: 'Projects', icon: Briefcase }, { id: 'pods', label: 'Agents', icon: Users } ].map((item) => (
            <button key={item.id} onClick={() => setActiveTab(item.id)} className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors ${activeTab === item.id ? 'bg-blue-50 text-blue-700' : 'text-slate-600 hover:bg-slate-50'}`}>
              <item.icon size={18}/> {item.label}
            </button>
          ))}
        </div>
      </nav>
      <main className="flex-1 p-8 overflow-y-auto">
        <h1 className="text-2xl font-bold text-slate-800 mb-8 capitalize">{activeTab}</h1>
        {activeTab === 'pods' && (
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
            <h2 className="text-lg font-bold mb-4">Available Agents</h2>
            {loading ? <p>Loading...</p> : <div className="grid gap-3">{agents.map((a, i) => <div key={i} className="p-3 bg-slate-50 border rounded font-mono">{a}</div>)}</div>}
          </div>
        )}
      </main>
    </div>
  );
}
