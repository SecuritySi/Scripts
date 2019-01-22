#!/usr/bin/python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import generator


send_from = ""
send_to = ""
subject = ""
message = "#MESSAGEDATA"
server = "127.0.0.1"
port = 25


def create_eml(send_from, send_to, subject, message):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['Message-ID'] = "#MessageID"

    msg.attach(MIMEText(message))
    msg.attach(MIMEMultipart())


    with open("email.eml", 'w') as outfile:
        gen = generator.Generator(outfile)
        gen.flatten(msg)


create_eml(send_from, send_to, subject, message)