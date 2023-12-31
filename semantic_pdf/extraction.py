import pytesseract
from tqdm import tqdm
from mydatabase import SemPdf
from pdf2image import convert_from_path


def extract_text_from_pdf(pdf_path):
    # Convert PDF to image
    pages = convert_from_path(pdf_path)

    # Extract text from each page using Tesseract OCR
    text_data = ""
    for page in pages:
        text = pytesseract.image_to_string(page)
        text_data += text + "\n"

    # Return the text data
    return text_data


def extract_text_for_sempdfs(sempdfs: list[SemPdf]):
    pbar = tqdm(sempdfs)
    for sempdf in pbar:
        sempdf.text = extract_text_from_pdf(sempdf.paths[0])
        pbar.set_description("Processing %s" % sempdf.paths[0].split("/")[-1])
    return sempdfs
