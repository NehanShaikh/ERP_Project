import pytesseract
import cv2
import sys
import json
from parser import extract_invoice_data
from pdf_handler import pdf_to_images

# Windows path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise Exception(f"Image not found or invalid format: {image_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)

    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    text = pytesseract.image_to_string(thresh)
    return text

def process_invoice(file_path):
    full_text = ""

    if file_path.endswith(".pdf"):
        images = pdf_to_images(file_path)
        for img in images:
            full_text += extract_text(img)
    else:
        full_text = extract_text(file_path)

    data = extract_invoice_data(full_text)
    return data

if __name__ == "__main__":
    file_path = sys.argv[1]

    result = process_invoice(file_path)
    

    print(json.dumps(result))
