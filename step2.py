# sending by the smtplib
# does not validate the email
import socket
import unicodedata
import idna
from email_validator import validate_email, EmailNotValidError
import smtplib
try:
    to = "حكم-١@هتا.البحرين"
    sndr = 'اخضر@فريق-٧.البحرين'
    sndr_local, sndr_domain = sndr.split("@", 1)
    sndr_normal = unicodedata.normalize('NFC', sndr_domain)

    sndr = '@'.join((sndr_local, idna.encode(sndr_normal).decode("ascii")))

    local_part, domain = to.rsplit('@', 1)
    domain_normalized = unicodedata.normalize("NFC", domain)
    
    # convert U-label to A-label
    to = '@'.join((local_part, idna.encode(domain_normalized).decode("ascii")))
    print(to)
    # validate email address
    validated = validate_email(to, check_deliverability=True)
    if validated:
        host = '10.83.9.133'
        port = '578'
        smtp = smtplib.SMTP(host, port)
        smtp.set_debuglevel(False)
        smtp.login(sndr, '8771643373')
        print('Logged in')
        sender = sndr
        subject = 'Step-2'
        content = 'Team7'
        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['to'] = to
        smtp.send_message(msg, sender, to)
        smtp.quit()
        logger.info("Email sent to '{to}'")
except smtplib.SMTPNotSupportedError:
    # the server does not support the SMTPUTF8 option, you may want to perform downgrading
    logger.warning(
        "the SMTP server {host}:{port} does not support the SMTPUTF8 option")
    raise
