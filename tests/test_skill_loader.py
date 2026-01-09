"""Tests for the skill loader module."""

import pytest

from sdr_agent.skills.loader import Skill, SkillLoader, SkillMetadata


@pytest.fixture
def skill_content():
    """Sample SKILL.md content."""
    return """---
name: test-skill
description: A test skill for unit testing
license: MIT
metadata:
  author: test
  version: "1.0"
---

# Test Skill

This is the instruction content.

## Section 1

Some instructions here.
"""


@pytest.fixture
def skill_dir(tmp_path, skill_content):
    """Create a temporary skill directory."""
    skill_path = tmp_path / "test-skill"
    skill_path.mkdir()
    (skill_path / "SKILL.md").write_text(skill_content)
    return tmp_path


class TestSkillLoader:
    """Tests for SkillLoader class."""

    def test_init(self, tmp_path):
        """Test SkillLoader initialization."""
        loader = SkillLoader(tmp_path)
        assert loader.skills_dir == tmp_path
        assert loader._skills == {}

    def test_discover_skills_empty_dir(self, tmp_path):
        """Test discovering skills in empty directory."""
        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_discover_skills_nonexistent_dir(self, tmp_path):
        """Test discovering skills in nonexistent directory."""
        loader = SkillLoader(tmp_path / "nonexistent")
        skills = loader.discover_skills()
        assert skills == []

    def test_discover_skills(self, skill_dir):
        """Test discovering skills."""
        loader = SkillLoader(skill_dir)
        skills = loader.discover_skills()

        assert len(skills) == 1
        assert skills[0].name == "test-skill"
        assert skills[0].description == "A test skill for unit testing"

    def test_discover_skills_skips_files(self, tmp_path):
        """Test that discover_skills skips non-directory entries."""
        (tmp_path / "not-a-skill.txt").write_text("just a file")
        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_discover_skills_skips_dirs_without_skill_md(self, tmp_path):
        """Test that discover_skills skips directories without SKILL.md."""
        (tmp_path / "empty-skill").mkdir()
        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_get_skill(self, skill_dir):
        """Test getting a skill by name."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        skill = loader.get_skill("test-skill")
        assert skill is not None
        assert skill.name == "test-skill"

    def test_get_skill_not_found(self, skill_dir):
        """Test getting a nonexistent skill."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        skill = loader.get_skill("nonexistent")
        assert skill is None

    def test_load_skill_instructions(self, skill_dir):
        """Test loading skill instructions."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        instructions = loader.load_skill_instructions("test-skill")
        assert instructions is not None
        assert "# Test Skill" in instructions
        assert "This is the instruction content." in instructions

    def test_load_skill_instructions_not_found(self, skill_dir):
        """Test loading instructions for nonexistent skill."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        instructions = loader.load_skill_instructions("nonexistent")
        assert instructions is None

    def test_generate_available_skills_xml(self, skill_dir):
        """Test generating XML for available skills."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        xml = loader.generate_available_skills_xml()
        assert "<available_skills>" in xml
        assert "</available_skills>" in xml
        assert "<name>test-skill</name>" in xml
        assert "<description>A test skill for unit testing</description>" in xml

    def test_generate_available_skills_xml_empty(self, tmp_path):
        """Test generating XML when no skills available."""
        loader = SkillLoader(tmp_path)
        xml = loader.generate_available_skills_xml()
        assert xml == "<available_skills>\n</available_skills>"

    def test_load_reference(self, skill_dir):
        """Test loading a reference file."""
        # Create a reference file
        skill_path = skill_dir / "test-skill"
        refs_dir = skill_path / "references"
        refs_dir.mkdir()
        (refs_dir / "guide.md").write_text("# Reference Guide\n\nSome content.")

        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        content = loader.load_reference("test-skill", "guide.md")
        assert content is not None
        assert "# Reference Guide" in content

    def test_load_reference_skill_not_found(self, skill_dir):
        """Test loading reference for nonexistent skill."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        content = loader.load_reference("nonexistent", "guide.md")
        assert content is None

    def test_load_reference_file_not_found(self, skill_dir):
        """Test loading nonexistent reference file."""
        loader = SkillLoader(skill_dir)
        loader.discover_skills()

        content = loader.load_reference("test-skill", "nonexistent.md")
        assert content is None


class TestSkillParsing:
    """Tests for skill parsing edge cases."""

    def test_invalid_frontmatter(self, tmp_path):
        """Test loading skill with invalid YAML frontmatter."""
        skill_path = tmp_path / "bad-skill"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: [invalid yaml
---

Content here.
""")

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_missing_name(self, tmp_path):
        """Test loading skill without name field."""
        skill_path = tmp_path / "no-name"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
description: Missing name field
---

Content here.
""")

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_missing_description(self, tmp_path):
        """Test loading skill without description field."""
        skill_path = tmp_path / "no-desc"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: no-desc
---

Content here.
""")

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_no_frontmatter(self, tmp_path):
        """Test loading skill without frontmatter."""
        skill_path = tmp_path / "no-frontmatter"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("# Just content\n\nNo frontmatter.")

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()
        assert skills == []

    def test_minimal_valid_skill(self, tmp_path):
        """Test loading skill with minimal required fields."""
        skill_path = tmp_path / "minimal"
        skill_path.mkdir()
        (skill_path / "SKILL.md").write_text("""---
name: minimal
description: Minimal skill
---

Instructions.
""")

        loader = SkillLoader(tmp_path)
        skills = loader.discover_skills()

        assert len(skills) == 1
        assert skills[0].name == "minimal"
        assert skills[0].metadata.license is None


class TestSkillModel:
    """Tests for Skill model."""

    def test_skill_directories(self, tmp_path):
        """Test Skill directory properties."""
        metadata = SkillMetadata(name="test", description="Test skill")
        skill = Skill(
            name="test",
            description="Test skill",
            path=tmp_path / "test-skill",
            metadata=metadata,
        )

        assert skill.scripts_dir == tmp_path / "test-skill" / "scripts"
        assert skill.references_dir == tmp_path / "test-skill" / "references"
        assert skill.assets_dir == tmp_path / "test-skill" / "assets"
