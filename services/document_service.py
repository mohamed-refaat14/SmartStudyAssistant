from pypdf import PdfReader


def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages_text.append(page_text.strip())

    if not pages_text:
        raise ValueError(
            "No extractable text was found in the PDF."
        )

    return "\n\n".join(pages_text)


def extract_pdf_pages(uploaded_file) -> list[dict]:
    reader = PdfReader(uploaded_file)
    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1,
    ):
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages.append(
                {
                    "page_number": page_number,
                    "text": page_text.strip(),
                }
            )

    if not pages:
        raise ValueError(
            "No extractable text was found in the PDF."
        )

    return pages
