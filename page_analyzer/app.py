import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    # url_for,
    # redirect,
    # session
)

from page_analyzer.validate import validate
from page_analyzer.normalize import normalize_url

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    return render_template(
        'index.html',
        url = '',
        messages = []
    )

@app.get('/urls')
def get_urls():
    return render_template(
        'urls.html',
    )

@app.post('/urls')
def post_new_url():
    url = request.form.to_dict().get('url')
    errors = validate(url)
    messages = []
    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
        'index.html',
        url = url,
        messages = messages
    )






    return render_template(
        'urls.html',
        # messages=messages
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404
