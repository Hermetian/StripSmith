"""Character prompt template management for consistency."""

from typing import Dict, List
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger("stripsmith.templates")


class CharacterTemplateManager:
    """Manage character prompt templates for consistent generation."""

    def __init__(self):
        """Initialize template manager."""
        self.config = get_config()
        self.templates = {}

    def create_template(self, character: Dict, style: Dict) -> str:
        """
        Create a prompt template for a character.

        Args:
            character: Character data from project spec
            style: Style data from project spec

        Returns:
            Complete prompt string for DALL-E 3
        """
        template_format = self.config.get(
            "characters.template",
            "{style}, {name}, {age}, {gender}, {physical_features}, {clothing}, {accessories}"
        )

        # Build template data
        template_data = {
            "style": style.get("art_style", "comic book art"),
            "name": character.get("name", "character"),
            "age": character.get("age", "adult"),
            "gender": character.get("gender", ""),
            "physical_features": character.get("physical_features", ""),
            "clothing": character.get("clothing", "casual clothing"),
            "accessories": character.get("accessories", ""),
            "mood": style.get("mood", ""),
            "era": style.get("era", "")
        }

        # Format template
        prompt = template_format.format(**template_data)

        # Clean up empty fields
        prompt = " ".join(prompt.split())  # Remove extra spaces

        # Store template
        self.templates[character["name"]] = {
            "base_prompt": prompt,
            "template_data": template_data,
            "negative_prompt": self.config.get("characters.negative", "")
        }

        logger.debug(f"Created template for {character['name']}: {prompt[:100]}...")

        return prompt

    def get_character_prompt(
        self,
        character_name: str,
        angle: str = "front",
        shot_type: str = "medium-shot",
        action: str = ""
    ) -> str:
        """
        Get a complete prompt for a specific character view.

        Args:
            character_name: Character name
            angle: View angle (front, 3/4, profile, back)
            shot_type: Shot type (close-up, medium-shot, full-body)
            action: Optional action description

        Returns:
            Complete prompt string
        """
        if character_name not in self.templates:
            raise ValueError(f"No template found for character: {character_name}")

        template = self.templates[character_name]
        base = template["base_prompt"]

        # Add angle and shot type
        angle_desc = self._get_angle_description(angle)
        shot_desc = self._get_shot_description(shot_type)

        # Build complete prompt
        parts = [base, angle_desc, shot_desc]

        if action:
            parts.append(action)

        prompt = ", ".join(parts)

        return prompt

    def _get_angle_description(self, angle: str) -> str:
        """Get description for camera angle."""
        angles = {
            "front": "facing forward, front view",
            "3/4": "three-quarter view, slight angle",
            "profile": "side profile, 90 degree angle",
            "back": "back view, facing away",
            "overhead": "overhead view, bird's eye"
        }
        return angles.get(angle, "front view")

    def _get_shot_description(self, shot_type: str) -> str:
        """Get description for shot type."""
        shots = {
            "extreme-close-up": "extreme close-up shot, face detail",
            "close-up": "close-up shot, head and shoulders",
            "medium-shot": "medium shot, waist up",
            "full-body": "full body shot, head to toe",
            "long-shot": "long shot, full figure with environment"
        }
        return shots.get(shot_type, "medium shot")

    def create_character_sheet_prompts(
        self,
        character_name: str,
        angles: List[str] = None
    ) -> List[Dict[str, str]]:
        """
        Create prompts for a character reference sheet.

        Args:
            character_name: Character name
            angles: List of angles to generate (default: front, 3/4, profile)

        Returns:
            List of prompt dicts with angle and prompt
        """
        if angles is None:
            angles = ["front", "3/4", "profile"]

        prompts = []

        for angle in angles:
            prompt = self.get_character_prompt(
                character_name=character_name,
                angle=angle,
                shot_type="full-body",
                action="character reference sheet, neutral expression, clean background"
            )

            prompts.append({
                "angle": angle,
                "prompt": prompt,
                "character": character_name
            })

        logger.info(f"Created {len(prompts)} reference sheet prompts for {character_name}")

        return prompts

    def get_negative_prompt(self, character_name: str = None) -> str:
        """
        Get negative prompt for character generation.

        Args:
            character_name: Optional specific character

        Returns:
            Negative prompt string
        """
        if character_name and character_name in self.templates:
            return self.templates[character_name]["negative_prompt"]

        return self.config.get(
            "characters.negative",
            "multiple people, crowd, anime, realistic photo, 3d render, blurry"
        )

    def create_all_templates(self, project_spec: Dict) -> Dict[str, str]:
        """
        Create templates for all characters in project spec.

        Args:
            project_spec: Project specification with characters and style

        Returns:
            Dict mapping character names to base prompts
        """
        characters = project_spec.get("characters", [])
        style = project_spec.get("style", {})

        all_templates = {}

        for character in characters:
            name = character["name"]
            prompt = self.create_template(character, style)
            all_templates[name] = prompt

        logger.info(f"Created templates for {len(all_templates)} characters")

        return all_templates
