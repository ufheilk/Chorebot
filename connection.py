import imaplib
import smtplib
import person

from email.mime.text import MIMEText

class Messager:
    """Abstraction of an SMTP connection over which messages can be sent"""
    def __init__(self, account, password):
        self.account = account
        self.connection = SMTP_CONNECTION = smtplib.SMTP(host='smtp.gmail.com', port=587, timeout=1000000)
        self.connection.starttls()
        self.connection.login(account, password)

    def send(self, recipient, msg):
        msg = MIMEText(msg)
        msg['From'] = self.account
        msg['To'] = recipient
        self.connection.sendmail(self.account, recipient, msg.as_string())

class Mailbox:
    """Abstraction of an IMAP4 gmail connection which can access emails"""
    def __init__(self, account, password):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(account, password)
        self.mail.select('inbox')

    def process_mail(self, people):
        rv, data = self.mail.search(None, 'ALL')
        mail_ids = data[0].split()
        
        for mail_id in mail_ids:
            rv, data = self.mail.fetch(mail_id, '(BODY[HEADER.FIELDS (FROM)])')
            raw_email = data[0][1]
            print(raw_email) 
            self.mail.store(mail_id, '+FLAGS', r'\Deleted')
        
        self.mail.expunge()
    
