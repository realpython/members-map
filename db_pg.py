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


def create_table():
    '''
    created new data table in DB
    :return:
    '''
    db = get_db()
    cursor = db.cursor()
    status = cursor.execute('CREATE TABLE data2 (id SERIAL PRIMARY KEY, location TEXT NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, created TIMESTAMP NOT NULL, nickname TEXT);')
    print('status: ', status)
    db.commit()
    cursor.close()
    close_db(db)


def add_column_to_data():
    '''
    adds empty nickname column to data table
    :return:
    '''
    db = get_db()
    cursor = db.cursor()
    status = cursor.execute('ALTER TABLE data ADD COLUMN nickname TEXT;')
    db.commit()
    cursor.close()
    close_db(db)


def insert_into_data(location, latitude, longitude, nickname):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO data (location, latitude, longitude, created, nickname) VALUES (%s, %s, %s, %s, %s)",
                   (location, latitude, longitude, datetime.utcnow(), nickname))
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


def select_nicknames():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT nickname FROM data')
    db_data = cursor.fetchall()
    nicknames = []
    for each in db_data:
        nicknames.append(each[0])
    cursor.close()
    # db.close()
    close_db(db)
    return nicknames


def init_app(app):
    app.teardown_appcontext(close_db)
