from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import Config
from flask import current_app


def sendmail(email, subject, content):
    message = Mail(
        from_email=Config.SENDGRID_FROM_EMAIL,
        to_emails=email,
        subject=subject,
        html_content=content,
    )

    try:
        sendgrid = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sendgrid.send(message)
        current_app.logger.info(response.status_code)
        current_app.logger.info("✅  Email sent successfully!")
        return True

    except Exception as e:
        current_app.logger.error(f"⚠️  Error sending email: {e}")
        return False
