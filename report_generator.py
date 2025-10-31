"""
ROSHN PULSE Module 3: Automated Report Generator
=================================================
Generates clean, professional PDF reports from extracted data
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from schema import DailyLogExtraction


class ReportGenerator:
    """Generates PDF reports from extracted daily log data"""

    def __init__(self):
        """Initialize report generator with styles"""
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12
        )

        self.normal_style = self.styles['Normal']


    def generate_pdf(self, extraction: DailyLogExtraction, output_path: str) -> str:
        """
        Generate a PDF report from extraction results

        Args:
            extraction: DailyLogExtraction object with extracted data
            output_path: Path where PDF should be saved

        Returns:
            Path to generated PDF
        """

        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Container for PDF elements
        story = []

        # Add header
        story.extend(self._create_header(extraction))
        story.append(Spacer(1, 0.3 * inch))

        # Add summary section
        story.extend(self._create_summary(extraction))
        story.append(Spacer(1, 0.2 * inch))

        # Add completed tasks section
        story.extend(self._create_tasks_section(extraction))
        story.append(Spacer(1, 0.2 * inch))

        # Add blockers section
        if extraction.total_blockers > 0:
            story.extend(self._create_blockers_section(extraction))
            story.append(Spacer(1, 0.2 * inch))

        # Add incidents section
        if extraction.total_incidents > 0:
            story.extend(self._create_incidents_section(extraction))

        # Add footer
        story.append(Spacer(1, 0.3 * inch))
        story.extend(self._create_footer())

        # Build PDF
        doc.build(story)
        return output_path

    def _create_header(self, extraction: DailyLogExtraction) -> list:
        """Create report header"""
        elements = []

        # Title
        title = Paragraph("ROSHN PULSE - Daily Site Report", self.title_style)
        elements.append(title)

        # Metadata table
        data = [
            ['Site:', extraction.site_name or 'N/A'],
            ['Date:', str(extraction.log_date) if extraction.log_date else 'N/A'],
            ['Submitted By:', extraction.submitted_by or 'N/A'],
            ['Generated:', datetime.now().strftime('%d/%m/%Y %H:%M')],
        ]

        table = Table(data, colWidths=[2 * inch, 4 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)

        return elements

    def _create_summary(self, extraction: DailyLogExtraction) -> list:
        """Create summary statistics section"""
        elements = []

        # Section heading
        heading = Paragraph("Executive Summary", self.heading_style)
        elements.append(heading)

        # Summary data
        data = [
            ['Metric', 'Count', 'Status'],
            ['Completed Tasks', str(extraction.total_tasks_completed),
             self._get_status_indicator(extraction.total_tasks_completed, 'task')],
            ['Active Blockers', str(extraction.total_blockers),
             self._get_status_indicator(extraction.total_blockers, 'blocker')],
            ['Incidents Reported', str(extraction.total_incidents),
             self._get_status_indicator(extraction.total_incidents, 'incident')],
        ]

        table = Table(data, colWidths=[3 * inch, 1.5 * inch, 1.5 * inch])
        table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            # Data rows
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ]))
        elements.append(table)

        return elements

    def _create_tasks_section(self, extraction: DailyLogExtraction) -> list:
        """Create completed tasks section"""
        elements = []

        heading = Paragraph(f"Completed Tasks ({extraction.total_tasks_completed})", self.heading_style)
        elements.append(heading)

        if not extraction.completed_tasks:
            elements.append(Paragraph("No tasks completed.", self.normal_style))
            return elements

        # Create table data
        data = [['#', 'Task Description', 'Location', 'Crew']]

        # Create a smaller font style for table cells
        cell_style = ParagraphStyle('CellStyle', parent=self.normal_style, fontSize=9, leading=11)

        for i, task in enumerate(extraction.completed_tasks, 1):
            # Use Paragraph for task description to enable wrapping
            task_para = Paragraph(task.task_name[:200] + ('...' if len(task.task_name) > 200 else ''), cell_style)

            data.append([
                str(i),
                task_para,
                task.location or '-',
                task.crew or '-'
            ])

        # Adjusted column widths: wider Location and Crew columns
        table = Table(data, colWidths=[0.3 * inch, 3.4 * inch, 1.4 * inch, 1.4 * inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            # Data
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f1f8f4')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            # Enable word wrapping
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(table)

        return elements

    def _create_blockers_section(self, extraction: DailyLogExtraction) -> list:
        """Create blockers section"""
        elements = []

        heading = Paragraph(f"⚠ Active Blockers ({extraction.total_blockers})", self.heading_style)
        elements.append(heading)

        # Create table data
        data = [['#', 'Issue Description', 'Cause']]

        cell_style = ParagraphStyle('CellStyle', parent=self.normal_style, fontSize=9, leading=11)

        for i, blocker in enumerate(extraction.blockers, 1):
            issue_para = Paragraph(blocker.issue[:200] + ('...' if len(blocker.issue) > 200 else ''), cell_style)

            data.append([
                str(i),
                issue_para,
                blocker.cause or 'Unknown'
            ])

        table = Table(data, colWidths=[0.3 * inch, 4.4 * inch, 1.8 * inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            # Data
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef5e7')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(table)

        return elements

    def _create_incidents_section(self, extraction: DailyLogExtraction) -> list:
        """Create incidents section"""
        elements = []

        heading = Paragraph(f"⚠ Incidents ({extraction.total_incidents})", self.heading_style)
        elements.append(heading)

        # Create table data
        data = [['#', 'Type', 'Description', 'Severity']]

        cell_style = ParagraphStyle('CellStyle', parent=self.normal_style, fontSize=9, leading=11)

        for i, incident in enumerate(extraction.incidents, 1):
            desc_para = Paragraph(incident.description[:180] + ('...' if len(incident.description) > 180 else ''), cell_style)

            data.append([
                str(i),
                incident.incident_type.title(),
                desc_para,
                incident.severity or 'Unknown'
            ])

        table = Table(data, colWidths=[0.3 * inch, 0.9 * inch, 3.9 * inch, 1.4 * inch])
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            # Data
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fadbd8')]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        elements.append(table)

        return elements

    def _create_footer(self) -> list:
        """Create report footer"""
        elements = []

        footer_text = "Generated by ROSHN PULSE - AI-Powered Predictive Command Center | Module 3: Auto-Report Scribe"
        footer = Paragraph(f"<i>{footer_text}</i>", ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        ))
        elements.append(footer)

        return elements

    def _get_status_indicator(self, count: int, metric_type: str) -> str:
        """Get status indicator based on metric"""
        if metric_type == 'task':
            if count >= 5:
                return '✓ Good'
            elif count >= 2:
                return '○ Moderate'
            else:
                return '! Low'
        elif metric_type == 'blocker':
            if count == 0:
                return '✓ None'
            elif count <= 2:
                return '○ Manageable'
            else:
                return '! High'
        elif metric_type == 'incident':
            if count == 0:
                return '✓ None'
            elif count == 1:
                return '○ Minor'
            else:
                return '! Multiple'
        return '-'


def test_report_generator():
    """Test the report generator"""
    from extractor import DailyLogExtractor
    import os

    print("\n" + "=" * 80)
    print("TESTING PDF REPORT GENERATOR")
    print("=" * 80)

    # Create output directory
    os.makedirs("data/reports", exist_ok=True)

    # Load and extract from a sample log
    extractor = DailyLogExtractor()

    with open("data/sample_logs/log_001.txt", 'r', encoding='utf-8') as f:
        text = f.read()

    extraction = extractor.extract_from_text(text)

    # Generate PDF
    generator = ReportGenerator()
    output_path = "data/reports/test_report_001.pdf"
    generator.generate_pdf(extraction, output_path)

    print(f"\n[SUCCESS] PDF report generated: {output_path}")
    print(f"  - Tasks: {extraction.total_tasks_completed}")
    print(f"  - Blockers: {extraction.total_blockers}")
    print(f"  - Incidents: {extraction.total_incidents}")


if __name__ == "__main__":
    test_report_generator()
