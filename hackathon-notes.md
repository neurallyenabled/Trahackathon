Types of top level domain(TLD) names:
- old short top-level (ASCII)
- new short top-level
- longer top-level
- internationalized top-level (IDN)
## IDN
- each n-level domain in a domain is 63 octet, with the whole domain less than 255 octet including separators

Concepts: character / character set / glyph / code point / octet

0600-06FF for Arabic script character in Unicode

unicode encoding used is UTF-8

## basic operations

~~~python
# read UTF-8 input
print("Enter your input: ")
inputstr = input() # default encoding is UTF-8
print("Input dat is: ")
print(inputstr)
~~~

~~~ python
# read UTF-8 file
file = open("filepath","r",encoding='UTF-8')
for line in file:
 print(line)
file.close()
~~~

~~~ python
# write UTF-8 file
file2 = open("filepath", 'w',encoding='UTF-8')
data_to_write = "السلام عليكم"
file2.writeline(data_to_write)
file2.close()
~~~

## Normalization
- multiple characters can produce the same glyph, nromalization reduces the number of caharcters used to produce the glyph
- normalization forms: NFD/**NFC**/NFKD/NFKC

~~~ python
# normalization code
import unicodedata

inputstr = input() # take input from user
normalized_input = unicodedata.normalize("NFC",inputstr) # normalize user input
print(normalized_input)
~~~

## U-label & A-label and Domain name validation

### U-label & A-label
- two equivalent IDN domain labels are U-label & A-label
- U-label for users & A-label for system and application processing
Process of converting U-label to A-label:
1. take user input and normalize it check against IDN2008 to form IDN U-label
2. convert U-label to puny-code(using RFC3492)
3. Add the "xn--" prefix to identify the ASCII string as an IDN A-label
### validation
- use **IDN2008** not IDN2003
- to validate an ASCII domain name RFC1035, letters, digits, and hyphen only with max length 255 octet and each label max 63 octet
- to validate an IDN domain name RFC5890-5894, both valid A-label and U-label
- A-label are used for host-name resolution
~~~ python
# convert U-label to A-label and vice versa & validate the domain name
import unicodedata # library for normalization
import idna # library for conversion
domain_name = "مصر.صحة"
try:
 domain_name_normalized = unicodedata.normalize("NFC", domain_name) # normalize to NFC
 print(domain_name_normalized)
 domain_name_alabel = idna.encode(domain_name_normalized).decode("ascii") #U-label to A-label
 print(domain_name_alabel)
 domain_name_ulabel = idna.decode(domain_name_alabel)
 print(domain_name_ulabel)
except idna.IDNAError as e:
 print("Domain '{domain_name}' is invalid: {e}") # invalid domain as per IDNA2008
except Exception as e:
 print("ERROR: {e}")
~~~

## domain name resolution
~~~ python
# domain name resolution
import socket
import unicodedata
import idna
domain_name = "مصر.صحة"
try:
 domain_name_normalized = unicodedata.normalize("NFC",domain_name)
 # U-label to A-label
 domain_name_alabel = idna.encode(domain_name_normalized).decode("ascii")
 # get IP address of the domain
 ip = socket.gethostbyname(domain_name_alabel)
 print(ip)
except Exception as ex:
 print(ex)
~~~

## domain name storage
- datebase configured to support UTF-8
### SQL: mysql, oracle, microsoftsqlserver
- set domain name to max 255 octet, 63 octet per label
	- in UTF-8, variable-length
- use variable-length string column
- consider/verify the object-relational mapping (ORM) driver/tool if you use it
### NOSQL
- already UTF-8 variable length
- store U-label and A-label consistently
- store them in separate fields

## EAI
- A-label and U-label represent the same email address
- support both, but use U-label for user facing and A-label for back-end
- email validation regex: '.*@.*'
- send and receive email in both U-label & A-label
- store email in either A-label or U-label form
- mail server manages the sending & receiving of email
- you are concerned with the handover process from the front-end to mail-server how to make it compliant
Types of internationalized email addresses:
- ASCII@IDN
- UTF8@ASCII
- UTF8@IDN LTR
- UTF8@IDN RTL

EMAIL SYSTEM:
- MUA: user client
- MSA: SMTP
- MTA: backend
- MDA: POP/IMAP

~~~ python
# EAI validation
from email_validator import validate_email,EmailNotValidError
logger = logging.getLogger(__name__)
try:
 # it performs DNS resolution
 # it performs normalization
 # it supports internationalized domain name
 validated = validate_email(email_address, check_deliverability=True)
 print(validated)
 logger.info("'{address}' is a valid email address")
 print("'{address}' is a valid email address")
except EmailNotValidError as e:
 print("'{address}' is not a valid email address: {e}")
except Exception as ex:
 print("Unexpected Exception")
~~~

~~~ python
# sending by the smtplib
# does not validate the email
try:
 to = "kevin@example.com"
 local_part, doamin = to.rsplit('@',1)
 domain_normalized = unicodedata.normalize("NFC",domain)
 to = '@'.join((local_part,idna.encode(domain_normalized).decode("ascii"))) # convert U-label to A-label
 validated = validate_email(to, check_deliverability=True) # validate email address
 if validated:
  host=''
  port=''
  smtp = smtplib.SMTP(host,port)
  smtp.set_debuglevel(False)
  smtp.login('username','password')
  sender = 'ua2test.org'
  subject='hi'
  content='content here'
  msg = EmailMessage()
  msg.set_content(content)
  msg('Subject') = subject
  msg('From') = sender
  msg('to') = to
  smtp.send_message(msg,sender,to)
  smtp.quit()
  logger.info("Email sent to '{to}'")
except smtplib.SMTPNotSupportedError:
 # the server does not support the SMTPUTF8 option, you may want to perform downgrading
 logger.warning("the SMTP server {host}:{port} does not support the SMTPUTF8 option")
 raise
~~~
