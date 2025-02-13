import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def send_otp(email):
    otp = str(random.randint(100000, 999999))

    sender_email = "sgessagessg@gmail.com"
    sender_password = "tdic wanb hzue pcmn"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email
    message['Subject'] = "Your OTP Code: " + otp
    body = f"Welcome, User! Your OTP code is: {otp}"
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return otp
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None
