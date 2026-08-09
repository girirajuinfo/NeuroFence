"""
pdf_generator.py

Generate a PDF security report for NeuroFence scans.
"""

from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


class PDFReportGenerator:
    """Generate a professional NeuroFence PDF security report."""

    def __init__(self, output_dir="reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate(self, metadata, risk_summary, prompt_count):
        """Generate and save a PDF security report."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        pdf_path = (
            self.output_dir
            / f"neurofence_security_report_{timestamp}.pdf"
        )

        document = SimpleDocTemplate(
            str(pdf_path),
            pagesize=A4,
            rightMargin=18 * mm,
            leftMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=22,
            spaceAfter=8,
        )

        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=18,
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceBefore=12,
            spaceAfter=8,
        )

        story = []

        # --------------------------------------------------
        # Title
        # --------------------------------------------------

        story.append(
            Paragraph(
                "NeuroFence Security Assessment Report",
                title_style,
            )
        )

        story.append(
            Paragraph(
                "LLM Weight Poisoning & Backdoor Scanner",
                subtitle_style,
            )
        )

        story.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                subtitle_style,
            )
        )

        # --------------------------------------------------
        # Model Information
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Model Information",
                heading_style,
            )
        )

        model_data = [
            ["Property", "Value"],
            [
                "Model Name",
                str(metadata.get("model_name", "Unknown")),
            ],
            [
                "Architecture",
                str(metadata.get("architecture", "Unknown")),
            ],
            [
                "Hidden Size",
                str(metadata.get("hidden_size", "Unknown")),
            ],
            [
                "Number of Layers",
                str(metadata.get("num_layers", "Unknown")),
            ],
            [
                "Vocabulary Size",
                str(metadata.get("vocab_size", "Unknown")),
            ],
            [
                "Total Parameters",
                f"{metadata.get('total_parameters', 'Unknown'):,}"
                if isinstance(
                    metadata.get("total_parameters"),
                    int,
                )
                else str(
                    metadata.get(
                        "total_parameters",
                        "Unknown",
                    )
                ),
            ],
        ]

        model_table = Table(
            model_data,
            colWidths=[65 * mm, 105 * mm],
        )

        model_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1f2937"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "MIDDLE",
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.whitesmoke,
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#f3f4f6"),
                        ],
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(model_table)
        story.append(Spacer(1, 10))

        # --------------------------------------------------
        # Scan Summary
        # --------------------------------------------------

        story.append(
            Paragraph(
                "Security Scan Summary",
                heading_style,
            )
        )

        scan_data = [
            ["Metric", "Result"],
            [
                "Risk Level",
                str(
                    risk_summary.get(
                        "risk_level",
                        "Unknown",
                    )
                ),
            ],
            [
                "Risk Score",
                str(
                    risk_summary.get(
                        "risk_score",
                        "Unknown",
                    )
                ),
            ],
            [
                "Total Spikes",
                str(
                    risk_summary.get(
                        "total_spikes",
                        0,
                    )
                ),
            ],
            [
                "Dormant Neurons",
                str(
                    risk_summary.get(
                        "total_dormant_neurons",
                        0,
                    )
                ),
            ],
            [
                "Prompts Analyzed",
                str(prompt_count),
            ],
        ]

        scan_table = Table(
            scan_data,
            colWidths=[65 * mm, 105 * mm],
        )

        scan_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#1f2937"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (-1, -1),
                        colors.white,
                    ),
                    (
                        "ROWBACKGROUNDS",
                        (0, 1),
                        (-1, -1),
                        [
                            colors.white,
                            colors.HexColor("#f3f4f6"),
                        ],
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        8,
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        6,
                    ),
                ]
            )
        )

        story.append(scan_table)
        story.append(Spacer(1, 15))

        # --------------------------------------------------
        # Conclusion
        # --------------------------------------------------

        risk_level = str(
            risk_summary.get(
                "risk_level",
                "Unknown",
            )
        )

        story.append(
            Paragraph(
                f"Assessment Result: <b>{risk_level}</b>",
                heading_style,
            )
        )

        story.append(
            Paragraph(
                "This report summarizes the activation analysis "
                "performed by NeuroFence. The assessment is based "
                "on the captured model activation statistics and "
                "the configured risk scoring engine.",
                styles["BodyText"],
            )
        )

        story.append(Spacer(1, 20))

        story.append(
            Paragraph(
                "Generated by NeuroFence",
                subtitle_style,
            )
        )

        document.build(story)

        return str(pdf_path)
