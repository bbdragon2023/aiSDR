"""Chat API routes with SSE streaming."""

import json
from typing import Generator

from flask import Blueprint, Response, current_app, request

from sdr_agent.agent import SDRAgent

chat_bp = Blueprint("chat", __name__)

# Store agent instances per session (simple in-memory storage)
_agents: dict[str, SDRAgent] = {}


def get_agent(session_id: str) -> SDRAgent:
    """Get or create an agent for a session."""
    if session_id not in _agents:
        settings = current_app.config.get("settings")
        if not settings:
            raise ValueError("Settings not configured")
        _agents[session_id] = SDRAgent(settings)
    return _agents[session_id]


def sse_event(event_type: str, data: dict) -> str:
    """Format a Server-Sent Event."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


def chat_stream(agent: SDRAgent, message: str) -> Generator[str, None, None]:
    """Stream chat response with SSE events."""
    # Emit thinking event
    yield sse_event("thinking", {"status": "processing"})

    # Get system prompt
    system_prompt = agent._build_system_prompt()

    # Get initial response from Claude
    response = agent.claude.chat(message, system_prompt)

    # Handle tool calls in a loop
    while response.tool_calls:
        for tool_call in response.tool_calls:
            # Emit tool execution event
            yield sse_event("tool", {
                "name": tool_call.name,
                "input": tool_call.input,
            })

            # Execute tool
            if tool_call.name == "send_email":
                result = agent._handle_send_email(tool_call.input)
            else:
                result = agent.skill_executor.execute_tool(
                    tool_call.name, tool_call.input
                )

            # Emit tool result
            yield sse_event("tool_result", {
                "name": tool_call.name,
                "success": not result.startswith("Error"),
            })

        # Build tool results
        tool_results = []
        for tool_call in response.tool_calls:
            if tool_call.name == "send_email":
                result = agent._handle_send_email(tool_call.input)
            else:
                result = agent.skill_executor.execute_tool(
                    tool_call.name, tool_call.input
                )
            tool_results.append({
                "tool_use_id": tool_call.id,
                "content": result,
            })

        # Continue conversation
        response = agent.claude.continue_with_tool_results(tool_results, system_prompt)

    # Emit content event with final response
    yield sse_event("content", {"text": response.content})

    # Emit done event
    yield sse_event("done", {"status": "complete"})


@chat_bp.route("/chat", methods=["POST"])
def chat():
    """Handle chat message with SSE streaming response."""
    data = request.get_json()
    message = data.get("message", "")
    session_id = data.get("session_id", "default")

    if not message:
        return {"error": "Message is required"}, 400

    try:
        agent = get_agent(session_id)
    except ValueError as e:
        return {"error": str(e)}, 500

    return Response(
        chat_stream(agent, message),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@chat_bp.route("/chat/clear", methods=["POST"])
def clear_chat():
    """Clear conversation history for a session."""
    data = request.get_json() or {}
    session_id = data.get("session_id", "default")

    if session_id in _agents:
        _agents[session_id].claude.clear_conversation()

    return {"status": "cleared"}


@chat_bp.route("/chat/history", methods=["GET"])
def get_history():
    """Get conversation history for a session."""
    session_id = request.args.get("session_id", "default")

    if session_id not in _agents:
        return {"messages": []}

    agent = _agents[session_id]
    messages = []

    for msg in agent.claude.messages:
        role = msg.get("role", "")
        content = msg.get("content", "")

        # Handle different content formats
        if isinstance(content, str):
            messages.append({"role": role, "content": content})
        elif isinstance(content, list):
            # Extract text from content blocks
            text_parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
            if text_parts:
                messages.append({"role": role, "content": "".join(text_parts)})

    return {"messages": messages}
