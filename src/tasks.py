from pathlib import Path
from crewai import Task


# =========================================================
# PROJECT PATHS
# =========================================================

# tasks.py is located inside:
# deep-research-agent/src/tasks.py
#
# Therefore:
# parent        = src
# parent.parent = deep-research-agent

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_MD = OUTPUT_DIR / "report.md"
REPORT_PDF = OUTPUT_DIR / "report.pdf"

# Make sure the output directory exists
OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =========================================================
# RESEARCH / ANALYSIS / WRITING TASKS
# =========================================================

def create_tasks(
    researcher,
    analyst,
    writer,
):

    # -----------------------------------------------------
    # TASK 1 - RESEARCH
    # -----------------------------------------------------

    research_task = Task(
        description=(
            "Research {topic} thoroughly. "
            "Find at least 5 key facts supported by reliable sources. "
            "Use recent information whenever possible. "
            "Include important statistics, market trends, organizations, "
            "and other relevant data. "
            "Identify the source for important factual claims."
        ),

        expected_output=(
            "A research brief containing 5-7 key findings with relevant "
            "data points, source names, source types, and URLs when available. "
            "Keep the research brief under 500 words."
        ),

        agent=researcher,
    )

    # -----------------------------------------------------
    # TASK 2 - ANALYSIS
    # -----------------------------------------------------

    analysis_task = Task(
        description=(
            "Analyze the research findings about {topic}. "
            "Evaluate the market trends and evidence collected by the "
            "researcher. "
            "Identify exactly 3 major opportunities, "
            "2 significant challenges, and "
            "1 actionable strategic recommendation. "
            "Base the analysis on the research provided."
        ),

        expected_output=(
            "A structured market analysis containing exactly "
            "3 major opportunities, "
            "2 significant challenges, and "
            "1 actionable strategic recommendation."
        ),

        agent=analyst,

        context=[
            research_task,
        ],
    )

    # -----------------------------------------------------
    # TASK 3 - PROFESSIONAL REPORT
    # -----------------------------------------------------

    writing_task = Task(
        description=(
            "Create a professional executive-level report about {topic}. "
            "Combine the research findings and industry analysis into "
            "a clear and well-structured report. "
            "Include the following sections: "
            "title, executive summary, key findings, opportunities, "
            "challenges, strategic recommendation, conclusion, and sources. "
            "Write the report in clean Markdown format. "
            "Preserve useful source names and URLs from the research. "
            "Do not attempt to create a PDF. "
            "The application will convert the Markdown report into PDF "
            "after this task is completed."
        ),

        expected_output=(
            "A polished executive-level Markdown report containing "
            "a title, executive summary, key findings, "
            "3 opportunities, 2 challenges, "
            "1 strategic recommendation, conclusion, and sources. "
            "The report should be professionally written and ready "
            "for conversion into PDF."
        ),

        agent=writer,

        context=[
            research_task,
            analysis_task,
        ],

        # IMPORTANT:
        # CrewAI writes the report as Markdown.
        # pdf_generator.py creates the real PDF afterward.
        output_file=str(REPORT_MD),
    )

    return [
        research_task,
        analysis_task,
        writing_task,
    ]


# =========================================================
# DELIVERY TASK
# =========================================================

def create_delivery_task(
    delivery_agent,
    delivery_method,
    recipient_email=None,
):
    """
    Create a delivery task only after the human operator
    has approved the delivery in main.py.

    Supported methods:
        gmail
        drive
        both
    """

    # Always calculate the absolute PDF path.
    pdf_path = str(REPORT_PDF.resolve())

    # -----------------------------------------------------
    # VERIFY DELIVERY METHOD
    # -----------------------------------------------------

    valid_methods = [
        "gmail",
        "drive",
        "both",
    ]

    if delivery_method not in valid_methods:

        raise ValueError(
            "Invalid delivery method. "
            "Use 'gmail', 'drive', or 'both'."
        )

    # -----------------------------------------------------
    # VERIFY EMAIL WHEN REQUIRED
    # -----------------------------------------------------

    if delivery_method in ["gmail", "both"]:

        if not recipient_email:

            raise ValueError(
                "An approved recipient email address is required "
                "for Gmail delivery."
            )

    # =====================================================
    # GMAIL ONLY
    # =====================================================

    if delivery_method == "gmail":

        description = (
            "The human operator has explicitly approved delivery "
            "of the final report by Gmail. "

            f"The approved PDF report is located at: '{pdf_path}'. "

            f"Send this exact PDF report to the approved recipient: "
            f"'{recipient_email}'. "

            "Use the email subject: "
            "'Approved Market Research Report'. "

            "Include a short professional message explaining that "
            "the approved market research report is attached. "

            "Attach the PDF report to the email. "

            "Do not modify the report. "
            "Do not change the recipient. "
            "Do not add additional recipients. "
            "Do not upload the report to Google Drive. "
            "Do not send the report to anyone else."
        )

        expected_output = (
            "Confirmation that the approved PDF report was sent "
            f"by Gmail to exactly '{recipient_email}'."
        )

    # =====================================================
    # GOOGLE DRIVE ONLY
    # =====================================================

    elif delivery_method == "drive":

        description = (
            "The human operator has explicitly approved delivery "
            "of the final report to Google Drive. "

            f"The approved PDF report is located at: '{pdf_path}'. "

            "Upload this exact PDF report to the user's "
            "connected Google Drive. "

            "Keep the filename 'report.pdf'. "

            "Do not modify the report. "
            "Do not email the report. "
            "Do not send the report to any recipient. "

            "After the upload, report whether the upload "
            "was successful."
        )

        expected_output = (
            "Confirmation that the approved report.pdf "
            "was successfully uploaded to Google Drive."
        )

    # =====================================================
    # GMAIL + GOOGLE DRIVE
    # =====================================================

    elif delivery_method == "both":

        description = (
            "The human operator has explicitly approved delivery "
            "of the final report using BOTH Gmail and Google Drive. "

            f"The approved PDF report is located at: '{pdf_path}'. "

            "FIRST: "
            "Upload this exact PDF report to the user's "
            "connected Google Drive. "
            "Keep the filename 'report.pdf'. "

            "SECOND: "
            f"Send this exact PDF report to the approved Gmail "
            f"recipient: '{recipient_email}'. "

            "Use the email subject: "
            "'Approved Market Research Report'. "

            "Include a short professional message explaining that "
            "the approved market research report is attached. "

            "Attach the PDF report to the Gmail message. "

            "Do not modify the report. "
            "Do not change the approved recipient. "
            "Do not add additional recipients. "
            "Do not send the report to anyone else. "

            "Complete both approved delivery actions and report "
            "the result of each action separately."
        )

        expected_output = (
            "Confirmation containing two results: "
            "1. Google Drive upload status for report.pdf. "
            f"2. Gmail delivery status to exactly '{recipient_email}'."
        )

    # =====================================================
    # CREATE DELIVERY TASK
    # =====================================================

    delivery_task = Task(
        description=description,
        expected_output=expected_output,
        agent=delivery_agent,
    )

    return delivery_task