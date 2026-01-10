export default function LoadingIndicator({ status, toolName }) {
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3">
        <div className="flex items-center gap-3">
          {/* Animated dots */}
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                 style={{ animationDelay: '0ms' }} />
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                 style={{ animationDelay: '150ms' }} />
            <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce"
                 style={{ animationDelay: '300ms' }} />
          </div>

          {/* Status text */}
          <span className="text-sm text-slate-600">
            {status === 'thinking' && 'Thinking...'}
            {status === 'tool' && (
              <span className="flex items-center gap-2">
                <span className="px-2 py-0.5 bg-amber-100 text-amber-700 rounded text-xs font-medium">
                  {toolName === 'web_search' && 'Searching web'}
                  {toolName === 'read_skill' && 'Loading skill'}
                  {toolName === 'send_email' && 'Sending email'}
                  {!['web_search', 'read_skill', 'send_email'].includes(toolName) && toolName}
                </span>
              </span>
            )}
          </span>
        </div>
      </div>
    </div>
  )
}
