import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatScopeInterface from './ChatScopeInterface';

// Mock fetch globally
global.fetch = jest.fn();

describe('ChatScopeInterface', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  test('renders initial UI correctly', () => {
    render(<ChatScopeInterface />);
    expect(screen.getByText('Project Scoping Chat')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Describe your project...')).toBeInTheDocument();
    expect(screen.getByText('Project Preview')).toBeInTheDocument();
  });

  test('sends message and updates UI on success', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        response: 'Mock assistant response',
        extracted_details: {
          name: 'Test Project',
          description: 'A test project',
          tech_stack: ['React', 'Node']
        }
      })
    });

    render(<ChatScopeInterface />);
    
    const input = screen.getByPlaceholderText('Describe your project...');
    const sendButton = screen.getByRole('button', { name: /send/i });

    // Type and send message
    fireEvent.change(input, { target: { value: 'I want a test project' } });
    fireEvent.click(sendButton);

    // Should show user message
    expect(screen.getByText('I want a test project')).toBeInTheDocument();
    
    // Wait for the assistant response
    await waitFor(() => {
      expect(screen.getByText('Mock assistant response')).toBeInTheDocument();
    });

    // Check if extracted details updated
    expect(screen.getByText('Test Project')).toBeInTheDocument();
    expect(screen.getByText('A test project')).toBeInTheDocument();
    expect(screen.getByText('React')).toBeInTheDocument();
    expect(screen.getByText('Node')).toBeInTheDocument();
  });

  test('handles network error', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<ChatScopeInterface />);
    
    const input = screen.getByPlaceholderText('Describe your project...');
    const sendButton = screen.getByRole('button', { name: /send/i });

    fireEvent.change(input, { target: { value: 'Trigger error' } });
    fireEvent.click(sendButton);

    await waitFor(() => {
      expect(screen.getByText('Error: Could not reach the server.')).toBeInTheDocument();
    });
  });
});
