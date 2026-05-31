import re

with open("client/src/ChatScopeInterface.jsx", "r") as f:
    content = f.read()

# Add useWorkspace import
if "import { useWorkspace }" not in content:
    content = content.replace("import React,", "import React, { useState, useRef, useEffect } from 'react';\nimport { useWorkspace } from './WorkspaceContext';\n//")

# Replace initial state
content = re.sub(
    r"const \[messages, setMessages\] = useState\(\[[\s\S]*?\]\);",
    "const [messages, setMessages] = useState([]);\n  const { apiFetch, activeWorkspaceId } = useWorkspace();\n  const [chatId, setChatId] = useState(null);\n  const [projectId, setProjectId] = useState(null);",
    content
)

content = re.sub(
    r"const \[projectDetails, setProjectDetails\] = useState\(\{[\s\S]*?\}\);",
    "const [projectDetails, setProjectDetails] = useState({\n    name: '',\n    description: '',\n    tech_stack: []\n  });",
    content
)

# Insert useEffect for initialization
init_effect = """
  useEffect(() => {
    const initialize = async () => {
      try {
        let currentProjectId = null;
        let currentChatId = null;

        const projRes = await apiFetch('/api/v1/projects');
        if (projRes.ok) {
          const projs = await projRes.json();
          if (projs.length > 0) {
            currentProjectId = projs[0].id;
            setProjectId(currentProjectId);
            setProjectDetails({
              name: projs[0].name,
              description: projs[0].description,
              tech_stack: projs[0].tech_stack || []
            });
          } else {
            const newProjRes = await apiFetch('/api/v1/projects', {
              method: 'POST',
              body: JSON.stringify({ name: 'New Project', description: '', tech_stack: [] })
            });
            if (newProjRes.ok) {
              const newProj = await newProjRes.json();
              currentProjectId = newProj.id;
              setProjectId(currentProjectId);
            }
          }
        }

        const chatRes = await apiFetch('/api/v1/chat');
        if (chatRes.ok) {
          const chats = await chatRes.json();
          if (chats.length > 0) {
            currentChatId = chats[0].id;
            setChatId(currentChatId);
            const chatDetailsRes = await apiFetch(`/api/v1/chat/${currentChatId}`);
            if (chatDetailsRes.ok) {
              const chatDetails = await chatDetailsRes.json();
              if (chatDetails.messages && chatDetails.messages.length > 0) {
                setMessages(chatDetails.messages);
              }
            }
          } else {
            const newChatRes = await apiFetch('/api/v1/chat', {
              method: 'POST',
              body: JSON.stringify({ project_id: currentProjectId, name: 'Scoping Chat' })
            });
            if (newChatRes.ok) {
              const newChat = await newChatRes.json();
              currentChatId = newChat.id;
              setChatId(currentChatId);
            }
          }
        }
      } catch (error) {
        console.error('Failed to initialize chat scope:', error);
      }
    };
    if (activeWorkspaceId) {
      initialize();
    }
  }, [apiFetch, activeWorkspaceId]);
"""

content = content.replace("const messagesEndRef = useRef(null);", init_effect + "\n  const messagesEndRef = useRef(null);")

# Update handleSendMessage fetch
handle_send = """
    try {
      if (chatId) {
        await apiFetch(`/api/v1/chat/${chatId}/messages`, {
          method: 'POST',
          body: JSON.stringify(userMessage)
        });
      }

      const response = await apiFetch('/api/v1/chat/scope', {
        method: 'POST',
        body: JSON.stringify({ message: inputValue }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const assistantMessage = { role: 'assistant', content: data.chat_response || data.response || "No response" };
      
      if (chatId) {
        await apiFetch(`/api/v1/chat/${chatId}/messages`, {
          method: 'POST',
          body: JSON.stringify(assistantMessage)
        });
      }

      setMessages((prev) => [...prev, assistantMessage]);
      
      const extraction = data.extraction || data.extracted_details;
      if (extraction) {
        setProjectDetails(extraction);
        if (projectId) {
          await apiFetch(`/api/v1/projects/${projectId}`, {
            method: 'PUT',
            body: JSON.stringify({
              name: extraction.name || 'New Project',
              description: extraction.description || '',
              tech_stack: extraction.tech_stack || []
            })
          });
        }
      }
"""
content = re.sub(
    r"try \{\s*const response = await fetch\('/api/v1/chat/scope'[\s\S]*?if \(data\.extraction\) \{[\s\S]*?setProjectDetails\(data\.extracted_details\);\s*\}",
    handle_send,
    content
)

# Update document generation fetch
content = content.replace(
    "const response = await fetch(`/api/v1/chat/1/generate/${docType}`",
    "const response = await apiFetch(`/api/v1/chat/${chatId || 1}/generate/${docType}`"
)
content = content.replace(
    "headers: { 'Content-Type': 'application/json' },",
    ""
)


# clean up duplicate imports
content = re.sub(r"import React,.*?from 'react';\n//.*?\nimport React, { useState, useRef, useEffect } from 'react';", "import React, { useState, useRef, useEffect } from 'react';", content)

with open("client/src/ChatScopeInterface.jsx", "w") as f:
    f.write(content)
