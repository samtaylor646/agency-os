import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatScopeInterface from './ChatScopeInterface';

// Mock useWorkspace globally
jest.mock('./WorkspaceContext', () => ({
  useWorkspace: () => ({
    apiFetch: jest.fn().mockImplementation((url, options) => {
      if (url.includes('/api/v1/projects') && options?.method === 'POST') {
         return Promise.resolve({ ok: true, json: async () => ({ id: 1, name: 'New Project', description: '', tech_stack: [] }) });
      }
      if (url.includes('/api/v1/projects') && !options) {
         return Promise.resolve({ ok: true, json: async () => ([{ id: 1, name: 'Test Project', description: 'A test project', tech_stack: ['React'] }]) });
      }
      if (url.includes('/api/v1/chat') && url.endsWith('/chat') && !options) {
         return Promise.resolve({ ok: true, json: async () => ([{ id: 1, name: 'Scoping Chat' }]) });
      }
      if (url.includes('/api/v1/chat/1') && !url.includes('messages') && !options) {
         return Promise.resolve({ ok: true, json: async () => ({ messages: [{ role: 'assistant', content: 'Hello' }] }) });
      }
      if (url.includes('/api/v1/chat/scope')) {
         return Promise.resolve({
            ok: true,
            json: async () => ({
              response: 'Mock assistant response',
              extracted_details: {
                name: 'Test Project',
                description: 'A test project updated',
                tech_stack: ['React', 'Node']
              }
            })
         });
      }
      return Promise.resolve({ ok: true, json: async () => ({}) });
    }),
    activeWorkspaceId: '1'
  })
}));

describe('ChatScopeInterface', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders initial UI correctly', async () => {
    render(<ChatScopeInterface />);
    expect(screen.getByPlaceholderText('What would you like to build?')).toBeInTheDocument();
    
    await waitFor(() => {
       expect(screen.getByText('Hello')).toBeInTheDocument();
    });
  });
});
