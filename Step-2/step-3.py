import requests
import xmltodict
import re
from bs4 import BeautifulSoup as bs
import unicodedata 
import idna
from email_validator import validate_email,EmailNotValidError


tlds_list = requests.get(
    'http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split()[11::]
tlds_list = [x.lower() for x in tlds_list]

allowed_resp = requests.get(
    'https://www.iana.org/assignments/idna-tables-11.0.0/idna-tables-11.0.0.xml')

allowed_dict = xmltodict.parse(allowed_resp.text)

def parse_main(mail):
    mail_local, mail_domain = mail.split('@')
    mail_normal = unicodedata.normalize('NFC', mail_domain)
    mail_mail = '@'.join((mail_local, idna.encode(mail_normal).decode("ascii")))
    return mail_mail


def validate_ascii_domain(domain: str):
    try:
        domainName_normalized = unicodedata.normalize('NFC', domain)
        domainName_alabel = idna.encode(domainName_normalized).decode("ascii") 
        domainName_ulabel = idna.decode(domainName_alabel)
        domain = domainName_ulabel.lower()
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
    except idna.IDNAError as e:       
        print("Domain '{domainName}' is invalid: {e}")  #invalid domain as per IDNA 2008
    except Exception as e:
        print("ERROR: {e}")
    


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
    try:
        validated = validate_email(email, check_deliverability=False)  
        return validated
    except EmailNotValidError as e:
        print("'{address}' is not a valid email address: {e}")
    except Exception as ex:
        print("Unexpected Exception")

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
