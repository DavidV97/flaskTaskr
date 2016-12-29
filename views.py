from flask import Flask, render_template, request, session, redirect, url_for, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)

app.config.from_object('_config')


def connectDataBase():
    return sqlite3.connect(app.config['DATABASE_PATH'])


def login_reqired(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('logIn'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def logIn():
    error = None
    statusCode = 200

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or\
                request.form['password'] != app.config['PASSWORD']:

            error = 'Invalid Credentials.Plese try again.'
            statusCode = 401

        else:
            session['logged_in'] = True
            return redirect(url_for('main'))

    if request.method == 'GET':
        if 'logged_in' in session:
            return redirect(url_for('main'))

    return render_template('login.html', error=error), statusCode


@app.route('/main')
@login_reqired
def main():
    return render_template('main.html', posts=[])


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('logIn'))
