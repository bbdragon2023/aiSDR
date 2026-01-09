# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Install dependencies
uv sync

# Install dev dependencies
uv sync --all-extras

# Run interactive chat
uv run sdr-agent chat

# Research commands
uv run sdr-agent research --company "Acme Corp"
uv run sdr-agent research --prospect "John Smith" --company "Acme Corp"

# List available skills
uv run sdr-agent skills

# Run tests
uv run pytest

# Run single test
uv run pytest tests/test_file.py::test_function -v

# Lint
uv run ruff check .

# Fix lint issues
uv run ruff check . --fix
```

## Architecture

This is an AI Sales Development Representative (SDR) agent built on the [Agent Skills](https://agentskills.io) open standard.

### Core Flow

1. **SDRAgent** (`agent.py`) orchestrates all components - handles user input, coordinates tool execution, manages conversation
2. **ClaudeClient** (`llm/claude.py`) wraps Anthropic API with tool use support - maintains conversation history, handles tool call responses
3. **SkillLoader** (`skills/loader.py`) discovers and parses SKILL.md files from `skills/` directory at startup
4. **SkillExecutor** (`skills/executor.py`) handles tool execution including `web_search` (via Tavily), `read_skill`, and running skill scripts

### Agent Tool Loop

The agent uses a tool-use loop pattern in `SDRAgent.chat()`:
1. Send user message with system prompt containing available skills
2. If response contains tool calls, execute them via `SkillExecutor`
3. Continue conversation with tool results until no more tool calls

### Skills System

Skills are modular instruction sets in `skills/` directory. Each skill folder contains:
- `SKILL.md` - Required. YAML frontmatter (name, description) + markdown instructions
- `references/` - Optional reference documents loadable via `SkillLoader.load_reference()`
- `scripts/` - Optional executable scripts runnable via `SkillExecutor.run_skill_script()`

Skills are loaded into the system prompt as XML (`generate_available_skills_xml()`) and can be fully loaded at runtime via the `read_skill` tool.

### Available Tools

Tools are defined in `ClaudeClient._build_tools()`:
- `web_search` - Tavily-powered web search for research
- `send_email` - SMTP email sending (handled by SDRAgent, not SkillExecutor)
- `read_skill` - Load full skill instructions at runtime

## Configuration

Settings loaded via pydantic-settings from `.env` file. Required: `ANTHROPIC_API_KEY`. Optional: `TAVILY_API_KEY` (for research), SMTP settings (for email).
