from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import folium
from datetime import datetime
from geopy.geocoders import Nominatim
import db_pg
from folium.plugins import MarkerCluster
from folium.map import Marker, Tooltip

# TODO_: load data from DB - OK
# TODO_: validate new posted data - partially
# TODO: use cookies to verify if the user already submitted location
# TODO_: display flash message for location validation error/successful location submission - OK
# TODO_: add nickname to form and DB
# TODO_: folium pins with nicknames
# TODO: endpoint for exporting DB data to json

bp = Blueprint('map', __name__)
geolocator = Nominatim(user_agent="pythonista_world_map")


@bp.route('/', methods=('GET', 'POST'))
def index():
    m = folium.Map(location=[20, 0], zoom_start=3)
    points = db_pg.select_map_data()
    nicknames = db_pg.select_nicknames()

    # MarkerCluster(locations=points, popups=nicknames).add_to(m)
    for i in range(len(points)):
        tooltip_ = Tooltip(nicknames[i], permanent=True)
        if nicknames[i] is None:
            Marker(points[i]).add_to(m)
        else:
            Marker(points[i], tooltip=tooltip_).add_to(m)

    map_html = m._repr_html_()
    if request.method == 'POST':
        # TODO: add new point to map in a different color - red or so
        location = request.form['location']
        nickname = request.form['nickname']
        try:
            decoded_location = geolocator.geocode(location)
            db_pg.insert_into_data(location, decoded_location.latitude, decoded_location.longitude, nickname)
            # MarkerCluster(locations=[[decoded_location.latitude, decoded_location.longitude]]).add_to(m)
            # map_html = m._repr_html_()
            flash('location successfully added')
            print('new location: ', location, ', ', decoded_location.latitude,', ', decoded_location.longitude, ', ', datetime.utcnow())
        except AttributeError:
            flash('location not found, try again')
            print('location not found')
        return redirect(url_for('index'))
    return render_template('base.html', map_=map_html)


@bp.route('/map')
def map1():
    m = folium.Map(location=[20, 0], zoom_start=3)
    return m._repr_html_()


@bp.route('/export')
def export():
    data = db_pg.select_all_data()
    # return data
    return render_template('base.html', map_=data)

