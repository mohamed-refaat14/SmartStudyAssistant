from pypdf import PdfReader


def extract_pdf_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text and page_text.strip():
            pages_text.append(page_text.strip())

    if not pages_text:
        raise ValueError("No extractable text was found in the PDF.")

    return "\n\n".join(pages_text)
