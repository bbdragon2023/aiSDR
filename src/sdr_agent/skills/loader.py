"""Skill loader for discovering and parsing Agent Skills."""

import re
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class SkillMetadata(BaseModel):
    """Metadata from SKILL.md frontmatter."""

    name: str
    description: str
    license: Optional[str] = None
    compatibility: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
    allowed_tools: Optional[str] = None


class Skill(BaseModel):
    """A loaded Agent Skill."""

    name: str
    description: str
    path: Path
    instructions: str = ""
    metadata: SkillMetadata

    @property
    def scripts_dir(self) -> Path:
        """Path to the skill's scripts directory."""
        return self.path / "scripts"

    @property
    def references_dir(self) -> Path:
        """Path to the skill's references directory."""
        return self.path / "references"

    @property
    def assets_dir(self) -> Path:
        """Path to the skill's assets directory."""
        return self.path / "assets"


class SkillLoader:
    """Loader for discovering and parsing Agent Skills."""

    FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)
        self._skills: dict[str, Skill] = {}

    def discover_skills(self) -> list[Skill]:
        """Discover all skills in the skills directory."""
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_path in self.skills_dir.iterdir():
            if not skill_path.is_dir():
                continue

            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            skill = self._load_skill(skill_path)
            if skill:
                skills.append(skill)
                self._skills[skill.name] = skill

        return skills

    def _load_skill(self, skill_path: Path) -> Optional[Skill]:
        """Load a skill from its directory."""
        skill_md = skill_path / "SKILL.md"

        try:
            content = skill_md.read_text()
        except Exception:
            return None

        # Parse frontmatter
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return None

        try:
            frontmatter = yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None

        if not frontmatter or "name" not in frontmatter or "description" not in frontmatter:
            return None

        # Extract body (instructions after frontmatter)
        instructions = content[match.end() :].strip()

        metadata = SkillMetadata(
            name=frontmatter["name"],
            description=frontmatter["description"],
            license=frontmatter.get("license"),
            compatibility=frontmatter.get("compatibility"),
            metadata=frontmatter.get("metadata", {}),
            allowed_tools=frontmatter.get("allowed-tools"),
        )

        return Skill(
            name=metadata.name,
            description=metadata.description,
            path=skill_path,
            instructions=instructions,
            metadata=metadata,
        )

    def get_skill(self, name: str) -> Optional[Skill]:
        """Get a skill by name."""
        return self._skills.get(name)

    def load_skill_instructions(self, name: str) -> Optional[str]:
        """Load full instructions for a skill."""
        skill = self.get_skill(name)
        if skill:
            return skill.instructions
        return None

    def generate_available_skills_xml(self) -> str:
        """Generate XML listing of available skills for system prompt."""
        if not self._skills:
            self.discover_skills()

        lines = ["<available_skills>"]
        for skill in self._skills.values():
            lines.append("  <skill>")
            lines.append(f"    <name>{skill.name}</name>")
            lines.append(f"    <description>{skill.description}</description>")
            lines.append(f"    <location>{skill.path.absolute()}/SKILL.md</location>")
            lines.append("  </skill>")
        lines.append("</available_skills>")

        return "\n".join(lines)

    def load_reference(self, skill_name: str, reference_name: str) -> Optional[str]:
        """Load a reference file from a skill."""
        skill = self.get_skill(skill_name)
        if not skill:
            return None

        ref_path = skill.references_dir / reference_name
        if ref_path.exists():
            return ref_path.read_text()
        return None
