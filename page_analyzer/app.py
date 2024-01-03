import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    request,
    flash,
    get_flashed_messages,
    url_for,
    redirect
)

from page_analyzer.validate import validate
from page_analyzer.normalize import normalize_url

from page_analyzer.db import (
    get_data_by_name,
    get_data_by_id,
    get_all_urls,
    get_checks_by_id,
    add_url,
    add_check,
)

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    """
        Show start page
    """
    return render_template(
        'index.html',
        url='',
        messages=[]
    )


@app.get('/urls')
def get_urls():
    """
        Show all urls
    """
    urls = get_all_urls()
    return render_template(
        'urls.html',
        urls=urls
    )


@app.post('/urls')
def post_new_url():
    """
        Get the url from the form.
        Check for compliance with validation conditions.
        If the url is invalid, display an error message.
        If the url is valid - query db for the existence of a similar url.
        If it exists - inform about its existence.
        If it does not exist - write the data into the db.
        Redirect to the page of the corresponding url.
    """
    url = request.form.to_dict().get('url')
    errors = validate(url)
    messages = []
    if errors:
        for error in errors:
            flash(error, 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template(
            'index.html',
            url=url,
            messages=messages
        ), 422

    url = normalize_url(url)
    existing = get_data_by_name(url)
    if existing:
        flash('Страница уже существует', 'info')
        id = existing.id
    else:
        flash('Страница успешно добавлена', 'success')
        id = add_url(url)
    return redirect(url_for('get_url_id', id=id), 302)


@app.get('/urls/<id>')
def get_url_id(id):
    """
        Show choiced url's page
    """
    url = get_data_by_id(id)
    checks = get_checks_by_id(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'url.html',
        url=url,
        messages=messages,
        checks=checks[::-1]
    )


@app.post('/urls/<id>/checks')
def post_checks(id):
    add_check(id)
    return redirect(url_for('get_url_id', id=id), 302)


@app.errorhandler(404)
def page_not_found():
    return render_template('error/404.html'), 404
