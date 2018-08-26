

class Messager():
    """Abstraction of an SMTP connection over which messages can be sent"""
    def __init__(self):
        pass

    def send(self, recipient, msg):
        pass

class Mailbox():
    """Abstraction of an IMAP4 gmail connection which can access emails"""
    def __init__(self):
        pass
    
    
