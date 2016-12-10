from flask import request, url_for, jsonify, Response, make_response
from flask.ext.api import FlaskAPI, status, exceptions
import xml.etree.ElementTree as ET
import json
import numpy as np
import matplotlib.pyplot as plt
import random
import os.path
import matplotlib.patches as patch
import pylab as pl
#co2_patch = patch.Patch(color='b', label='The output data')
#so2_patch = patch.Patch(color='y', label='The output data')
#no2_patch = patch.Patch(color='r', label='The output data')

tree = ET.parse('nomenclator.xml')
root = tree.getroot()
app = FlaskAPI(__name__, static_url_path='/static')

CO2 = {
    44.9636: 8.56,
    0.894261: 10.32,
    67.5422: 11.04,
    1010.25: 13.00,
    1.4061: 13.56,
    6.61613: 14.03,
    7.2167: 17.23,
    13.069: 17.56,
    10.2905: 19.23,
    2.45465: 20.12,
    2.53499: 20.45,
    58.1173: 21.53,
    1.02819: 22.12,
    262.751: 22.25,
    0.2: 22.56
}
NO2 = {
    6.66051: 40.4345, 8.28019: 42.99192, 9.45969: 29.07984, 13.75428: 7.67093, 17.71887: 36.0379, 18.30747: 14.76178, 19.31711: 26.04555, 20.27711: 31.81935, 21.10296: 8.46923, 23.76183: 27.40776, 25.53115: 12.27045, 26.79637: 34.15272, 47.88958: 6.71289, 28.07569: 21.84888, 30.81138: 30.96105, 31.85429: 45.73897, 37.12345: 11.74809, 38.62947: 4.06257, 17.32156: 25.9291, 40.92408: 8.55236, 47.65939: 41.52663, 19.55517: 2.30449, 30.09286: 12.39989, 9.2645: 15.1266, 20.28064: 39.23015}
SO2 = {
    34.9636: 8.56,
    0.894261: 1.32,
    97.5422: 11.04,
    100.25: 3.00,
    13.4061: 13.56,
    64.61613: 14.03,
    71.2167: 17.23,
    5.069: 17.56,
    1.2905: 19.23,
    2.45465: 30.12,
    2.53499: 40.45,
    53.1173: 21.53,
    1.02819: 62.12,
    22.751: 22.25,
    0.2: 22.56
}

def note_repr(key):
    return {
        'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
        #'text': notes[key]
    }
def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)

@app.route('/CO2')
def CO2info():
    lists = sorted(CO2.items())
    x, y = zip(*lists)
 #   plt.legend(hendels=[co2_patch])
    plt.clf()
    plt.scatter(y,x, color='b')
    plt.ylim([0, 300])
    plt.xlim([0, 24])
    plt.xlabel("Ora(h:m)")
    plt.ylabel("Cantitate(g/l)")
    plt.savefig('/home/alexandru/HACKSOCIETY/static/map.png')
    content = get_file('templates/output.html')
    return Response(content, mimetype="text/html")


@app.route('/NO2')
def NO2info():

    lists = sorted(NO2.items())
    x, y = zip(*lists)
    plt.clf()
    plt.scatter(y,x, color='r')
    plt.ylim([0, 300])
    plt.xlim([0, 24])
    plt.xlabel("Ora(h:m)")
    plt.ylabel("Cantitate(g/l)")
    plt.savefig('/home/alexandru/HACKSOCIETY/static/map.png')
    content = get_file('templates/output.html')
    return Response(content, mimetype="text/html")

@app.route('/SO2')
def SO2info():

    lists = sorted(SO2.items())
    x, y = zip(*lists)
    plt.clf()
    plt.scatter(y,x, color='y')
    plt.ylim([0, 300])
    plt.xlim([0, 24])
    plt.xlabel("Ora(h:m)")
    plt.ylabel("Cantitate(g/l)")
    plt.savefig('/home/alexandru/HACKSOCIETY/static/map.png')
    content = get_file('templates/output.html')
    return Response(content, mimetype="text/html")



@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/air')
def api_co2():
    co2js = json.dumps(CO2)
    resp = Response(co2js, status=200, mimetype='application/json')
    if 'elem' in request.args:
        return resp

@app.route("/air", methods=['GET', 'POST'])
def notes_list():
    """
    List or create notes.
    """
    if request.method == 'POST':
        note = str(request.data.get('text', ''))
        #idx = max(notes.keys()) + 1
        #notes[idx] = note
        return note_repr(idx), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [note_repr(idx) for idx in sorted(notes.keys())]


@app.route("/<int:key>/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):
    """
    Retrieve, update or delete note instances.
    """
    if request.method == 'PUT':
        note = str(request.data.get('text', ''))
        #notes[key] = note
        return note_repr(key)

    elif request.method == 'DELETE':
        #notes.pop(key, None)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
   # if key not in notes:
    #    raise exceptions.NotFound()
    return note_repr(key)


if __name__ == "__main__":
    app.run(debug=True)
