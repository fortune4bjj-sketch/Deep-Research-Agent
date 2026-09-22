from pathlib import Path
from crewai import Crew, Process

from src.crew import create_crew
from src.agents import create_delivery_agent
from src.tasks import create_delivery_task
from src.pdf_generator import generate_pdf


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_MD = OUTPUT_DIR / "report.md"
REPORT_PDF = OUTPUT_DIR / "report.pdf"


# =========================================================
# HUMAN APPROVAL
# =========================================================

def get_delivery_approval():
    """
    Human-in-the-loop approval.

    Nothing is uploaded or emailed until the human
    explicitly approves the delivery.
    """

    print("\n" + "=" * 65)
    print("HUMAN-IN-THE-LOOP DELIVERY APPROVAL")
    print("=" * 65)

    print(f"\nFinal PDF:\n{REPORT_PDF.resolve()}")

    print("\nChoose delivery method:")
    print("1. Gmail")
    print("2. Google Drive")
    print("3. Gmail + Google Drive")
    print("4. Do not deliver")

    while True:

        choice = input("\nSelection (1-4): ").strip()

        if choice in ["1", "2", "3", "4"]:
            break

        print("Invalid selection. Enter 1, 2, 3, or 4.")

    # -----------------------------------------------------
    # CANCEL DELIVERY
    # -----------------------------------------------------

    if choice == "4":

        print("\nDelivery cancelled by human operator.")

        return None, None

    # -----------------------------------------------------
    # MAP SELECTION
    # -----------------------------------------------------

    delivery_map = {
        "1": "gmail",
        "2": "drive",
        "3": "both",
    }

    delivery_method = delivery_map[choice]

    recipient_email = None

    # -----------------------------------------------------
    # GET EMAIL RECIPIENT
    # -----------------------------------------------------

    if delivery_method in ["gmail", "both"]:

        while True:

            recipient_email = input(
                "\nEnter the approved recipient email: "
            ).strip()

            if (
                recipient_email
                and "@" in recipient_email
                and "." in recipient_email
            ):
                break

            print("Please enter a valid email address.")

    # -----------------------------------------------------
    # DISPLAY FINAL DELIVERY REQUEST
    # -----------------------------------------------------

    print("\n" + "-" * 65)
    print("FINAL DELIVERY REQUEST")
    print("-" * 65)

    print(f"\nReport:\n{REPORT_PDF.resolve()}")

    if delivery_method == "gmail":

        print("\nGoogle Drive: NO")
        print("Gmail: YES")
        print(f"Recipient: {recipient_email}")

    elif delivery_method == "drive":

        print("\nGoogle Drive: YES")
        print("Gmail: NO")

    elif delivery_method == "both":

        print("\nGoogle Drive: YES")
        print("Gmail: YES")
        print(f"Recipient: {recipient_email}")

    print("\n" + "-" * 65)

    # -----------------------------------------------------
    # FINAL HUMAN APPROVAL
    # -----------------------------------------------------

    approval = input(
        "\nApprove this delivery? Type YES to continue: "
    ).strip()

    if approval.upper() != "YES":

        print("\nDelivery NOT approved.")
        print("No email was sent.")
        print("No Google Drive upload was performed.")

        return None, None

    print("\nHuman approval received.")

    return delivery_method, recipient_email


# =========================================================
# DELIVER REPORT
# =========================================================

def deliver_report(delivery_method, recipient_email=None):
    """
    Create the delivery agent only AFTER human approval.
    """

    print("\n" + "=" * 65)
    print("STARTING APPROVED DELIVERY")
    print("=" * 65)

    # -----------------------------------------------------
    # SAFETY CHECK
    # -----------------------------------------------------

    if not REPORT_PDF.exists():

        raise FileNotFoundError(
            "\nDelivery blocked because PDF does not exist:\n"
            f"{REPORT_PDF.resolve()}"
        )

    if REPORT_PDF.stat().st_size == 0:

        raise ValueError(
            "\nDelivery blocked because PDF is empty:\n"
            f"{REPORT_PDF.resolve()}"
        )

    print("\nPDF verified before delivery.")
    print(f"File: {REPORT_PDF.resolve()}")
    print(f"Size: {REPORT_PDF.stat().st_size:,} bytes")

    # -----------------------------------------------------
    # CREATE DELIVERY AGENT
    # -----------------------------------------------------

    print("\nConnecting approved delivery tools...")

    delivery_agent = create_delivery_agent()

    # -----------------------------------------------------
    # CREATE APPROVED DELIVERY TASK
    # -----------------------------------------------------

    delivery_task = create_delivery_task(
        delivery_agent=delivery_agent,
        delivery_method=delivery_method,
        recipient_email=recipient_email,
    )

    # -----------------------------------------------------
    # CREATE DELIVERY CREW
    # -----------------------------------------------------

    delivery_crew = Crew(
        agents=[
            delivery_agent
        ],
        tasks=[
            delivery_task
        ],
        process=Process.sequential,
        verbose=True,
    )

    # -----------------------------------------------------
    # EXECUTE DELIVERY
    # -----------------------------------------------------

    print("\nExecuting approved delivery...\n")

    delivery_result = delivery_crew.kickoff()

    print("\n" + "=" * 65)
    print("DELIVERY RESULT")
    print("=" * 65)

    print(delivery_result)

    print("=" * 65)

    return delivery_result


