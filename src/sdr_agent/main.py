"""CLI entry point for SDR Agent."""

import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from .agent import SDRAgent
from .config import Settings, get_settings


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="sdr-agent",
        description="AI-powered Sales Development Representative agent",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Chat command
    subparsers.add_parser("chat", help="Start interactive chat session")

    # Research command
    research_parser = subparsers.add_parser("research", help="Research a company or prospect")
    research_parser.add_argument("--company", "-c", help="Company name to research")
    research_parser.add_argument("--prospect", "-p", help="Prospect name to research")

    # Skills command
    subparsers.add_parser("skills", help="List available skills")

    # Version command
    subparsers.add_parser("version", help="Show version")

    return parser


def cmd_chat(settings: Settings, console: Console) -> int:
    """Run interactive chat mode."""
    try:
        agent = SDRAgent(settings)
        agent.interactive_chat()
        return 0
    except KeyboardInterrupt:
        console.print("\n[dim]Goodbye![/dim]")
        return 0
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


def cmd_research(
    settings: Settings,
    console: Console,
    company: str | None,
    prospect: str | None,
) -> int:
    """Run research command."""
    if not company and not prospect:
        console.print("[red]Error: Please specify --company or --prospect[/red]")
        return 1

    try:
        agent = SDRAgent(settings)

        with console.status("[bold green]Researching...[/bold green]"):
            if prospect:
                result = agent.research_prospect(prospect, company)
            else:
                result = agent.research_company(company)

        console.print()
        console.print(Markdown(result))
        return 0

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return 1


def cmd_skills(console: Console, skills_dir: str = "./skills") -> int:
    """List available skills."""
    from pathlib import Path

    from .skills.loader import SkillLoader

    loader = SkillLoader(Path(skills_dir))
    skills = loader.discover_skills()

    if not skills:
        console.print("[yellow]No skills found.[/yellow]")
        console.print(f"[dim]Skills directory: {skills_dir}[/dim]")
        return 0

    console.print(Panel("[bold]Available Skills[/bold]", expand=False))
    console.print()

    for skill in skills:
        console.print(f"[bold cyan]{skill.name}[/bold cyan]")
        console.print(f"  {skill.description}")
        console.print(f"  [dim]Path: {skill.path}[/dim]")
        console.print()

    return 0


def cmd_version(console: Console) -> int:
    """Show version."""
    from . import __version__

    console.print(f"sdr-agent version {__version__}")
    return 0


def main() -> int:
    """Main entry point."""
    console = Console()
    parser = create_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "version":
        return cmd_version(console)

    # Skills command doesn't need API keys
    if args.command == "skills":
        return cmd_skills(console)

    # Load settings for commands that need API keys
    try:
        settings = get_settings()
    except Exception as e:
        console.print(f"[red]Configuration error: {e}[/red]")
        console.print("[dim]Make sure you have a .env file with required settings.[/dim]")
        console.print("[dim]See .env.example for required variables.[/dim]")
        return 1

    if args.command == "chat":
        return cmd_chat(settings, console)
    elif args.command == "research":
        return cmd_research(settings, console, args.company, args.prospect)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
