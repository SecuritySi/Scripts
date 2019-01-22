#!/usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

send_from = "SENDER_EMAIL"
send_to = "TO_EMAIL"
subject = "IMPORTANT: Please Click Me"
server = "127.0.0.1"
port = 25


def send_mail(send_from, send_to, subject, message, files,
              server, port):

    msg = MIMEMultipart('alternative')
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['Message-ID'] = "#MessageID"

    text = "Hi,\n Test,\nClick this link: http://www.fakeurl.local"

    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi,<br>
    	Test,<br>
    	Click this link: <a href="http://www.fakeurl.local">link</a>
        </p>
      </body>
    </html>
    """
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)

    smtp = smtplib.SMTP(server, port)

    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()

send_mail(send_from, send_to, subject, message, files,
              server, port)
