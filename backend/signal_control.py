# backend/signal_control.py

def control_traffic_signal(ambulance_pos, intersections, traffic_status):
    """
    Simple mock logic: If ambulance is near an intersection and traffic is clear,
    change the signal to green.
    """
    for inter in intersections:
        distance = ((ambulance_pos[0] - inter["location"][0]) ** 2 + 
                    (ambulance_pos[1] - inter["location"][1]) ** 2) ** 0.5
        distance_meters = distance * 111000  # rough conversion lat/lng → meters

        if distance_meters < 300:  # Within 300m
            if traffic_status[inter["id"]] == "clear":
                inter["signal"] = "green"
            else:
                inter["signal"] = "red"
