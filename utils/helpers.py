import re
from urllib.parse import urlparse

def get_platform(url: str) -> str:
    """Determine the platform from the URL."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    if any(x in domain for x in ['youtube.com', 'youtu.be']):
        return 'youtube'
    elif 'tiktok.com' in domain:
        return 'tiktok'
    elif 'pinterest.com' in domain:
        return 'pinterest'
    else:
        return 'unknown'

def is_valid_url(url: str) -> bool:
    """Check if the URL is valid."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.match(url))