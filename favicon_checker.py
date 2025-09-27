import hashlib
import requests

def get_favicon_hash(url):
    try:
        if not url.endswith('/'):
            url += '/'
        favicon_url = url + 'favicon.ico'
        response = requests.get(favicon_url, timeout=5)
        if response.status_code == 200:
            return hashlib.sha256(response.content).hexdigest()
        return None
    except requests.exceptions.Timeout:
        return None  # Could not fetch favicon (timeout)
    except requests.exceptions.RequestException as e:
        return None  # Could not fetch favicon (request failed)
    except Exception as e:
        return None  # Handle other unexpected errors
