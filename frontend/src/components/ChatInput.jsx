import { useState } from 'react'

export default function ChatInput({ onSend, disabled }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (message.trim() && !disabled) {
      onSend(message)
      setMessage('')
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-slate-200 p-4 bg-white">
      <div className="flex gap-4">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          disabled={disabled}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-slate-300 px-4 py-3
                     focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none
                     disabled:bg-slate-50 disabled:text-slate-400
                     transition-colors"
        />
        <button
          type="submit"
          disabled={disabled || !message.trim()}
          className="px-6 py-3 bg-indigo-600 text-white rounded-xl font-medium
                     hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-200 focus:outline-none
                     disabled:bg-slate-300 disabled:cursor-not-allowed
                     transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
            />
          </svg>
        </button>
      </div>
    </form>
  )
}
