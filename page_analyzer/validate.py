import validators

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