import smtplib
import ssl
from email.message import EmailMessage
from typing import List

class EmailConnector:
    def __init__(self, email_sender: str, email_password: str, smtp_host: str = 'smtp.gmail.com', smtp_port: int = 465) -> None:
        self.email_sender = email_sender
        self.email_password = email_password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.context = ssl.create_default_context()

    def send_email(self, receiver_list: List[str], subject: str, body: str) -> bool:
        em = EmailMessage()
        em['From'] = self.email_sender


        em['To'] = ", ".join(receiver_list)
        em['Subject'] = subject
        
        em.set_content("Seu cliente de e-mail não suporta HTML.")
        em.add_alternative(body, subtype='html')

        try:
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=self.context) as smtp:
                smtp.login(self.email_sender, self.email_password)
                smtp.send_message(em)
                return True
        except smtp.SMTPAuthenticationError:
            print("Erro de autentificação. Verifique credenciais.")
            return False
        except Exception as e:
            print(f"Erro: {e}")
            return False