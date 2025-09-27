def calculate_risk_score(results):
    score = 0

    if results.get('uses_ip'): score += 30
    if results.get('bad_tld'): score += 20
    if results.get('tunneling'): score += 15
    if results.get('suspicious_keywords'): score += 15
    if not results.get('ssl', {}).get('valid', True): score += 10
    if results.get('brand_mismatch'): score += 20

    if score >= 60:
        level = 'High'
    elif score >= 30:
        level = 'Medium'
    else:
        level = 'Low'

    return {'score': score, 'level': level}
