import requests
from bs4 import BeautifulSoup
from utils import truncate_text

def fetch_website_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Error fetching the website: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove scripts and styles
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()

    # Extract text from 
    text_parts = []
    for tag in soup.find_all(['p', 'li', 'div', 'span']):
        text = tag.get_text(strip=True)
        if text:
            text_parts.append(text)

    full_text = '\n'.join(text_parts)
    return truncate_text(full_text) 
