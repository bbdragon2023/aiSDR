"""SDR Agent orchestrator - connects Claude with Skills and integrations."""

from typing import Any, Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .config import Settings
from .integrations.email import EmailClient
from .llm.claude import ClaudeClient, ClaudeResponse
from .skills.executor import SkillExecutor
from .skills.loader import SkillLoader

SYSTEM_PROMPT_TEMPLATE = """\
You are an AI Sales Development Representative (SDR) agent. Your role is to help with:

1. **Company Research**: Research companies to understand their business,
   technology stack, funding, and key decision makers.
2. **Prospect Research**: Research individual prospects to understand their
   role, background, and interests.
3. **Email Composition**: Write personalized outreach emails based on research.
4. **Lead Qualification**: Evaluate and score leads based on fit criteria.

## Available Skills

You have access to specialized skills that provide detailed instructions for
specific tasks. When you need guidance on a complex task, use the `read_skill`
tool to load the relevant skill instructions.

{available_skills}

## Tools Available

- **web_search**: Search the web for information about companies, people, or topics
- **send_email**: Send an email to a prospect
- **read_skill**: Load detailed instructions from a skill

## Guidelines

1. Always research before reaching out - personalization is key
2. Keep emails concise and value-focused
3. Reference specific details from your research
4. Be professional but conversational
5. Focus on the prospect's needs, not your product features

When a user asks you to research a company or prospect, use the web_search tool
to gather information. When composing emails, reference the email-composer skill
for best practices.
"""


class SDRAgent:
    """Main SDR Agent that orchestrates all components."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.console = Console()

        # Initialize components
        self.skill_loader = SkillLoader(settings.skills_dir)
        self.skill_loader.discover_skills()

        self.skill_executor = SkillExecutor(
            skill_loader=self.skill_loader,
            tavily_api_key=settings.tavily_api_key,
        )

        self.claude = ClaudeClient(
            api_key=settings.anthropic_api_key,
            model=settings.claude_model,
            max_tokens=settings.max_tokens,
        )

        self.email_client: Optional[EmailClient] = None
        if settings.email_configured:
            self.email_client = EmailClient(
                host=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_username,
                password=settings.smtp_password,
                from_email=settings.smtp_from_email,
                from_name=settings.smtp_from_name,
            )

    def _build_system_prompt(self) -> str:
        """Build the system prompt with available skills."""
        available_skills = self.skill_loader.generate_available_skills_xml()
        return SYSTEM_PROMPT_TEMPLATE.format(available_skills=available_skills)

    def _handle_tool_calls(self, response: ClaudeResponse) -> list[dict[str, str]]:
        """Handle tool calls from the model response."""
        results = []

        for tool_call in response.tool_calls:
            self.console.print(f"[dim]Executing tool: {tool_call.name}[/dim]")

            if tool_call.name == "send_email":
                result = self._handle_send_email(tool_call.input)
            else:
                result = self.skill_executor.execute_tool(tool_call.name, tool_call.input)

            results.append(
                {
                    "tool_use_id": tool_call.id,
                    "content": result,
                }
            )

        return results

    def _handle_send_email(self, tool_input: dict[str, Any]) -> str:
        """Handle the send_email tool call."""
        if not self.email_client:
            return "Error: Email is not configured. Please set SMTP settings in your environment."

        to_email = tool_input.get("to_email", "")
        to_name = tool_input.get("to_name", "")
        subject = tool_input.get("subject", "")
        body = tool_input.get("body", "")

        success, message = self.email_client.send_email(
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            body=body,
        )

        return message

    def chat(self, user_message: str) -> str:
        """Process a user message and return the response."""
        system_prompt = self._build_system_prompt()

        # Get initial response
        response = self.claude.chat(user_message, system_prompt)

        # Handle tool calls in a loop
        while response.tool_calls:
            tool_results = self._handle_tool_calls(response)
            response = self.claude.continue_with_tool_results(tool_results, system_prompt)

        return response.content

    def interactive_chat(self) -> None:
        """Run an interactive chat session."""
        self.console.print(
            Panel(
                "[bold green]SDR Agent[/bold green]\n"
                "AI-powered Sales Development Representative\n\n"
                "Type your message and press Enter. Type 'quit' or 'exit' to end.\n"
                "Type 'clear' to start a new conversation.",
                title="Welcome",
            )
        )

        # Show loaded skills
        skills = list(self.skill_loader._skills.values())
        if skills:
            skill_list = ", ".join(s.name for s in skills)
            self.console.print(f"[dim]Loaded skills: {skill_list}[/dim]\n")
        else:
            self.console.print("[yellow]No skills loaded. Check your skills directory.[/yellow]\n")

        while True:
            try:
                user_input = self.console.input("[bold blue]You:[/bold blue] ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ("quit", "exit"):
                    self.console.print("[dim]Goodbye![/dim]")
                    break

                if user_input.lower() == "clear":
                    self.claude.clear_conversation()
                    self.console.print("[dim]Conversation cleared.[/dim]\n")
                    continue

                # Get response
                with self.console.status("[bold green]Thinking...[/bold green]"):
                    response = self.chat(user_input)

                # Display response
                self.console.print()
                self.console.print("[bold green]Agent:[/bold green]")
                self.console.print(Markdown(response))
                self.console.print()

            except KeyboardInterrupt:
                self.console.print("\n[dim]Interrupted. Type 'quit' to exit.[/dim]")
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")

    def research_company(self, company_name: str) -> str:
        """Research a company and return a summary."""
        prompt = f"""Research the company "{company_name}" thoroughly.

Please find and summarize:
1. Company overview (what they do, industry, size)
2. Recent news and developments
3. Key products or services
4. Technology stack (if detectable)
5. Key decision makers (C-suite, VP-level)
6. Any recent funding or financial news

Provide a comprehensive research report that would help an SDR prepare for outreach."""

        return self.chat(prompt)

    def research_prospect(self, prospect_name: str, company: Optional[str] = None) -> str:
        """Research a prospect and return a summary."""
        company_context = f" at {company}" if company else ""
        prompt = f"""Research the prospect "{prospect_name}"{company_context} thoroughly.

Please find and summarize:
1. Current role and responsibilities
2. Professional background and experience
3. Education and certifications
4. Recent public activity (posts, articles, speaking)
5. Professional interests and focus areas
6. Any personal details that could help personalize outreach

Provide a comprehensive prospect profile that would help craft a personalized outreach message."""

        return self.chat(prompt)
