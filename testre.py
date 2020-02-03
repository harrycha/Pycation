import re

urls = r"""
https://www.googl e.com
http://coreyms.com
https://youtube.com
https://www.nasa.gov
"""

pattern = re.compile(r'https?://(www\.)?(\w+\s+\w+)(\.\w+)')

subbed_urls = pattern.sub(r'https://\3', urls)
print(subbed_urls)
