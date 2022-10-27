import datetime

from flask import Flask, render_template, session, redirect, url_for, request, abort
from random import choice

from config import Config
import os
from pprint import pprint
app = Flask(__name__)

# app.config['SECRET_KEY'] = 'dhme;kghjanrkael/jgbuilarelkjmgbipuehjmghiotrkjhtoikle'
app.config.from_object(Config)
#print(*app.config.items(), sep='\n')
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flask.db')))
#print(*app.config.items(), sep='\n')
title = ['Flask', 'Как интересно', 'Ваши предложения', 'Химия', '']
menu = [{'name': 'Главная', 'url': '/'}, {'name': 'Помощь', 'url': 'help'}, {'name': 'О приложении', 'url': 'about'},
        {'name': 'Таблица', 'url': 'table'}, {'name': 'Авторизация', 'url': 'login'}]


@app.route('/index/')
@app.route('/')
def hello():
    user = {'username': 'yURA'}
    return render_template('index.html', user=user, title=choice(title), menu=menu)


@app.route('/help')
def help():
    return render_template('help.html', title='Помощь', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='IT CUB', menu=menu)


# @app.route('/<int:id>')
# def users(id):
#     return f'<h1>Ваш порядковый номер {id} </h1>'


@app.route('/profile/<user>')
def profile(user):
    if 'user_logged' not in session or session['user_logged'] != user:
        abort(401)
    return render_template('people.html', name=user)


# @app.route('/profile/<username>')
# def profile(username):
#     return f'hello {username}'


@app.route('/table')
def t1():
    return render_template('table.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена', menu=menu)


@app.errorhandler(401)
def profile_error(error):
    return f"<h1>сначала авторизуйтесь </h1> {error}"


app.permanent_session_lifetime = datetime.timedelta(seconds=160)


@app.route('/login', methods=["POST", "GET"])
def login():
    print(session)
    users = {'Gog': '111', 'VOV': '123', 'bob': '334', '1': '1'}

    if 'user_logged' in session:
        print(session['user_logged'])
        return redirect(url_for('profile', user=session['user_logged']))
    elif request.method == 'POST' and request.form['username'] in users and request.form['password'] in users[
        request.form['username']]:
        session['user_logged'] = request.form['username']
        return redirect(url_for('profile', user=session['user_logged']))
    return render_template('login.html', title="Авторизация")


@app.route('/visits-counter')
def visits():
    session.permanent = True
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    return "Total visits: {}".format(session.get('visits'))


@app.route('/delete-visits')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'


@app.route('/delete_exit')
def delete_exit():
    if session.get('user_logged', False):
        del session['user_logged']
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
