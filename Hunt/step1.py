import smtplib
from getpass import getpass
to = 'uahackathon@gmail.com'

# euser = 'team7trahackathon@gmail.com'
# epwd = '@team7trahackathon123'

euser = input('email: ')
epwd = getpass('pass: ')
# creates SMTP session
s = smtplib.SMTP('smtp-mail.outlook.com', 587)

# start TLS for security
s.starttls()

# Authentication
s.login(euser, epwd)

# message to be sent
header = 'To:' + to + '\n' + 'From: ' + euser + '\n' + 'Subject:Step-1 \n'
print (header)
msg = f'''\
From: {euser}
To: {to}
Subject: Step-1

فريق٧
'''


# sending the mail
s.sendmail(euser, to, msg)

# terminating the session
s.quit()



