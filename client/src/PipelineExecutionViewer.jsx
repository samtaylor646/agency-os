import React, { useState, useEffect, useRef } from 'react';
import { Play, CheckCircle, Clock, AlertCircle, Terminal, Activity, FileText, ChevronRight, XCircle } from 'lucide-react';
import { useWorkspace } from './WorkspaceContext';

export const PipelineExecutionViewer = () => {
  const { currentWorkspace, apiFetch } = useWorkspace();
  const [pipelineState, setPipelineState] = useState('idle'); // idle, running, completed, error, waiting_approval
  const [pauseReason, setPauseReason] = useState('');
  const [errorDetails, setErrorDetails] = useState('');
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [tasks, setTasks] = useState([]);
  const [activeTask, setActiveTask] = useState(null);
  const [overallLogs, setOverallLogs] = useState([]);
  
  const logsEndRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [overallLogs, tasks, chatMessages]);

  useEffect(() => {
    if (!currentWorkspace) return;

    // Connect WebSocket
    const wsUrl = import.meta.env.VITE_WS_URL || (import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL.replace('http', 'ws') : 'ws://localhost:5000');
    const ws = new WebSocket(`${wsUrl}/ws/${currentWorkspace.id}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected for Pipeline Execution Viewer");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      } catch (e) {
        console.error("Failed to parse WS message", e);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, [currentWorkspace]);

  const handleWebSocketMessage = (data) => {
    switch(data.type) {
      case 'workflow_start':
        setPipelineState('running');
        setOverallLogs(prev => [...prev, `[SYSTEM] Workflow started: ${data.workflow_name}`]);
        // Initialize tasks from data.nodes if available
        if (data.nodes) {
          const newTasks = Object.entries(data.nodes).map(([id, info]) => ({
            id,
            name: info.task,
            agent: info.agent_name,
            status: 'pending',
            logs: []
          }));
          setTasks(newTasks);
        }
        break;

      case 'node_start':
        setActiveTask(data.node_id);
        setTasks(prev => prev.map(t => t.id === data.node_id ? { ...t, status: 'running', logs: [...t.logs, `[${data.agent_name}] Initializing...`] } : t));
        setOverallLogs(prev => [...prev, `[ORCHESTRATOR] Node ${data.node_id} started by ${data.agent_name}`]);
        break;

      case 'node_complete':
        setTasks(prev => prev.map(t => t.id === data.node_id ? { ...t, status: 'completed', logs: [...t.logs, `[SYSTEM] Completed successfully. Result: ${JSON.stringify(data.result)}`] } : t));
        setOverallLogs(prev => [...prev, `[ORCHESTRATOR] Node ${data.node_id} completed.`]);
        break;

      case 'node_failed':
        setTasks(prev => prev.map(t => t.id === data.node_id ? { ...t, status: 'error', logs: [...t.logs, `[ERROR] ${data.error}`] } : t));
        setOverallLogs(prev => [...prev, `[ERROR] Node ${data.node_id} failed: ${data.error}`]);
        break;

      case 'workflow_complete':
        setPipelineState('completed');
        setActiveTask(null);
        setOverallLogs(prev => [...prev, `[SYSTEM] Workflow execution finished with status: ${data.status}`]);
        if (data.status === 'PARTIAL_FAILURE') {
            setPipelineState('error');
            setErrorDetails('Workflow completed with partial failures.');
        }
        break;

      case 'workflow_failed':
        setPipelineState('error');
        setErrorDetails(data.error || 'Workflow execution failed.');
        setOverallLogs(prev => [...prev, `[ERROR] Workflow failed: ${data.error}`]);
        break;

      default:
        // Handle unhandled or generic messages
        break;
    }
  };

  const handleApprove = () => {
    // Left for backward compatibility/demo purposes if needed
  };

  const handleReject = () => {
    // Left for backward compatibility/demo purposes if needed
  };

  const handleSendChatMessage = (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    
    const newMsg = { sender: 'user', text: chatInput };
    setChatMessages(prev => [...prev, newMsg]);
    setOverallLogs(prev => [...prev, `[USER CHAT] ${chatInput}`]);
    
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
        wsRef.current.send(JSON.stringify({ type: 'user_message', text: chatInput }));
    }
    
    setChatInput('');
  };

  const startPipeline = async () => {
    if (!currentWorkspace) return;
    
    setPipelineState('running');
    setOverallLogs(prev => [...prev, '[SYSTEM] Triggering pipeline execution via API...']);
    
    // We send a request to the backend to start a test workflow
    try {
        const response = await apiFetch(`/api/v1/workflows/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nodes: [
                    { node_id: "1", agent_name: "nexus-strategy", task: "Analyze requirements", required_inputs: [] },
                    { node_id: "2", agent_name: "academic-psychologist", task: "Draft plan", required_inputs: ["1"] }
                ],
                edges: [
                    { from_node: "1", to_node: "2" }
                ]
            })
        });
        
        if (!response.ok) {
            setPipelineState('error');
            setErrorDetails('Failed to start pipeline via API.');
        }
    } catch (e) {
        setPipelineState('error');
        setErrorDetails(e.toString());
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'running': return <Clock className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'error': return <XCircle className="w-5 h-5 text-red-500" />;
      default: return <Clock className="w-5 h-5 text-gray-300" />;
    }
  };

  const activeTaskData = tasks.find(t => t.id === activeTask) || tasks.find(t => t.status === 'error') || tasks[tasks.length - 1];

  return (
    <div className="flex flex-col h-full space-y-4 md:space-y-6">
      <div className="bg-white p-4 md:p-6 rounded-xl border border-gray-200 md:border-gray-100 md:shadow-sm">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 md:gap-4 mb-4 md:mb-6">
          <div>
            <h2 className="text-lg md:text-xl font-bold text-gray-800 flex items-center tracking-tight">
              <Activity className="w-5 h-5 md:w-6 md:h-6 mr-2 text-blue-600 shrink-0" />
              Pipeline Execution
            </h2>
            <p className="text-gray-600 text-xs md:text-sm mt-1">Monitor real-time task orchestration and agent execution.</p>
          </div>
          <button 
            onClick={startPipeline}
            disabled={pipelineState === 'running'}
            className={`flex items-center justify-center px-4 py-2 rounded-xl text-sm md:text-base font-medium transition-colors w-full sm:w-auto shrink-0 uppercase tracking-wider md:tracking-normal md:normal-case ${
              pipelineState === 'running' 
                ? 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200 md:border-transparent' 
                : 'bg-blue-600 md:bg-blue-600 text-white hover:bg-blue-700 md:hover:bg-blue-700'
            }`}
          >
            {pipelineState === 'running' ? (
              <><Clock className="w-4 h-4 md:w-5 md:h-5 mr-2 animate-spin" /> Running...</>
            ) : (
              <><Play className="w-4 h-4 md:w-5 md:h-5 mr-2" /> Start Pipeline</>
            )}
          </button>
        </div>

          {/* Approval Gate UI */}
          {pipelineState === 'waiting_approval' && (
            <div className="mb-6 p-4 bg-yellow-50 border border-yellow-200 rounded-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 mr-3 shrink-0" />
                <div>
                  <h3 className="font-semibold text-yellow-800 text-sm md:text-base">Approval Required</h3>
                  <p className="text-yellow-700 text-xs md:text-sm mt-1">{pauseReason}</p>
                </div>
              </div>
              <div className="flex space-x-3 w-full md:w-auto">
                <button onClick={handleReject} className="flex-1 md:flex-none px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
                  Reject
                </button>
                <button onClick={handleApprove} className="flex-1 md:flex-none px-4 py-2 bg-yellow-600 text-white rounded-lg text-sm font-medium hover:bg-yellow-700 transition-colors">
                  Approve
                </button>
              </div>
            </div>
          )}

          {/* Error Escalation UI */}
          {pipelineState === 'error' && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start">
              <XCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 shrink-0" />
              <div>
                <h3 className="font-semibold text-red-800 text-sm md:text-base">Execution Error</h3>
                <p className="text-red-700 text-xs md:text-sm mt-1">{errorDetails}</p>
              </div>
            </div>
          )}

        {/* DAG / Task List Visualizer */}
        <div className="relative">
          <div className="absolute left-6 md:left-8 top-0 bottom-0 w-0.5 bg-gray-100 z-0"></div>
          <div className="space-y-3 md:space-y-4 relative z-10">
            {tasks.map((task, index) => (
              <div 
                key={task.id} 
                className={`flex items-start space-x-3 md:space-x-4 p-3 md:p-4 rounded-xl border transition-all ${
                  task.status === 'running' ? 'border-blue-300 bg-blue-50/50 md:bg-blue-50 shadow-sm' : 
                  task.status === 'completed' ? 'border-green-200 bg-green-50/20 md:bg-green-50/30' : 
                  'border-gray-200 md:border-gray-100 bg-white'
                }`}
              >
                <div className="bg-white rounded-full p-1 border-2 border-white shadow-sm mt-0.5">
                  {getStatusIcon(task.status)}
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-gray-800">{task.name}</h3>
                      <div className="flex items-center text-sm text-gray-500 mt-1">
                        <span className="bg-gray-100 px-2 py-0.5 rounded-md text-xs font-mono text-gray-600 border border-gray-200">
                          {task.agent}
                        </span>
                      </div>
                    </div>
                    <div>
                      <span className={`text-xs font-medium px-2.5 py-1 rounded-full uppercase ${
                        task.status === 'running' ? 'bg-blue-100 text-blue-700' :
                        task.status === 'completed' ? 'bg-green-100 text-green-700' :
                        'bg-gray-100 text-gray-500'
                      }`}>
                        {task.status}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Logs and Terminal View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6 flex-1 min-h-[300px]">
        {/* Orchestrator Logs */}
        <div className="bg-gray-900 rounded-xl border border-gray-800 shadow-inner flex flex-col overflow-hidden">
          <div className="bg-gray-800 px-3 md:px-4 py-2 border-b border-gray-700 flex items-center">
            <Terminal className="w-4 h-4 text-gray-400 mr-2" />
            <span className="text-[10px] md:text-sm font-medium text-gray-300 font-mono uppercase tracking-wider md:tracking-normal md:normal-case">Orchestrator Logs</span>
          </div>
          <div className="p-3 md:p-4 flex-1 overflow-y-auto font-mono text-[11px] md:text-sm space-y-2">
            {overallLogs.length === 0 ? (
              <span className="text-gray-500 italic">Waiting for pipeline to start...</span>
            ) : (
              overallLogs.map((log, i) => (
                <div key={i} className={`${
                  log.includes('[SYSTEM]') ? 'text-blue-400 font-semibold' : 'text-gray-300'
                }`}>
                  {log}
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>

          {/* Active Agent Context/Logs & Chat */}
          <div className="bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col overflow-hidden">
            <div className="bg-gray-50 md:bg-gray-50 px-3 md:px-4 py-2 md:py-3 border-b border-gray-200 flex items-center justify-between">
              <div className="flex items-center text-gray-700 font-medium text-[10px] md:text-sm uppercase tracking-wider md:tracking-normal md:normal-case">
                <FileText className="w-4 h-4 mr-2 text-indigo-500 hidden md:block" />
                Agent Execution Scope
              </div>
              {activeTaskData && (
                 <span className="text-[10px] md:text-xs bg-indigo-50 text-indigo-700 px-1.5 md:px-2 py-0.5 md:py-1 rounded-sm md:rounded font-mono border border-indigo-100">
                   {activeTaskData.agent}
                 </span>
              )}
            </div>
            <div className="p-3 md:p-4 flex-1 overflow-y-auto bg-gray-50 font-mono text-[11px] md:text-sm space-y-2 border-b border-gray-200 min-h-[150px]">
              {(!activeTaskData || activeTaskData.logs.length === 0) ? (
                 <div className="flex flex-col items-center justify-center h-full text-gray-400 space-y-2">
                   <Terminal className="w-6 h-6 md:w-8 md:h-8 opacity-20" />
                   <span>No active agent logs.</span>
                 </div>
              ) : (
                activeTaskData.logs.map((log, i) => (
                  <div key={i} className="text-slate-700 break-words">
                    <span className="text-slate-400 select-none mr-2">{'>'}</span>{log}
                  </div>
                ))
              )}
              <div ref={logsEndRef} />
            </div>

            {/* Mid-Execution Chat Interface */}
            <div className="flex flex-col h-[200px] bg-white">
              <div className="bg-gray-100 px-3 py-2 border-b border-gray-200 text-xs font-semibold text-gray-600 uppercase tracking-wide">
                Mid-Execution Chat
              </div>
              <div className="flex-1 overflow-y-auto p-3 space-y-3">
                {chatMessages.length === 0 ? (
                  <div className="text-center text-gray-400 text-xs mt-4">
                    Send a message to interject or provide feedback to the active agent.
                  </div>
                ) : (
                  chatMessages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                        msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {msg.text}
                      </div>
                    </div>
                  ))
                )}
                <div ref={logsEndRef} />
              </div>
              <form onSubmit={handleSendChatMessage} className="p-3 border-t border-gray-200 bg-gray-50 flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  placeholder={pipelineState === 'idle' || pipelineState === 'completed' ? "Pipeline not active" : "Message active agent..."}
                  disabled={pipelineState === 'idle' || pipelineState === 'completed'}
                  className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:text-gray-400"
                />
                <button
                  type="submit"
                  disabled={pipelineState === 'idle' || pipelineState === 'completed' || !chatInput.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Send
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PipelineExecutionViewer;
