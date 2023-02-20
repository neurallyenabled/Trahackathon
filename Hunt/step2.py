import socket
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
print('Connected to SMTP')
# start TLS for security
s.starttls()

sender_mail = 'اخضر@فريق-٧.البحرين'
to = 'حكم-١@هتا.البحرين'

to = parse_main(to)
sender_mail = parse_main(sender_mail)
print('parsed', sender_mail, to)

# s.login(sender_mail, '8771643373')
# print('Logged in')

# # message to be sent
# header = 'To:' + to + '\n' + 'From: ' + euser + '\n' + 'Subject:Step-1 \n'
# print (header)
msg = f'''\
From: {sender_mail}
To: {to}
Subject: Step-2

فريق٧
'''

# sending the mail
s.sendmail(sender_mail, to, msg)
print('sent')
# terminating the session
s.quit()



