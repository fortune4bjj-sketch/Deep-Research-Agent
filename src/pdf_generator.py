from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
)


def generate_pdf(markdown_path, pdf_path):

    markdown_path = Path(markdown_path)
    pdf_path = Path(pdf_path)

    if not markdown_path.exists():
        raise FileNotFoundError(
            f"Markdown report was not found: {markdown_path}"
        )

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    content = markdown_path.read_text(
        encoding="utf-8"
    )

    if not content.strip():
        raise ValueError(
            "The generated report is empty."
        )

    styles = getSampleStyleSheet()

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
        title="Market Research Report",
    )

    story = []

    for line in content.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(
                    line[2:],
                    styles["Title"],
                )
            )

        elif line.startswith("## "):
            story.append(
                Spacer(1, 10)
            )
            story.append(
                Paragraph(
                    line[3:],
                    styles["Heading2"],
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    line[4:],
                    styles["Heading3"],
                )
            )

        elif line.startswith("- "):
            story.append(
                ListFlowable(
                    [
                        ListItem(
                            Paragraph(
                                line[2:],
                                styles["BodyText"],
                            )
                        )
                    ],
                    bulletType="bullet",
                )
            )

        else:
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"],
                )
            )

            story.append(
                Spacer(1, 6)
            )

    document.build(story)

    if not pdf_path.exists():
        raise RuntimeError(
            "PDF generation failed."
        )

    if pdf_path.stat().st_size == 0:
        raise RuntimeError(
            "PDF was created but is empty."
        )

    print(
        f"PDF created successfully: "
        f"{pdf_path.resolve()}"
    )

    return pdf_path.resolve()