import re
import cgi

def normalize_email(email):
    return str(email).strip().lower()

def escape_html(content):

    def __allow_bold_text(text):
        regex = r'(\*{2})(.+?)\1'
        substr = '''<strong>\\2</strong>'''
        return re.sub(regex, substr, text, 0, re.MULTILINE)


    def __allow_links(text):
        # https://regex101.com
        regex = r'&lt;((?:[f]|[h][t])[t][p][s]?://[-:/~.&?=#%\w]*)&gt;'
        substr = '''<a class="user-link" href="\\1" target="_blank">\\1</a>'''
        return re.sub(regex, substr, text, 0, re.MULTILINE | re.IGNORECASE)

    # Prevent XSS attacks.
    escaped = cgi.escape(content,quote=True)
    escaped = escaped.replace("'", "&apos;")

    escaped = __allow_links(escaped)
    escaped = __allow_bold_text(escaped)

    return escaped

