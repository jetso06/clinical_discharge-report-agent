import io

import fitz
import pytesseract
from PIL import Image


def extract_text_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)

    full_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]

        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))

        img_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(img_bytes))

        text = pytesseract.image_to_string(image)

        full_text.append(text)

        print(f"Processed page {page_num + 1}/{len(doc)}")

    return "\n".join(full_text)
