from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.enums import TA_CENTER


def generate_pdf(candidate, role, total_score, average, recommendation, evaluations):

    filename = "Interview_Report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story = []

    story.append(Paragraph("AI Interview Report", title))
    story.append(Paragraph("<br/><br/>", styles["BodyText"]))

    story.append(Paragraph(f"<b>Candidate:</b> {candidate}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Job Role:</b> {role}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Final Score:</b> {total_score}/50", styles["BodyText"]))
    story.append(Paragraph(f"<b>Average Score:</b> {average:.1f}/10", styles["BodyText"]))
    story.append(Paragraph(f"<b>Recommendation:</b> {recommendation}", styles["BodyText"]))

    story.append(Paragraph("<br/><br/>", styles["BodyText"]))

    for i, item in enumerate(evaluations):

        story.append(
            Paragraph(
                f"<b>Question {i+1}</b> - Score: {item['score']}/10",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Feedback:</b> {item['feedback']}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Expected Answer:</b> {item['expected_answer']}",
                styles["BodyText"]
            )
        )

        story.append(Paragraph("<br/>", styles["BodyText"]))

    doc.build(story)

    return filename