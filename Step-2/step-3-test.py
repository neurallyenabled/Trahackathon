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


def validate_domain(domain: str):
    try:
        levels = domain.split('.')
        if len(levels) <= 1:
            return False
        domainName_normalized = unicodedata.normalize('NFC', domain.lower())
        domainName_alabel = idna.encode(domainName_normalized).decode("ascii") 
        if levels[-1] not in tlds_list:
            return False
        domainName_ulabel = idna.decode(domainName_alabel)

        return True
    except idna.IDNAError as e:   
        print(f"Domain '{domain}' is invalid: {e}")  #invalid domain as per IDNA 2008
    except Exception as e:
        print(f"ERROR: {e}")
    

def validate_email(email: str):
    try:
        validated = validate_email(email, check_deliverability=True)  
        return True
    except EmailNotValidError as e:
        print(f"'{email}' is not a valid email address: {str(e)}")
    except Exception as ex:
        print(f"Excpetion while processing {email}: {str(ex)}")

# Remove the last segment of the path

# Open the HTML in which you want to make changes
#html = open("D:\\advanced-css-course-master\\Natours\\starter\\aboutus.html")
html = open("/home/mj/projects/Trahackathon/ExampleHTMLs/aboutus.html")
# Parse HTML file in Beautiful Soup
soup = bs(html, 'html.parser')

# Give location where text is
# stored which you wish to aslter
tags = soup.find_all()
for tag in tags:
    words = tag.text.split()
    for word in words:
        if word == "|": 
           print(word)
        elif (validate_email(str(word)) == True):
            new_link = soup.new_tag("a", href=word)
            tag.find(text=re.compile(word)).replace_with(new_link)
            link = tag.find('a', href=word)
            link.string = word
        elif (validate_domain(str(word)) == True):
            try: 
                domainName_normalized = unicodedata.normalize('NFC', word.lower())
                domainName_alabel = idna.encode(domainName_normalized).decode("ascii") 
                new_link = soup.new_tag("a", href=domainName_alabel)
                tag.find(text=re.compile(word)).replace_with(new_link)
                link = tag.find('a', href=word)
                link.string = word
            except idna.IDNAError as e:   
                print(f"Domain '{domainName_normalized}' is invalid: {e}")  #invalid domain as per IDNA 2008
            except Exception as e:
                print(f"ERROR: {e}")

#with open("D:\\advanced-css-course-master\\Natours\\starter\\file.html", 'wb') as f:
with open("/home/mj/projects/Trahackathon/ExampleHTMLs/aboutus.html", 'wb') as f:
    f.write(soup.prettify("utf-8"))
