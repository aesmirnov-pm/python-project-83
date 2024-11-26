import os
from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv

from page_analyzer.database import (connection,
                                    get_url_by_name,
                                    add_to_urls,
                                    get_urls)
from page_analyzer.utils import normalize, validate

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.environ.get('DATABASE_URL')


@app.get('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def add_url():
    url = request.form.get('url')
    normalized_url = normalize(url)
    error = validate(normalized_url)
    if error:
        flash(error, 'error')
        return render_template('index.html', user_input=url), 422

    with connection(DATABASE_URL) as conn:
        found_url = get_url_by_name(conn, normalized_url)
        if found_url:
            id = found_url.id
            flash('Страница уже существует', 'success')
        else:
            id = add_to_urls(conn, normalized_url)
            flash('Страница успешно добавлена', 'success')
    return redirect(url_for('show_urls', id=id))


@app.get('/urls')
def show_urls():
    with connection(DATABASE_URL) as conn:
        all_urls = get_urls(conn)

    return render_template('urls.html', all_urls=all_urls)
