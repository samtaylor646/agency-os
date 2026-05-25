import re

with open('client/src/AgencyPanel.jsx', 'r') as f:
    code = f.read()

code = code.replace(
    "import CreateWorkspaceModal from './CreateWorkspaceModal';",
    "import CreateWorkspaceModal from './CreateWorkspaceModal';\nimport IntroPage from './IntroPage';"
)

code = code.replace(
    "const handleSendPrompt = async () => {\n    if (!chatInput.trim()) return;\n    \n    showNotification(`Processing your request: \"${chatInput}\"...`);",
    "const handleSendPrompt = async (overridePrompt) => {\n    const promptToSend = typeof overridePrompt === 'string' ? overridePrompt : chatInput;\n    if (!promptToSend.trim()) return;\n    \n    showNotification(`Processing your request: \"${promptToSend}\"...`);"
)

code = code.replace(
    "body: JSON.stringify({ message: chatInput }),",
    "body: JSON.stringify({ message: promptToSend }),"
)

code = code.replace(
    "          <div className=\"max-w-5xl mx-auto w-full flex-1 mb-20\">\n            {activeTab === 'dashboard' && (\n              userRole === 'Agency Admin' ? (\n                <div>\n                  <h2 className=\"text-xl sm:text-2xl font-bold text-gray-800 mb-4 sm:mb-6\">Agency Overview: {activeWorkspace?.name}</h2>\n                  <p className=\"text-gray-600\">Select \"Workspace Settings\" to manage this tenant, or switch workspaces using the dropdown in the sidebar.</p>\n                </div>\n              ) : (\n                <ClientPortalView />\n              )\n            )}",
    "          <div className=\"max-w-5xl mx-auto w-full flex-1 mb-20 flex flex-col\">\n            {activeTab === 'dashboard' && (\n              userRole === 'Agency Admin' ? (\n                <IntroPage onPromptSubmit={(prompt) => {\n                  setChatInput(prompt);\n                  handleSendPrompt(prompt);\n                  setActiveTab('scope');\n                }} />\n              ) : (\n                <ClientPortalView />\n              )\n            )}"
)

code = code.replace(
    "          {/* Chat Prompt Box */}\n          <div className=\"max-w-3xl mx-auto w-full mt-auto fixed bottom-0 md:bottom-6 left-0 right-0 md:pl-64 md:px-4 pointer-events-none\">",
    "          {/* Chat Prompt Box */}\n          {!(activeTab === 'dashboard' && userRole === 'Agency Admin') && (\n          <div className=\"max-w-3xl mx-auto w-full mt-auto fixed bottom-0 md:bottom-6 left-0 right-0 md:pl-64 md:px-4 pointer-events-none\">"
)

code = code.replace(
    "              </button>\n            </div>\n          </div>\n        </div>\n      </main>",
    "              </button>\n            </div>\n          </div>\n          )}\n        </div>\n      </main>"
)

with open('client/src/AgencyPanel.jsx', 'w') as f:
    f.write(code)
