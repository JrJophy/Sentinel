import fitz  # PyMuPDF
import re
import base64

def extract_links_from_pdf(pdf_path):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        text = ""

        # Extract text from all pages
        for page in doc:
            text += page.get_text()

        # Normal and obfuscated URLs
        urls = set(re.findall(r'(https?://\S+|hxxps?://\S+|http\[\:\]/{2}\S+)', text))

        # Base64 decoding (simple scan)
        b64_matches = re.findall(r'([A-Za-z0-9+/=]{20,})', text)
        decoded_urls = []
        for b64 in b64_matches:
            try:
                decoded = base64.b64decode(b64).decode('utf-8')
                if 'http' in decoded:
                    decoded_urls.append(decoded)
            except (base64.binascii.Error, UnicodeDecodeError):
                continue

        # Return both found URLs and base64 decoded URLs
        return list(urls) + decoded_urls
    except Exception as e:
        return [f'Error reading PDF: {str(e)}']
