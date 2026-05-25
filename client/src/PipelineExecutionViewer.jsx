import React, { useState, useEffect, useRef } from 'react';
import { Play, CheckCircle, Clock, AlertCircle, Terminal, Activity, FileText, ChevronRight, XCircle } from 'lucide-react';

export const PipelineExecutionViewer = () => {
  const [pipelineState, setPipelineState] = useState('idle'); // idle, running, completed, error
  const [tasks, setTasks] = useState([
    { id: 't1', name: 'Parse Marketing Brief', agent: 'nexus-strategy', status: 'pending', logs: [] },
    { id: 't2', name: 'Extract Target Audience', agent: 'academic-psychologist', status: 'pending', logs: [] },
    { id: 't3', name: 'Draft Ad Copy', agent: 'design-visual-storyteller', status: 'pending', logs: [] },
    { id: 't4', name: 'Generate Visual Assets', agent: 'design-image-prompt-engineer', status: 'pending', logs: [] },
  ]);
  const [activeTask, setActiveTask] = useState(null);
  const [overallLogs, setOverallLogs] = useState([]);
  
  const logsEndRef = useRef(null);

  useEffect(() => {
    if (logsEndRef.current) {
      logsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [overallLogs, tasks]);

  const startPipeline = () => {
    setPipelineState('running');
    setOverallLogs(prev => [...prev, '[SYSTEM] Pipeline execution started.']);
    simulateExecution();
  };

  const simulateExecution = async () => {
    for (let i = 0; i < tasks.length; i++) {
      const task = tasks[i];
      setActiveTask(task.id);
      
      // Update task to running
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'running' } : t));
      setOverallLogs(prev => [...prev, `[ORCHESTRATOR] Assigned task "${task.name}" to agent: ${task.agent}`]);
      
      // Simulate task processing
      await new Promise(r => setTimeout(r, 1000));
      
      setTasks(prev => prev.map(t => {
        if (t.id === task.id) {
          return { ...t, logs: [...t.logs, `[${task.agent}] Initializing context...`] };
        }
        return t;
      }));
      
      await new Promise(r => setTimeout(r, 1500));
      
      setTasks(prev => prev.map(t => {
        if (t.id === task.id) {
          return { ...t, logs: [...t.logs, `[${task.agent}] Processing data and generating output...`] };
        }
        return t;
      }));
      
      await new Promise(r => setTimeout(r, 1000));
      
      // Complete task
      setTasks(prev => prev.map(t => t.id === task.id ? { ...t, status: 'completed', logs: [...t.logs, `[${task.agent}] Task completed successfully.`] } : t));
      setOverallLogs(prev => [...prev, `[ORCHESTRATOR] Task "${task.name}" completed.`]);
    }
    
    setPipelineState('completed');
    setActiveTask(null);
    setOverallLogs(prev => [...prev, '[SYSTEM] Pipeline execution finished successfully.']);
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
        </div>

        {/* Active Agent Context/Logs */}
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
          <div className="p-3 md:p-4 flex-1 overflow-y-auto bg-gray-50 font-mono text-[11px] md:text-sm space-y-2">
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
        </div>
      </div>
    </div>
  );
};

export default PipelineExecutionViewer;
