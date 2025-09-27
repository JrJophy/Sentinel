import requests
from bs4 import BeautifulSoup

KNOWN_BRANDS = ['facebook', 'google', 'paypal', 'apple', 'amazon']

def check_brand_in_title(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.lower() if soup.title else ''
        for brand in KNOWN_BRANDS:
            if brand in title:
                return {'brand': brand, 'title': title}
        return {'brand': None, 'title': title}
    except requests.exceptions.Timeout:
        return {'brand': None, 'error': 'Request timed out'}
    except requests.exceptions.RequestException as e:
        return {'brand': None, 'error': f'Request failed: {str(e)}'}
    except Exception as e:
        return {'brand': None, 'error': f'Error: {str(e)}'}
