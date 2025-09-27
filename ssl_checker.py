import ssl
import socket
import tldextract

def get_ssl_info(url):
    try:
        domain = tldextract.extract(url).registered_domain
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                return {
                    'valid': True,
                    'issuer': issuer.get('organizationName', 'Unknown'),
                    'subject': dict(x[0] for x in cert['subject'])
                }
    except Exception as e:
        return {'valid': False, 'error': str(e)}
