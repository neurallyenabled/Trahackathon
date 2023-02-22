import requests
import xmltodict
import re
from bs4 import BeautifulSoup as bs
import unicodedata 
import idna        

tlds_list = requests.get(
    'http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split()[11::]
tlds_list = [x.lower() for x in tlds_list]

allowed_resp = requests.get(
    'https://www.iana.org/assignments/idna-tables-11.0.0/idna-tables-11.0.0.xml')

allowed_dict = xmltodict.parse(allowed_resp.text)


def validate_ascii_domain(domain: str):    
    domain = domain.lower()
    if len(domain) > 255 or len(domain) <= 0:
        return False
    levels = domain.split('.')
    if len(levels) <= 1:
        return False
    for level in levels:
        # Max octet of 6
        if len(level) > 63 or len(level) <= 0:
            return False
        # Begins with letter and ends with digits or letters per rfc1035
        if re.search('[a-z]', level[0]) == False or re.search('[a-z0-9]', level[-1]) == False:
            return False
        # Letters, Digits and Hypens allowed
        if re.search('^[a-z0-9\-]*$', level) == False:
            return False
    if levels[-1] not in tlds_list:
        return False
    else:
        return True


def validate_ascii_local(local: str):
    local = local.lower()
    if len(local) > 64 or len(local) <= 0:
        return False
    if '--' or '..' in local:
        return False
    # Begins with letter and ends with digits or letters per rfc1035
    if re.search('[a-z]', local[0]) == False or re.search('[a-z0-9]', local[-1]) == False:
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


# Remove the last segment of the path

# Open the HTML in which you want to make changes
html = open("D:\\advanced-css-course-master\\Natours\\starter\\aboutus.html")

# Parse HTML file in Beautiful Soup
soup = bs(html, 'html.parser')

# Give location where text is
# stored which you wish to aslter
tags = soup.find_all()
for tag in tags:
    words = tag.text.split()
    for word in words:
        new_link = soup.new_tag("a", href=word)
        if (validate_ascii_email(str(word)) == True) or (validate_ascii_domain(str(word)) == True):
            tag.find(text=re.compile(word)).replace_with(new_link)
            link = tag.find('a', href=word)
            link.string = word


with open("D:\\advanced-css-course-master\\Natours\\starter\\file.html", 'wb') as f:
    f.write(soup.prettify("utf-8"))