# =========================================================
# MAIN RESEARCH WORKFLOW
# =========================================================

def run(topic):

    print("\n" + "=" * 65)
    print("DEEP RESEARCH MULTI-AGENT SYSTEM")
    print("=" * 65)

    print(f"\nResearch Topic:\n{topic}")

    # -----------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # -----------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # -----------------------------------------------------
    # DELETE OLD REPORTS
    # -----------------------------------------------------

    if REPORT_MD.exists():

        print("\nRemoving previous Markdown report...")
        REPORT_MD.unlink()

    if REPORT_PDF.exists():

        print("Removing previous PDF report...")
        REPORT_PDF.unlink()

    # =====================================================
    # STEP 1 - RUN RESEARCH CREW
    # =====================================================

    print("\n" + "=" * 65)
    print("STEP 1 - RESEARCH AND ANALYSIS")
    print("=" * 65)

    research_crew = create_crew()

    research_result = research_crew.kickoff(
        inputs={
            "topic": topic
        }
    )

    print("\nResearch crew completed.")

    # =====================================================
    # STEP 2 - VERIFY MARKDOWN
    # =====================================================

    print("\n" + "=" * 65)
    print("STEP 2 - VERIFY REPORT")
    print("=" * 65)

    if not REPORT_MD.exists():

        raise FileNotFoundError(
            "\nCrewAI completed but report.md was not created.\n\n"
            f"Expected location:\n{REPORT_MD.resolve()}"
        )

    if REPORT_MD.stat().st_size == 0:

        raise ValueError(
            "\nreport.md exists but is empty.\n\n"
            f"File:\n{REPORT_MD.resolve()}"
        )

    print("\nMarkdown report verified.")

    print(
        f"\nLocation:\n"
        f"{REPORT_MD.resolve()}"
    )

    print(
        f"\nSize: "
        f"{REPORT_MD.stat().st_size:,} bytes"
    )

    # =====================================================
    # STEP 3 - CREATE REAL PDF
    # =====================================================

    print("\n" + "=" * 65)
    print("STEP 3 - GENERATE PDF")
    print("=" * 65)

    generate_pdf(
        REPORT_MD,
        REPORT_PDF,
    )

    # =====================================================
    # STEP 4 - VERIFY PDF
    # =====================================================

    print("\n" + "=" * 65)
    print("STEP 4 - VERIFY PDF")
    print("=" * 65)

    if not REPORT_PDF.exists():

        raise FileNotFoundError(
            "\nPDF generation failed.\n\n"
            f"Expected PDF:\n{REPORT_PDF.resolve()}"
        )

    if REPORT_PDF.stat().st_size == 0:

        raise ValueError(
            "\nPDF exists but is empty.\n\n"
            f"File:\n{REPORT_PDF.resolve()}"
        )

    print("\nPDF created and verified successfully.")

    print(
        f"\nPDF:\n"
        f"{REPORT_PDF.resolve()}"
    )

    print(
        f"\nPDF Size: "
        f"{REPORT_PDF.stat().st_size:,} bytes"
    )

    # =====================================================
    # STEP 5 - HUMAN-IN-THE-LOOP
    # =====================================================

    delivery_method, recipient_email = (
        get_delivery_approval()
    )

    # Human cancelled delivery
    if delivery_method is None:

        print("\n" + "=" * 65)
        print("WORKFLOW COMPLETED WITHOUT DELIVERY")
        print("=" * 65)

        print(
            "\nYour report remains available at:\n"
            f"{REPORT_PDF.resolve()}"
        )

        return research_result

    # =====================================================
    # STEP 6 - APPROVED DELIVERY
    # =====================================================

    delivery_result = deliver_report(
        delivery_method=delivery_method,
        recipient_email=recipient_email,
    )

    # =====================================================
    # COMPLETE
    # =====================================================

    print("\n" + "=" * 65)
    print("WORKFLOW COMPLETED")
    print("=" * 65)

    print(f"\nResearch Topic:\n{topic}")

    print(
        f"\nFinal PDF:\n"
        f"{REPORT_PDF.resolve()}"
    )

    print(
        f"\nDelivery Method: "
        f"{delivery_method.upper()}"
    )

    if recipient_email:

        print(
            f"Email Recipient: "
            f"{recipient_email}"
        )

    print("\nHuman approval: YES")

    print("=" * 65)

    return {
        "research_result": research_result,
        "delivery_result": delivery_result,
    }


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":

    try:

        print("\n" + "=" * 65)
        print("DEEP RESEARCH AGENT")
        print("Research -> Analysis -> PDF -> Human Approval -> Delivery")
        print("=" * 65)

        topic = input(
            "\nEnter the topic you want to research: "
        ).strip()

        if not topic:

            raise ValueError(
                "You must enter a research topic."
            )

        run(topic)

    except KeyboardInterrupt:

        print(
            "\n\nProgram cancelled by human operator."
        )

    except Exception as error:

        print("\n" + "=" * 65)
        print("PROGRAM ERROR")
        print("=" * 65)

        print(
            f"\nError Type: "
            f"{type(error).__name__}"
        )

        print(
            f"\nError Message:\n{error}"
        )

        print("\n" + "=" * 65)