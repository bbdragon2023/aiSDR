"""Email integration for sending outreach emails via SMTP."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional


class EmailClient:
    """SMTP email client for sending outreach emails."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        from_email: str,
        from_name: str = "SDR Agent",
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.from_email = from_email
        self.from_name = from_name

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        to_name: Optional[str] = None,
        html_body: Optional[str] = None,
    ) -> tuple[bool, str]:
        """Send an email via SMTP.

        Args:
            to_email: Recipient email address
            subject: Email subject line
            body: Plain text email body
            to_name: Optional recipient name
            html_body: Optional HTML version of the body

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"

            if to_name:
                msg["To"] = f"{to_name} <{to_email}>"
            else:
                msg["To"] = to_email

            # Attach plain text body
            msg.attach(MIMEText(body, "plain"))

            # Attach HTML body if provided
            if html_body:
                msg.attach(MIMEText(html_body, "html"))

            # Connect and send
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            return True, f"Email sent successfully to {to_email}"

        except smtplib.SMTPAuthenticationError:
            return False, "Authentication failed. Check your username and password."
        except smtplib.SMTPRecipientsRefused:
            return False, f"Recipient address rejected: {to_email}"
        except smtplib.SMTPException as e:
            return False, f"SMTP error: {str(e)}"
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"

    def test_connection(self) -> tuple[bool, str]:
        """Test the SMTP connection.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
            return True, "SMTP connection successful"
        except Exception as e:
            return False, f"SMTP connection failed: {str(e)}"
