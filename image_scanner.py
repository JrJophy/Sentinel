# anti_phish_tool/image_scanner.py

import pytesseract
from PIL import Image
import re

# Windows-specific Tesseract path - update if needed
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_links_from_image(image_path):
    """
    Extracts URLs from a given image using OCR.

    Args:
        image_path (str): The path to the image file.

    Returns:
        list: A list of extracted URLs found in the image.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        # Optional: Clean up text if needed
        text = text.replace('\n', ' ').replace('\r', '')

        # Use regex to extract http/https URLs
        urls = re.findall(r'(https?://[^\s]+)', text)
        return urls
    except Exception as e:
        print(f"[ERROR] Failed to extract links from image: {e}")
        return []
