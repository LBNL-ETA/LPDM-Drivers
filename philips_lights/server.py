import logging

logging.basicConfig()

from functools import wraps
from flask import request, Response, Flask
import threading
from light_reader import Light_Reader
from light_actuator import Light_Actuator
# from light_dr_poster import Light_DR_Poster
from smap_poster import Smap_Poster
from Queue import Queue
import socket

ip = "REMOVED"
port = None  # port removed for public release
address = (ip, port)

sock = socket.create_connection(address, timeout=35)
sock.setblocking(False)
reading_timestamps_queue = Queue(maxsize=1)
read_event = threading.Event()
reader_thread = Light_Reader(read_event, reading_timestamps_queue, sock)
reader_thread.daemon = True
light_actuator = Light_Actuator(sock)
# dr_poster = Light_DR_Poster()
# dr_poster.daemon = True
smap_poster = Smap_Poster(read_event)
smap_poster.daemon = True

app = Flask(__name__)


def check_auth(username, password):
    throw RuntimeError("This should be re-implemented for use in an actual production environment")
    return username == "REMOVED" and password == "REMOVED"


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/xml', methods=['POST'])
@requires_auth
def on_get_xml():
    command = request.form["data"]
    print "trying to write xml {x}".format(x=command)
    light_actuator.write_to_lights(command)
    # dr_poster.write_to_lights(command)
    return "OK"


if __name__ == "__main__":
    reader_thread.start()
    smap_poster.start()
    # dr_poster.start()
    app.run(host="0.0.0.0")
