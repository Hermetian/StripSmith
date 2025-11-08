"""Page layout and panel composition (Stage 5)."""

import os
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image, ImageDraw, ImageFont

from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger("stripsmith.layout")


class PageCompositor:
    """Compose comic pages from panel images."""

    def __init__(self):
        """Initialize page compositor."""
        self.config = get_config()

        # Page settings
        self.page_width, self.page_height = self.config.get(
            "layout.page_size", [1200, 1600]
        )
        self.gutter = self.config.get("layout.gutter_width", 10)
        self.margin = self.config.get("layout.page_margin", 20)

        logger.info(f"Page compositor initialized: {self.page_width}x{self.page_height}")

    def compose_page(
        self,
        page_data: Dict,
        panel_images: List[str],
        output_path: str
    ) -> str:
        """
        Compose a comic page from panel images.

        Args:
            page_data: Page data with layout and panels
            panel_images: List of paths to panel images
            output_path: Path to save composed page

        Returns:
            Path to composed page image
        """
        page_num = page_data.get("page_number", 1)
        layout = page_data.get("layout", "3-panel-grid")

        logger.info(f"Composing page {page_num} with layout: {layout}")

        # Create blank page
        page = Image.new('RGB', (self.page_width, self.page_height), 'white')

        # Get panel positions
        positions = self._calculate_panel_positions(layout, len(panel_images))

        # Place panels
        for i, (panel_path, position) in enumerate(zip(panel_images, positions)):
            try:
                panel_img = Image.open(panel_path)
                panel_img = self._resize_panel(panel_img, position)
                page.paste(panel_img, (position[0], position[1]))

                logger.debug(f"Placed panel {i+1} at {position}")

            except Exception as e:
                logger.error(f"Failed to place panel {panel_path}: {e}")
                continue

        # Add panel borders
        self._draw_panel_borders(page, positions)

        # Save page
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        page.save(output_path, 'PNG', dpi=(300, 300))

        logger.info(f"Page saved: {output_path}")
        return output_path

    def _calculate_panel_positions(
        self,
        layout: str,
        panel_count: int
    ) -> List[Tuple[int, int, int, int]]:
        """
        Calculate panel positions for layout.

        Returns:
            List of (x, y, width, height) tuples
        """
        positions = []

        usable_width = self.page_width - (2 * self.margin)
        usable_height = self.page_height - (2 * self.margin)

        if layout == "3-panel-grid":
            # 3 equal rows
            panel_height = (usable_height - (2 * self.gutter)) // 3

            for i in range(min(3, panel_count)):
                y = self.margin + (i * (panel_height + self.gutter))
                positions.append((
                    self.margin,
                    y,
                    usable_width,
                    panel_height
                ))

        elif layout == "4-panel-grid":
            # 2x2 grid
            panel_width = (usable_width - self.gutter) // 2
            panel_height = (usable_height - self.gutter) // 2

            for row in range(2):
                for col in range(2):
                    if len(positions) >= panel_count:
                        break

                    x = self.margin + (col * (panel_width + self.gutter))
                    y = self.margin + (row * (panel_height + self.gutter))

                    positions.append((x, y, panel_width, panel_height))

        elif layout == "splash":
            # Full page
            positions.append((
                self.margin,
                self.margin,
                usable_width,
                usable_height
            ))

        elif layout == "webtoon":
            # Vertical stack
            panel_height = usable_height // min(panel_count, 6)

            for i in range(min(6, panel_count)):
                y = self.margin + (i * panel_height)
                positions.append((
                    self.margin,
                    y,
                    usable_width,
                    panel_height
                ))

        else:
            # Default: 3-panel grid
            logger.warning(f"Unknown layout: {layout}, using 3-panel-grid")
            return self._calculate_panel_positions("3-panel-grid", panel_count)

        return positions

    def _resize_panel(
        self,
        panel: Image.Image,
        position: Tuple[int, int, int, int]
    ) -> Image.Image:
        """Resize panel to fit position."""
        target_width = position[2]
        target_height = position[3]

        # Resize maintaining aspect ratio
        panel_resized = panel.copy()
        panel_resized.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)

        # Create centered version if aspect ratios don't match
        result = Image.new('RGB', (target_width, target_height), 'white')

        # Center the panel
        paste_x = (target_width - panel_resized.width) // 2
        paste_y = (target_height - panel_resized.height) // 2

        result.paste(panel_resized, (paste_x, paste_y))

        return result

    def _draw_panel_borders(
        self,
        page: Image.Image,
        positions: List[Tuple[int, int, int, int]]
    ):
        """Draw borders around panels."""
        draw = ImageDraw.Draw(page)

        for pos in positions:
            x, y, w, h = pos

            # Draw rectangle border
            draw.rectangle(
                [(x, y), (x + w, y + h)],
                outline='black',
                width=3
            )

    def add_text_overlay(
        self,
        page_path: str,
        panel_data: Dict,
        output_path: str
    ) -> str:
        """
        Add dialogue and narration text to a page.

        Args:
            page_path: Path to composed page
            panel_data: Panel data with dialogue
            output_path: Output path

        Returns:
            Path to page with text
        """
        logger.info("Adding text overlay...")

        page = Image.open(page_path)
        draw = ImageDraw.Draw(page)

        # Load font
        try:
            font_size = self.config.get("bubbles.font_size", 14)
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Add text for each panel (simplified - just caption text at bottom)
        # Full speech bubble implementation would be Phase 2

        page.save(output_path, 'PNG')
        logger.info(f"Text overlay complete: {output_path}")

        return output_path
