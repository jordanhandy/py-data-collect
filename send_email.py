# Import modules
# MIME.Text allow for HTML formatted mail
from email.mime.text import MIMEText
import smtplib

# Function send email
# params:
# sender email
# height
# average height
# record count
def send_email(email, height, average_height, count):
    # SMTP auth info
    from_email="myemail@gmail.com"
    from_password="mypassword"
    to_email=email

    subject="Height data"
    message="Hey there, your height is <strong>%s</strong>. <br> Average height of all is <strong>%s</strong> and that is calculated out of <strong>%s</strong> people. <br> Thanks!" % (height, average_height, count)

    # Read line above as HTML
    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    # Auth methods for Gmail server
    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    # Send method to send email
    gmail.send_message(msg)
