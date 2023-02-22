import unicodedata
import idna
from email_validator import validate_email, EmailNotValidError
import smtplib

def parse_main(mail):
  mail_local, mail_domain = mail.split('@')
  mail_normal = unicodedata.normalize('NFC', mail_domain)
  mail_mail = '@'.join((mail_local, idna.encode(mail_normal).decode("ascii")))
  return mail_mail

# creates SMTP session
s = smtplib.SMTP('10.83.9.133', 25)
# start TLS for security
s.starttls()

sender_mail = 'اخضر@فريق-٧.البحرين'
to = 'حكم-٢@هتا.البحرين'

to = parse_main(to)
sender_mail = parse_main(sender_mail)

msg = f'''\
From: {sender_mail}
To: {to}
Subject: Step-2

فريق٧
'''

# sending the mail
s.sendmail(sender_mail, to, msg)
# terminating the session
s.quit()



