import psycopg2
from flask import current_app, g
from flask.cli import with_appcontext
import click
from datetime import datetime
from os import path, environ


def get_db():
    db_url = environ.get('DATABASE_URL')
    try:
        if 'db' not in g:
            g.db = psycopg2.connect(db_url)
        return g.db
    except RuntimeError:
        db = psycopg2.connect(db_url)
        return db


def close_db(db_conn=None):
    try:
        db = g.pop('db', None)
        if db is not None:
            db.close()
    except RuntimeError:
        try:
            db_conn.close()
        except:
            print('db close error')


def select_all_data():
    db = get_db()
    cursor = db.cursor()
    all_data = cursor.execute('SELECT id, location, latitude, longitude, created FROM data;')
    all_data = cursor.fetchall()
    db.commit()
    cursor.close()
    # db.close()
    close_db(db)
    return all_data


def insert_into_data(location, latitude, longitude):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO data (location, latitude, longitude, created) VALUES (%s, %s, %s, %s)",
        (location, latitude, longitude, datetime.utcnow()))
    db.commit()
    cursor.close()
    # db.close()
    close_db(db)
    return True


def select_map_data():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT latitude, longitude FROM data')
    all_data = cursor.fetchall()
    map_data = []
    for each in all_data:
        # map_data.append([each['latitude'], each['longitude']])
        map_data.append([each[0], each[1]])
    cursor.close()
    # db.close()
    close_db(db)
    return map_data


def init_app(app):
    app.teardown_appcontext(close_db)
