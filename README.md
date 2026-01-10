# AI SDR Agent

AI-powered Sales Development Representative agent built on the [Agent Skills](https://agentskills.io) open standard.

## Features

- **Company Research**: Research companies to understand their business, technology, funding, and decision makers
- **Prospect Research**: Research individual prospects for personalized outreach
- **Email Composition**: Generate personalized cold emails based on research
- **Lead Qualification**: Score and prioritize leads based on fit criteria

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Anthropic API key
- Tavily API key (for web search)

### Installation

```bash
# Clone the repository
cd ai_sdr_agent

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# Required: ANTHROPIC_API_KEY
# Optional: TAVILY_API_KEY (for web search)

# Install dependencies
uv sync
```

### Usage

#### Interactive Chat

```bash
uv run sdr-agent chat
```

#### Research Commands

```bash
# Research a company
uv run sdr-agent research --company "Acme Corp"

# Research a prospect
uv run sdr-agent research --prospect "John Smith" --company "Acme Corp"
```

#### List Skills

```bash
uv run sdr-agent skills
```

### Web Application

The SDR Agent also includes a beautiful web interface with real-time streaming responses.

#### Start the Backend

```bash
uv run sdr-web
```

The API server will start at http://localhost:5000

#### Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

The web UI will be available at http://localhost:5173

#### Features

- **Chat Interface**: Interactive chat with the SDR agent, with real-time streaming responses
- **Research Dashboard**: Research companies and prospects with visual results
- **Skills Viewer**: Browse available skills and their instructions

## Configuration

Create a `.env` file with the following variables:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional - for web search research
TAVILY_API_KEY=your_tavily_api_key

# Optional - for email sending
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=Your Name
```

## Agent Skills

This agent uses the Agent Skills standard for modular capabilities. Skills are located in the `skills/` directory:

| Skill | Description |
|-------|-------------|
| `company-research` | Research companies for B2B outreach |
| `prospect-research` | Research individual prospects |
| `email-composer` | Compose personalized sales emails |
| `lead-qualifier` | Score and qualify leads |

### Creating Custom Skills

Add new skills by creating a folder in `skills/` with a `SKILL.md` file:

```
skills/
└── my-skill/
    ├── SKILL.md          # Required: Skill definition
    ├── scripts/          # Optional: Executable scripts
    ├── references/       # Optional: Reference docs
    └── assets/           # Optional: Static resources
```

See the [Agent Skills specification](https://agentskills.io/specification) for details.

## Architecture

```
src/sdr_agent/           # Core agent (CLI)
├── main.py              # CLI entry point
├── agent.py             # Agent orchestrator
├── config.py            # Configuration management
├── llm/
│   └── claude.py        # Claude API integration
├── skills/
│   ├── loader.py        # Skill discovery & parsing
│   └── executor.py      # Skill execution
└── integrations/
    └── email.py         # SMTP email client

web/                     # Flask backend (Web API)
├── app.py               # Flask application
└── routes/
    ├── chat.py          # Chat API with SSE streaming
    ├── research.py      # Research endpoints
    └── skills.py        # Skills endpoints

frontend/                # React frontend
├── src/
│   ├── components/      # UI components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom React hooks
│   └── api/             # API client
└── ...
```

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

## License

MIT
