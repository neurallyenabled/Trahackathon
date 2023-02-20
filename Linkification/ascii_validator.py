import requests
import json
import xmltodict
import re

tlds_list = requests.get('http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split()[11::]

allowed_resp = requests.get('https://www.iana.org/assignments/idna-tables-11.0.0/idna-tables-11.0.0.xml')

allowed_dict = xmltodict.parse(allowed_resp.text)

def validate_ascii_domain(domain: str):
    domain = domain.lower()
    if len(domain) > 255 or len(domain) <= 0:
        return False
    if '--' or '..' in domain:
        return False
    levels = domain.split('.')

    for level in levels:
        # Begins with letter and ends with digits or letters per rfc1035
        if re.search('[a-z]', level[0]) == False or re.search('[a-z0-9]', level[-1]) == False:
            return False
        # Max octet of 63
        if len(level) > 63:
            return False
            # Letters, Digits and Hypens allowed
        if re.search('^[a-z0-9\-]*$', level) == False:
            return False
    if level[-1] not in tlds_list:
        return False

    return True

def validate_ascii_local(local: str):
    local = local.lower()
    if len(local) > 255 or len(local) <= 0:
        return False
    if '--' or '..' in local:
        return False
    # Begins with letter and ends with digits or letters per rfc1035
    if re.search('[a-z]', local[0]) == False or re.search('[a-z0-9]', local[-1]) == False:
        return False
    if re.search('^[a-z0-9\-]*$', local) == False:
            return False

def validate_ascii_email(email: str):
    ats_count = email.count('@')
    if ats_count != 1:
        return False
    local, domain = email.split('@')

    if validate_ascii_domain(domain) == False:
        return False
    if validate_ascii_local(local) == False:
        return False

    return True
