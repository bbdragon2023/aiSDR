"""Claude API integration for SDR Agent."""

from typing import Any, Optional

import anthropic
from pydantic import BaseModel


class Message(BaseModel):
    """A conversation message."""

    role: str  # "user" or "assistant"
    content: str


class ToolCall(BaseModel):
    """A tool call from the model."""

    id: str
    name: str
    input: dict[str, Any]


class ClaudeResponse(BaseModel):
    """Response from Claude API."""

    content: str
    tool_calls: list[ToolCall] = []
    stop_reason: str


class ClaudeClient:
    """Client for interacting with Claude API."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 4096,
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.conversation: list[Message] = []

    def _build_tools(self) -> list[dict[str, Any]]:
        """Build tool definitions for the agent."""
        return [
            {
                "name": "web_search",
                "description": "Search the web for information about a company, person, or topic. Use this to research prospects and companies.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of results (default: 5)",
                            "default": 5,
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "send_email",
                "description": "Send an email to a prospect. Use this after composing a personalized email.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "Recipient email address",
                        },
                        "to_name": {
                            "type": "string",
                            "description": "Recipient name",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject line",
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body content",
                        },
                    },
                    "required": ["to_email", "subject", "body"],
                },
            },
            {
                "name": "read_skill",
                "description": "Load the full instructions from an agent skill. Use this when you need detailed guidance on a specific task.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "skill_name": {
                            "type": "string",
                            "description": "Name of the skill to load",
                        },
                    },
                    "required": ["skill_name"],
                },
            },
        ]

    def chat(
        self,
        user_message: str,
        system_prompt: str,
        tools_enabled: bool = True,
    ) -> ClaudeResponse:
        """Send a message and get a response."""
        self.conversation.append(Message(role="user", content=user_message))

        messages = [{"role": m.role, "content": m.content} for m in self.conversation]

        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": system_prompt,
            "messages": messages,
        }

        if tools_enabled:
            kwargs["tools"] = self._build_tools()

        response = self.client.messages.create(**kwargs)

        # Extract text content and tool calls
        text_content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        input=block.input,
                    )
                )

        # Add assistant response to conversation
        if text_content:
            self.conversation.append(Message(role="assistant", content=text_content))

        return ClaudeResponse(
            content=text_content,
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
        )

    def add_tool_result(self, tool_use_id: str, result: str) -> None:
        """Add a tool result to the conversation."""
        self.conversation.append(
            Message(
                role="user",
                content=f'<tool_result tool_use_id="{tool_use_id}">{result}</tool_result>',
            )
        )

    def continue_with_tool_results(
        self,
        tool_results: list[dict[str, str]],
        system_prompt: str,
    ) -> ClaudeResponse:
        """Continue the conversation after tool execution."""
        # Format tool results for Claude
        tool_result_content = []
        for result in tool_results:
            tool_result_content.append(
                {
                    "type": "tool_result",
                    "tool_use_id": result["tool_use_id"],
                    "content": result["content"],
                }
            )

        # Build messages including the tool results
        messages = [{"role": m.role, "content": m.content} for m in self.conversation]
        messages.append({"role": "user", "content": tool_result_content})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system_prompt,
            messages=messages,
            tools=self._build_tools(),
        )

        # Extract response
        text_content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=block.id,
                        name=block.name,
                        input=block.input,
                    )
                )

        if text_content:
            self.conversation.append(Message(role="assistant", content=text_content))

        return ClaudeResponse(
            content=text_content,
            tool_calls=tool_calls,
            stop_reason=response.stop_reason,
        )

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.conversation = []
