import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import json

# Importing your existing functions (adjust the imports as per your project structure)
from anti_phish_tool.ssl_checker import get_ssl_info
from anti_phish_tool.brand_title_checker import check_brand_in_title
from anti_phish_tool.pdf_scanner import extract_links_from_pdf
from anti_phish_tool.risk_score import calculate_risk_score
from anti_phish_tool.favicon_checker import get_favicon_hash
from anti_phish_tool.form_detector import detect_sensitive_forms
from anti_phish_tool.image_scanner import extract_links_from_image  # New import

app = Flask(__name__)

# Setting the upload folder for PDF and image files
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Utility function to check file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_url', methods=['POST'])
def analyze_url():
    data = request.get_json()
    url = data.get('url', '')
    
    # Placeholder for URL analysis
    analysis_results = {
        "ssl": get_ssl_info(url),
        "brand_check": check_brand_in_title(url),
        "favicon_hash": get_favicon_hash(url),
        "forms": detect_sensitive_forms(url),
        "risk": calculate_risk_score({
            'ssl': get_ssl_info(url),
            'brand_check': check_brand_in_title(url),
            'favicon_hash': get_favicon_hash(url),
            'forms': detect_sensitive_forms(url),
            'uses_ip': False,  # Add more logic as needed
            'bad_tld': False,  # Add logic for TLD
            'suspicious_keywords': False,  # Add logic for keywords
            'tunneling': False,  # Add tunneling checks
            'brand_mismatch': False,  # Based on brand check
        }),
        "suspicious_keywords": False,  # Add actual checks
        "tunneling": False,  # Add tunneling check
        "uses_ip": False,  # Add IP usage check
        "bad_tld": False,  # Check TLD
    }
    
    return jsonify(analysis_results)

@app.route('/analyze_pdf', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract URLs from the PDF
        extracted_urls = extract_links_from_pdf(file_path)

        return jsonify({'extracted_urls': extracted_urls})
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'})

# New route for image analysis
@app.route('/analyze_image', methods=['POST'])
def analyze_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Extract URLs from the image
        extracted_urls = extract_links_from_image(file_path)

        return jsonify({'extracted_urls': extracted_urls})
    else:
        return jsonify({'error': 'Invalid file type. Only image files are allowed.'})

if __name__ == '__main__':
    app.run(debug=True)
