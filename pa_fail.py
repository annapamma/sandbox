import json
import os
import pickle
import sys
import urllib.request

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def process():
    context = ssl.create_default_context()
    file_id = sys.argv[1]
    urllib.request.urlretrieve(f'http://pathwayassessor.org/expression_table/{file_id}', '/tmp/tmp.pkl')
    data = pickle.load(open('/tmp/tmp.pkl', 'rb'))
    receiver_email = data['email']

    subject = "IPAS Results -- Error"
    body = """
        There was an issue with your IPAS run. 
        Please try again.
        
        You can also reach out to anna.calinawan@mssm.edu about file {}
    """.format(file_id)
    sender_email = "pathwayassessorresults@gmail.com"
    password = os.getenv('PA_CIRCLE')

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    text = message.as_string()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    return 'OK'


if __name__ == '__main__':
    print('Fail!!')
    print(sys.argv[1])
    process()
