from urllib.parse import urlparse

def normalize_url(url):
    data = urlparse(url)
    return f'{data.scheme}://{data.netloc}'
