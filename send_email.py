from email.mime.text import MIMEText
import smtplib

def send_email(email, name):
    from_email = "testudemystudent123@gmail.com"
    from_password="niraj 2000"
    to_email=email

    subject="StockX sign up confirmation"
    message="Thank you <strong>%s</strong> for sigining up with StockX." % name

    msg=MIMEText(message, 'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
