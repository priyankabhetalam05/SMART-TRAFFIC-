from flask import Flask, render_template
from flask_socketio import SocketIO
import time
import threading
import eventlet

eventlet.monkey_patch()  # <== Make sure to include this

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

ambulance_route = [
    (12.8729, 80.2261),
    (12.8732, 80.2270),
    (12.8735, 80.2280),
    (12.8750, 80.2300),
    (12.8760, 80.2290)
]

ambulance_pos = ambulance_route[0]

intersections = [
    {"id": 1, "location": (12.8735, 80.2280), "signal": "red"},
    {"id": 2, "location": (12.8750, 80.2300), "signal": "red"},
]

def compute_distance(p1, p2):
    return (((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5) * 111000

def control_traffic_signal(pos):
    for inter in intersections:
        dist = compute_distance(pos, inter["location"])
        inter["signal"] = "green" if dist < 100 else "red"

def simulate_ambulance():
    global ambulance_pos
    for pos in ambulance_route:
        ambulance_pos = pos
        control_traffic_signal(ambulance_pos)

        socketio.emit('update', {
            "ambulance": ambulance_pos,
            "intersections": intersections
        })

        time.sleep(5)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/start_simulation')
def start_simulation():
    threading.Thread(target=simulate_ambulance).start()
    return "Simulation started"

if __name__ == '__main__':
    socketio.run(app, debug=True)
