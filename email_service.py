import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import logging

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        # Set default values if environment variables are not set
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.email_from = os.getenv("EMAIL_FROM")
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            autoescape=True
        )
        
        # Validate required settings
        if not all([self.smtp_username, self.smtp_password, self.email_from]):
            logging.warning("Email service not properly configured. Emails will not be sent.")
            self.is_configured = False
        else:
            self.is_configured = True

    async def send_reminder(self, task, recipient_email):
        if not self.is_configured:
            logging.warning("Email service not configured. Skipping reminder email.")
            return

        try:
            # Get the template
            template = self.env.get_template('reminder_email.html')
            
            # Render the HTML
            html_content = template.render(task=task)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Reminder: {task.title}'
            msg['From'] = self.email_from
            msg['To'] = recipient_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logging.info(f"Reminder email sent successfully for task: {task.title}")
            
        except Exception as e:
            logging.error(f"Failed to send reminder email for task {task.title}: {str(e)}")
            # Don't raise the exception - we don't want the application to crash if email sending fails
            return False
        
        return True 