"""Export comic pages to various formats."""

import os
from pathlib import Path
from typing import List
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger("stripsmith.export")


class ComicExporter:
    """Export comic pages to PDF, PNG, or CBZ format."""

    def __init__(self):
        """Initialize exporter."""
        self.config = get_config()
        logger.info("Comic exporter initialized")

    def export_to_pdf(
        self,
        page_images: List[str],
        output_path: str,
        title: str = "Comic"
    ) -> str:
        """
        Export comic pages to PDF.

        Args:
            page_images: List of paths to page images
            output_path: Output PDF path
            title: Comic title for metadata

        Returns:
            Path to generated PDF
        """
        logger.info(f"Exporting {len(page_images)} pages to PDF...")

        try:
            # Create PDF
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            c = canvas.Canvas(output_path, pagesize=letter)

            # Set metadata
            c.setTitle(title)
            c.setAuthor("Stripsmith")

            # Add each page
            for i, img_path in enumerate(page_images):
                logger.debug(f"Adding page {i+1}/{len(page_images)}")

                # Open image
                img = Image.open(img_path)

                # Get dimensions
                img_width, img_height = img.size

                # Calculate scaling to fit page
                page_width, page_height = letter
                scale = min(page_width / img_width, page_height / img_height)

                scaled_width = img_width * scale
                scaled_height = img_height * scale

                # Center on page
                x = (page_width - scaled_width) / 2
                y = (page_height - scaled_height) / 2

                # Add image
                c.drawImage(
                    img_path,
                    x, y,
                    width=scaled_width,
                    height=scaled_height,
                    preserveAspectRatio=True
                )

                # New page for next image
                if i < len(page_images) - 1:
                    c.showPage()

            # Save PDF
            c.save()

            logger.info(f"PDF exported: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"PDF export failed: {e}")
            raise

    def export_to_images(
        self,
        page_images: List[str],
        output_dir: str,
        prefix: str = "page"
    ) -> List[str]:
        """
        Copy page images to output directory.

        Args:
            page_images: List of page image paths
            output_dir: Output directory
            prefix: Filename prefix

        Returns:
            List of output paths
        """
        logger.info(f"Exporting {len(page_images)} pages to {output_dir}...")

        try:
            os.makedirs(output_dir, exist_ok=True)

            output_paths = []

            for i, img_path in enumerate(page_images):
                # Create output filename
                output_filename = f"{prefix}_{i+1:03d}.png"
                output_path = os.path.join(output_dir, output_filename)

                # Copy image
                img = Image.open(img_path)
                img.save(output_path, 'PNG')

                output_paths.append(output_path)

                logger.debug(f"Exported: {output_filename}")

            logger.info(f"Images exported to: {output_dir}")
            return output_paths

        except Exception as e:
            logger.error(f"Image export failed: {e}")
            raise

    def export_to_cbz(
        self,
        page_images: List[str],
        output_path: str
    ) -> str:
        """
        Export to CBZ (Comic Book ZIP) format.

        Args:
            page_images: List of page image paths
            output_path: Output CBZ path

        Returns:
            Path to generated CBZ
        """
        import zipfile

        logger.info(f"Exporting {len(page_images)} pages to CBZ...")

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as cbz:
                for i, img_path in enumerate(page_images):
                    # Add with sequential filename
                    arcname = f"page_{i+1:03d}.png"
                    cbz.write(img_path, arcname)

                    logger.debug(f"Added: {arcname}")

            logger.info(f"CBZ exported: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"CBZ export failed: {e}")
            raise
