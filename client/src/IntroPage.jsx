import React, { useState } from 'react';
import { Search, Sparkles, FolderOpen, FileText, Bot } from 'lucide-react';

const IntroPage = ({ onPromptSubmit }) => {
  const [prompt, setPrompt] = useState('');

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && prompt.trim()) {
      onPromptSubmit(prompt);
    }
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-8 relative overflow-hidden bg-bg-default h-full">
      {/* Decorative background blur */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary-default/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="max-w-3xl w-full z-10 text-center space-y-8 mt-[-10vh]">
        <div className="space-y-4">
          <h1 className="text-4xl font-semibold text-text-strong tracking-tight">
            How can AgencyOS help you today?
          </h1>
          <p className="text-lg text-text-subtle">
            Initialize a workspace, query your analytics, or chat with custom agents.
          </p>
        </div>

        {/* Oversized Search Input */}
        <div className="relative group">
          <div className="absolute inset-0 bg-gradient-to-r from-primary-default to-indigo-500 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
          <div className="relative bg-bg-default border-2 border-border-default hover:border-primary-default rounded-xl shadow-sm transition-all flex items-center p-2 focus-within:border-primary-default focus-within:ring-4 focus-within:ring-primary-default/20">
            <Search className="w-6 h-6 text-text-muted ml-4 mr-3" aria-hidden="true" />
            <input
              type="text"
              role="search"
              aria-label="Universal search and command input"
              className="w-full bg-transparent border-none outline-none text-lg text-text-strong placeholder-text-muted py-4 pr-4"
              placeholder="Start a new project, analyze documents..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyDown}
            />
            <button 
              onClick={() => prompt.trim() && onPromptSubmit(prompt)}
              disabled={!prompt.trim()}
              className="bg-primary-default text-text-inverse p-3 rounded-lg mr-2 disabled:opacity-50 hover:bg-primary-hover transition-colors"
              aria-label="Submit prompt"
            >
              <Sparkles className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Quick Action Chips */}
        <div className="flex flex-wrap justify-center gap-3 pt-4">
          <button 
            className="flex items-center space-x-2 bg-bg-subtle hover:bg-bg-hover text-text-default px-4 py-2 rounded-full text-sm border border-border-default transition-colors"
            onClick={() => onPromptSubmit("Start a new workspace")}
          >
            <FolderOpen className="w-4 h-4 text-text-muted" />
            <span>Start a new workspace</span>
          </button>
          <button 
            className="flex items-center space-x-2 bg-bg-subtle hover:bg-bg-hover text-text-default px-4 py-2 rounded-full text-sm border border-border-default transition-colors"
            onClick={() => onPromptSubmit("Analyze recent documents")}
          >
            <FileText className="w-4 h-4 text-text-muted" />
            <span>Analyze recent documents</span>
          </button>
          <button 
            className="flex items-center space-x-2 bg-bg-subtle hover:bg-bg-hover text-text-default px-4 py-2 rounded-full text-sm border border-border-default transition-colors"
            onClick={() => onPromptSubmit("Create a custom agent")}
          >
            <Bot className="w-4 h-4 text-text-muted" />
            <span>Create a custom agent</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default IntroPage;