"""Research API routes with SSE streaming."""

from typing import Generator, Optional

from flask import Blueprint, Response, request

from sdr_agent.agent import SDRAgent
from web.routes.chat import get_agent, sse_event

research_bp = Blueprint("research", __name__)


def research_stream(
    agent: SDRAgent,
    company: Optional[str] = None,
    prospect: Optional[str] = None,
) -> Generator[str, None, None]:
    """Stream research response with SSE events."""
    # Emit thinking event
    yield sse_event("thinking", {"status": "researching"})

    # Build research prompt
    if prospect:
        company_context = f" at {company}" if company else ""
        prompt = f"""Research the prospect "{prospect}"{company_context} thoroughly.

Please find and summarize:
1. Current role and responsibilities
2. Professional background and experience
3. Education and certifications
4. Recent public activity (posts, articles, speaking)
5. Professional interests and focus areas
6. Any personal details that could help personalize outreach

Provide a comprehensive prospect profile that would help craft a personalized outreach message."""
    else:
        prompt = f"""Research the company "{company}" thoroughly.

Please find and summarize:
1. Company overview (what they do, industry, size)
2. Recent news and developments
3. Key products or services
4. Technology stack (if detectable)
5. Key decision makers (C-suite, VP-level)
6. Any recent funding or financial news

Provide a comprehensive research report that would help an SDR prepare for outreach."""

    # Get system prompt
    system_prompt = agent._build_system_prompt()

    # Get initial response from Claude
    response = agent.claude.chat(prompt, system_prompt)

    # Handle tool calls in a loop
    while response.tool_calls:
        for tool_call in response.tool_calls:
            # Emit tool execution event
            yield sse_event("tool", {
                "name": tool_call.name,
                "input": tool_call.input,
            })

        # Execute tools and build results
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

            # Emit tool result
            yield sse_event("tool_result", {
                "name": tool_call.name,
                "success": not result.startswith("Error"),
            })

        # Continue conversation
        response = agent.claude.continue_with_tool_results(tool_results, system_prompt)

    # Emit content event with final response
    yield sse_event("content", {"text": response.content})

    # Emit done event
    yield sse_event("done", {"status": "complete"})


@research_bp.route("/research/company", methods=["POST"])
def research_company():
    """Research a company with SSE streaming response."""
    data = request.get_json()
    company = data.get("company", "")
    session_id = data.get("session_id", "default")

    if not company:
        return {"error": "Company name is required"}, 400

    try:
        agent = get_agent(session_id)
    except ValueError as e:
        return {"error": str(e)}, 500

    return Response(
        research_stream(agent, company=company),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@research_bp.route("/research/prospect", methods=["POST"])
def research_prospect():
    """Research a prospect with SSE streaming response."""
    data = request.get_json()
    prospect = data.get("prospect", "")
    company = data.get("company")
    session_id = data.get("session_id", "default")

    if not prospect:
        return {"error": "Prospect name is required"}, 400

    try:
        agent = get_agent(session_id)
    except ValueError as e:
        return {"error": str(e)}, 500

    return Response(
        research_stream(agent, prospect=prospect, company=company),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
