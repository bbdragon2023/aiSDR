const API_BASE = '/api'

export async function clearChat(sessionId = 'default') {
  const response = await fetch(`${API_BASE}/chat/clear`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId }),
  })
  return response.json()
}

export function createChatStream(message, sessionId = 'default', onEvent) {
  const controller = new AbortController()

  fetch(`${API_BASE}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, session_id: sessionId }),
    signal: controller.signal,
  })
    .then(async (response) => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            const eventType = line.slice(7)
            onEvent({ type: 'eventType', value: eventType })
          } else if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              onEvent({ type: 'data', value: data })
            } catch (e) {
              console.error('Failed to parse SSE data:', e)
            }
          }
        }
      }

      onEvent({ type: 'done' })
    })
    .catch((error) => {
      if (error.name !== 'AbortError') {
        onEvent({ type: 'error', value: error.message })
      }
    })

  return () => controller.abort()
}

export function createResearchStream(type, params, sessionId = 'default', onEvent) {
  const controller = new AbortController()
  const endpoint = type === 'company' ? 'company' : 'prospect'

  fetch(`${API_BASE}/research/${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...params, session_id: sessionId }),
    signal: controller.signal,
  })
    .then(async (response) => {
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            const eventType = line.slice(7)
            onEvent({ type: 'eventType', value: eventType })
          } else if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              onEvent({ type: 'data', value: data })
            } catch (e) {
              console.error('Failed to parse SSE data:', e)
            }
          }
        }
      }

      onEvent({ type: 'done' })
    })
    .catch((error) => {
      if (error.name !== 'AbortError') {
        onEvent({ type: 'error', value: error.message })
      }
    })

  return () => controller.abort()
}
