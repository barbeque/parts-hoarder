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

if __name__ == '__main__':
  app.run()
