import requests
import json
import xmltodict
import re
from bs4 import BeautifulSoup

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
    else:
        return True

def validate_ascii_local(local: str):
    local = local.lower()
    if len(local) > 255 or len(local) <= 0:
        return False
    elif '--' or '..' in local:
        return False
    # Begins with letter and ends with digits or letters per rfc1035
    elif re.search('[a-z]', local[0]) == False or re.search('[a-z0-9]', local[-1]) == False:
        return False
    elif re.search('^[a-z0-9\-]*$', local) == False:
        return False
    else:
        return True
    

def validate_ascii_email(email: str):
    ats_count = email.count('@')
    if ats_count != 1:
        return False
    local, domain = email.split('@')

    if validate_ascii_domain(domain) == False:
        return False
    elif validate_ascii_local(local) == False:
        return False
    else:
        return True

usr_file = input("Please enter your File Name : ")

valid = usr_file.split('.')[-1]

final = []

if valid == 'html':
    with open(usr_file, 'r') as f:

        contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')

        tags = soup.find_all()
        for tag in tags:
            final.extend(tag.text.split())
            for i in final:
                final.append(' '.join(i))
                final.remove(i)
    f.close()
    print(final)
else:
    print('invalid file')
