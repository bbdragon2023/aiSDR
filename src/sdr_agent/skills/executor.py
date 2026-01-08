"""Skill executor for running skill scripts and handling tool calls."""

import subprocess
import sys
from pathlib import Path
from typing import Any, Optional

from tavily import TavilyClient

from .loader import Skill, SkillLoader


class SkillExecutor:
    """Executor for Agent Skills."""

    def __init__(
        self,
        skill_loader: SkillLoader,
        tavily_api_key: Optional[str] = None,
    ):
        self.skill_loader = skill_loader
        self.tavily_client = TavilyClient(api_key=tavily_api_key) if tavily_api_key else None

    def execute_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        """Execute a tool and return the result."""
        if tool_name == "web_search":
            return self._execute_web_search(tool_input)
        elif tool_name == "read_skill":
            return self._execute_read_skill(tool_input)
        else:
            return f"Unknown tool: {tool_name}"

    def _execute_web_search(self, tool_input: dict[str, Any]) -> str:
        """Execute a web search using Tavily."""
        query = tool_input.get("query", "")
        max_results = tool_input.get("max_results", 5)

        if not self.tavily_client:
            return "Error: Tavily API key not configured. Please set TAVILY_API_KEY in your environment."

        try:
            response = self.tavily_client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
            )

            # Format the results
            results = []

            if response.get("answer"):
                results.append(f"Summary: {response['answer']}\n")

            results.append("Search Results:")
            for i, result in enumerate(response.get("results", []), 1):
                results.append(f"\n{i}. {result.get('title', 'No title')}")
                results.append(f"   URL: {result.get('url', 'N/A')}")
                results.append(f"   {result.get('content', 'No content')[:500]}")

            return "\n".join(results)

        except Exception as e:
            return f"Search error: {str(e)}"

    def _execute_read_skill(self, tool_input: dict[str, Any]) -> str:
        """Load and return skill instructions."""
        skill_name = tool_input.get("skill_name", "")

        skill = self.skill_loader.get_skill(skill_name)
        if not skill:
            available = ", ".join(s.name for s in self.skill_loader._skills.values())
            return f"Skill '{skill_name}' not found. Available skills: {available}"

        return f"# {skill.name}\n\n{skill.instructions}"

    def run_skill_script(
        self,
        skill: Skill,
        script_name: str,
        args: list[str] = None,
    ) -> tuple[bool, str]:
        """Run a script from a skill's scripts directory."""
        script_path = skill.scripts_dir / script_name

        if not script_path.exists():
            return False, f"Script not found: {script_name}"

        args = args or []

        try:
            # Determine how to run the script based on extension
            if script_path.suffix == ".py":
                cmd = [sys.executable, str(script_path)] + args
            elif script_path.suffix == ".sh":
                cmd = ["bash", str(script_path)] + args
            else:
                # Try to run directly (assumes executable)
                cmd = [str(script_path)] + args

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=skill.path,
            )

            output = result.stdout
            if result.stderr:
                output += f"\nStderr: {result.stderr}"

            return result.returncode == 0, output

        except subprocess.TimeoutExpired:
            return False, "Script execution timed out"
        except Exception as e:
            return False, f"Script execution error: {str(e)}"

    def get_skill_reference(self, skill_name: str, reference_name: str) -> Optional[str]:
        """Get a reference document from a skill."""
        return self.skill_loader.load_reference(skill_name, reference_name)
