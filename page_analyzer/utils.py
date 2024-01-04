import validators
from bs4 import BeautifulSoup
from urllib.parse import urlparse

MAX_URL_LENGTH = 255


def validate(url):
    errors = []
    if not url:
        errors.append('URL обязателен')
    elif len(url) > MAX_URL_LENGTH:
        errors.append('URL превышает 255 символов')
    elif not validators.url(url):
        errors.append('Некорректный URL')
    return errors


def normalize_url(url):
    data = urlparse(url)
    return f'{data.scheme}://{data.netloc}'


def parse_html(template):
    result = {}
    soup = BeautifulSoup(template, 'html.parser')

    h1 = soup.find('h1')
    title = soup.find('title')
    descr = soup.find('meta', attrs={'name': 'description'})

    result['h1'] = h1.get_text().strip() if h1 else ''
    result['title'] = title.get_text().strip() if title else ''
    result['descr'] = descr.get('content', '').strip() if descr else ''

    return result
