import fitz


def read_pdf(path):
    doc = fitz.open(path)

    text = []

    print(f"Pages: {len(doc)}")

    for i, page in enumerate(doc):
        page_text = page.get_text()

        print(f"Page {i + 1}: {len(page_text)} chars")

        text.append(page_text)

    return "\n".join(text)
