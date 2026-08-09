"""
pdf_generator.py

Generate a professional PDF report for NeuroFence.
"""

from datetime import datetime
from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from utils import logger


class PDFReportGenerator:
    """
    Generate a PDF scan report.
    """

    def generate(
        self,
        metadata,
        risk_summary,
        prompt_count,
        output_path="reports/NeuroFence_Report.pdf"
    ):
        """
        Generate the PDF report.

        Returns:
            str: Path to the generated PDF.
        """

        output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        document = SimpleDocTemplate(str(output_path))

        styles = getSampleStyleSheet()

        elements = []

        # Title

        elements.append(
            Paragraph(
                "<b>NeuroFence Security Scan Report</b>",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        # Project

        elements.append(
            Paragraph(
                "<b>Project Name:</b> NeuroFence",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Scan Date:</b> {datetime.now()}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 15))

        # Model Information

        elements.append(
            Paragraph("<b>Model Information</b>", styles["Heading2"])
        )

        for key, value in metadata.items():
            elements.append(
                Paragraph(
                    f"{key}: {value}",
                    styles["BodyText"]
                )
            )

        elements.append(Spacer(1, 15))

        # Risk

        elements.append(
            Paragraph("<b>Risk Assessment</b>", styles["Heading2"])
        )

        for key, value in risk_summary.items():
            elements.append(
                Paragraph(
                    f"{key}: {value}",
                    styles["BodyText"]
                )
            )

        elements.append(Spacer(1, 15))

        # Prompt statistics

        elements.append(
            Paragraph("<b>Prompt Statistics</b>", styles["Heading2"])
        )

        elements.append(
            Paragraph(
                f"Total Prompts Processed: {prompt_count}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 15))

        verdict = risk_summary["risk_level"]

        elements.append(
            Paragraph(
                f"<b>Final Verdict:</b> {verdict}",
                styles["Heading2"]
            )
        )

        document.build(elements)

        logger.success(
            f"PDF report generated: {output_path}"
        )

        return str(output_path)