import html
def sanitize_text(text: str) -> str:
    if text is None:
        return ''
    # minimal sanitization: escape HTML to avoid trivial XSS
    return html.escape(str(text))

