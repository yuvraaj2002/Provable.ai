import requests
from pathlib import Path
from app.core.config import settings


def send_brevo_email(recipient_email: str, recipient_name: str, subject: str, html_content: str):
    """
    Send email using Brevo API via requests library.
    Matches the curl request structure exactly.
    
    Args:
        recipient_email: Email address of the recipient
        recipient_name: Name of the recipient
        subject: Email subject
        html_content: HTML content of the email
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    url = "https://api.brevo.com/v3/smtp/email"
    
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    payload = {
        "sender": {
            "name": settings.SENDER_NAME,
            "email": settings.SENDER_EMAIL
        },
        "to": [
            {
                "email": recipient_email,
                "name": recipient_name
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
        "headers": {
            "X-Mailin-custom": "custom_header_1:custom_value_1|custom_header_2:custom_value_2|custom_header_3:custom_value_3",
            "charset": "iso-8859-1"
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # Parse response if needed
        if response.status_code == 201:
            response_data = response.json()
            message_id = response_data.get("messageId", "Unknown")
            print(f"Success! Message ID: {message_id}")
            return True
        else:
            print(f"Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Exception when calling Brevo API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text}")
        return False


def load_email_template(template_name: str) -> str:
    """
    Load an email template from the templates/emails directory.
    """
    # Get the base directory (app directory)
    base_dir = Path(__file__).parent.parent
    template_path = base_dir / "templates" / "emails" / template_name
    
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def render_email_template(template_name: str, **kwargs) -> str:
    """
    Load and render an email template with provided variables.

    Args:
        template_name: Name of the template file
        **kwargs: Variables to replace in the template (e.g., name="John", verification_link="...")
        
    Returns:
        str: Rendered HTML content
    """
    template_content = load_email_template(template_name)
    # Use safe string replacement to avoid issues with CSS curly braces
    # Replace only the specific placeholders we need
    result = template_content
    for key, value in kwargs.items():
        placeholder = "{" + key + "}"
        result = result.replace(placeholder, str(value))
    return result


def send_verification_email(recipient_email: str, recipient_name: str, verification_token: str) -> bool:
    """
    Send verification email to a user.
    
    Args:
        recipient_email: Email address of the recipient
        recipient_name: Name of the recipient
        verification_token: JWT token for email verification
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    # Construct verification link
    verification_link = f"{settings.FRONTEND_BASE_URL}/verify-email?token={verification_token}"
    
    # Render the email template
    html_content = render_email_template(
        "verification_email.html",
        name=recipient_name,
        verification_link=verification_link
    )
    
    # Send the email
    subject = "Verify Your Email Address - AI Safety"
    return send_brevo_email(recipient_email, recipient_name, subject, html_content)
