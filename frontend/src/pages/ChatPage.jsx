import { useRef, useEffect } from 'react'
import { useChat } from '../hooks/useChat'
import ChatMessage from '../components/ChatMessage'
import ChatInput from '../components/ChatInput'
import LoadingIndicator from '../components/LoadingIndicator'

export default function ChatPage() {
  const { messages, isLoading, loadingStatus, toolName, error, sendMessage, clear } = useChat()
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-white">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Chat</h2>
          <p className="text-sm text-slate-500">Ask me anything about sales research</p>
        </div>
        <button
          onClick={clear}
          className="px-4 py-2 text-sm text-slate-600 hover:text-slate-900
                     hover:bg-slate-100 rounded-lg transition-colors"
        >
          Clear Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6">
        {messages.length === 0 && !isLoading ? (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
              <svg className="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-slate-900 mb-2">Start a Conversation</h3>
            <p className="text-slate-500 max-w-sm">
              Ask me to research companies, find prospects, compose emails, or qualify leads.
            </p>
            <div className="flex flex-wrap gap-2 mt-6 justify-center">
              {[
                'Research Anthropic',
                'Find CTOs in AI startups',
                'Write a cold email',
                'Qualify this lead',
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => sendMessage(suggestion)}
                  className="px-4 py-2 bg-white border border-slate-200 rounded-full text-sm
                           text-slate-600 hover:border-indigo-300 hover:text-indigo-600
                           transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage
                key={index}
                message={message.content}
                isUser={message.role === 'user'}
              />
            ))}
            {isLoading && (
              <LoadingIndicator status={loadingStatus} toolName={toolName} />
            )}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
                Error: {error}
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  )
}
