import React from 'react';

export default function ContextCard({ text, metadata, score }) {
  return (
    <div className="bg-white p-3 rounded-lg border border-gray-200 shadow-sm mb-3">
      <div className="flex justify-between items-center mb-2">
        <span className="text-xs font-semibold text-gray-500 uppercase">{metadata?.source || 'Memory Fragment'}</span>
        {score !== undefined && (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
            Score: {score.toFixed(2)}
          </span>
        )}
      </div>
      <p className="text-sm text-gray-700 line-clamp-3">{text}</p>
      {metadata?.timestamp && (
        <div className="mt-2 text-xs text-gray-400">
          {new Date(metadata.timestamp).toLocaleString()}
        </div>
      )}
    </div>
  );
}