def truncate_text(text, max_chars=3000):
    """Trims text to fit within model token limits."""
    return text[:max_chars]
