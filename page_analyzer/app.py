import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    # request,
    # url_for,
    # redirect,
    # flash,
    # get_flashed_messages,
    # session
)

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def main():
    # messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        # messages=messages
    )
