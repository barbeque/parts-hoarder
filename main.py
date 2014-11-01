from flask import Flask, request, session, g, redirect, url_for, \
  abort, render_template, flash
import sqlite3
from contextlib import closing

# db config
DATABASE = '/tmp/hoarder.db'
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'password'
SECRET_KEY = 'my secret key'

# create app
app = Flask(__name__)
app.config.from_object(__name__) # eat above config
# todo: load secret key from file (NOT COMMITTED TO GITHUB)

def init_db():
  with closing(connect_db()) as db:
    with app.open_resource('schema.sql', mode = 'r') as schema:
      db.cursor().executescript(schema.read())
    db.commit()

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

# db bindings time
@app.before_request
def before_request():
    g.db = connect_db()
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_parts():
    cursor = g.db.execute('select id, name from parts order by id desc')
    parts = [dict(title = row[0], text = row[1]) for row in cursor.fetchall()]
    return render_template('show_parts.html', parts = parts)

@app.route('/add', methods = ['POST'])
def add_part():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into parts (name) values (?)', [request.form['name']])
    g.db.commit()
    flash('new part successfully posted')
    return redirect(url_for('show_parts'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
            error = 'invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'invalid password.'
        else:
            session['logged_in'] = True
            flash('you are logged in')
            return redirect(url_for('show_parts'))
    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None) # pop logged_in, replace with None
    flash('logged out')
    return redirect(url_for('show_parts'))


# always at the bottom...
if __name__ == '__main__':
  app.run()
