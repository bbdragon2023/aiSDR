import { useState, useCallback, useRef } from 'react'
import { createChatStream, clearChat } from '../api/client'

export function useChat(sessionId = 'default') {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [loadingStatus, setLoadingStatus] = useState(null)
  const [toolName, setToolName] = useState(null)
  const [error, setError] = useState(null)
  const abortRef = useRef(null)

  const sendMessage = useCallback((message) => {
    // Add user message
    setMessages((prev) => [...prev, { role: 'user', content: message }])
    setIsLoading(true)
    setLoadingStatus('thinking')
    setError(null)

    let assistantMessage = ''

    abortRef.current = createChatStream(message, sessionId, (event) => {
      if (event.type === 'data') {
        const data = event.value

        if (data.status === 'processing') {
          setLoadingStatus('thinking')
        } else if (data.name) {
          // Tool event
          setLoadingStatus('tool')
          setToolName(data.name)
        } else if (data.text) {
          // Content event
          assistantMessage = data.text
        } else if (data.status === 'complete') {
          // Done event
          setMessages((prev) => [
            ...prev,
            { role: 'assistant', content: assistantMessage },
          ])
          setIsLoading(false)
          setLoadingStatus(null)
          setToolName(null)
        }
      } else if (event.type === 'error') {
        setError(event.value)
        setIsLoading(false)
        setLoadingStatus(null)
      } else if (event.type === 'done') {
        setIsLoading(false)
        setLoadingStatus(null)
      }
    })
  }, [sessionId])

  const clear = useCallback(async () => {
    if (abortRef.current) {
      abortRef.current()
    }
    await clearChat(sessionId)
    setMessages([])
    setError(null)
  }, [sessionId])

  const cancel = useCallback(() => {
    if (abortRef.current) {
      abortRef.current()
      setIsLoading(false)
      setLoadingStatus(null)
    }
  }, [])

  return {
    messages,
    isLoading,
    loadingStatus,
    toolName,
    error,
    sendMessage,
    clear,
    cancel,
  }
}
