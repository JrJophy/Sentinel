from bs4 import BeautifulSoup
import requests

def detect_sensitive_forms(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        flagged = []

        for form in forms:
            inputs = form.find_all('input')
            has_password = any(inp.get('type') == 'password' for inp in inputs)
            if has_password:
                flagged.append({
                    'action': form.get('action'),
                    'inputs': [inp.get('type') for inp in inputs]
                })

        return flagged
    except requests.exceptions.Timeout:
        return [{'error': 'Request timed out'}]
    except requests.exceptions.RequestException as e:
        return [{'error': f'Request failed: {str(e)}'}]
    except Exception as e:
        return [{'error': f'Error: {str(e)}'}]
