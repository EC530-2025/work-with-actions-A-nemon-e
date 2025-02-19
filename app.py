from flask import Flask, request, jsonify

app = Flask(__name__)

##################################
# Utility validation helpers
##################################
def check_required_fields(data, required_fields):
    """
    Check if all required fields are in the data.
    Returns (True, None) if all exist,
    otherwise (False, error_msg).
    """
    for field in required_fields:
        if field not in data:
            return False, f"'{field}' is required."
    return True, None

def make_error_response(msg, code=400):
    """
    Returns a JSON response with an 'error' key and the provided status code (default 400).
    """
    return jsonify({"error": msg}), code

def validate_lat_lon(lat, lon):
    """
    Validate latitude/longitude is numeric and within usual bounds:
      - lat in [-90, 90]
      - lon in [-180, 180]
    Raises ValueError if invalid.
    """
    # Check types
    if not isinstance(lat, (int, float)):
        raise ValueError("'lat' must be a number.")
    if not isinstance(lon, (int, float)):
        raise ValueError("'lon' must be a number.")

    # Check ranges
    if lat < -90 or lat > 90:
        raise ValueError("'lat' out of range (-90 to 90).")
    if lon < -180 or lon > 180:
        raise ValueError("'lon' out of range (-180 to 180).")

def validate_int_positive(value, field_name):
    """
    Validate a field is an integer > 0. Raises ValueError if invalid.
    """
    try:
        val = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"'{field_name}' must be an integer.")

    if val <= 0:
        raise ValueError(f"'{field_name}' must be greater than 0.")
    return val

##################################
# HOUSE
##################################
@app.route('/house/add', methods=['POST'])
def house_add():
    """
    Required JSON fields:
      - name
      - lat
      - lon
      - addr
      - uid
      - floors
      - size
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "lat", "lon", "addr", "uid", "floors", "size"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    # Validate lat/lon
    try:
        validate_lat_lon(data["lat"], data["lon"])
    except ValueError as e:
        return make_error_response(str(e))

    # Validate floors and size
    try:
        floors = validate_int_positive(data["floors"], "floors")
        size = validate_int_positive(data["size"], "size")
    except ValueError as e:
        return make_error_response(str(e))

    # If everything is OK:
    return jsonify({"message": "House added successfully."}), 201

@app.route('/house/remove', methods=['POST'])
def house_remove():
    """
    Required JSON fields:
      - uid
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["uid"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "House removed successfully."}), 200

@app.route('/house/update', methods=['POST'])
def house_update():
    """
    Required JSON fields:
      - uid (not modifiable)
    Optional fields:
      - name
      - lat
      - lon
      - addr
      - floors
      - size
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    # Must have uid
    if "uid" not in data:
        return make_error_response("'uid' is required.")

    # Validate lat/lon if provided
    if "lat" in data or "lon" in data:
        # Both must be present if updating lat/lon
        if "lat" not in data or "lon" not in data:
            return make_error_response("Both 'lat' and 'lon' must be provided if updating them.")
        try:
            validate_lat_lon(data["lat"], data["lon"])
        except ValueError as e:
            return make_error_response(str(e))

    # Validate floors if provided
    if "floors" in data:
        try:
            _ = validate_int_positive(data["floors"], "floors")
        except ValueError as e:
            return make_error_response(str(e))

    # Validate size if provided
    if "size" in data:
        try:
            _ = validate_int_positive(data["size"], "size")
        except ValueError as e:
            return make_error_response(str(e))

    return jsonify({"message": "House updated successfully."}), 200

@app.route('/house/query', methods=['POST'])
def house_query():
    """
    Can pass 0 or more of:
      - name
      - lat
      - lon
      - addr
      - uid
    in the JSON body.
    """
    data = request.get_json(force=True, silent=True) or {}
    # Typically you'd filter storage based on these params
    return jsonify({"message": "House query success.", "data": []}), 200

##################################
# ROOM
##################################
@app.route('/room/add', methods=['POST'])
def room_add():
    """
    Required JSON fields:
      - name
      - belong_to_house
      - size
      - floor
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_house", "size", "floor"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    # Example additional checks
    try:
        size = validate_int_positive(data["size"], "size")
        floor = validate_int_positive(data["floor"], "floor")
    except ValueError as e:
        return make_error_response(str(e))

    return jsonify({"message": "Room added successfully."}), 201

@app.route('/room/remove', methods=['POST'])
def room_remove():
    """
    Required JSON fields:
      - name
      - belong_to_house
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_house"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "Room removed successfully."}), 200

@app.route('/room/update', methods=['POST'])
def room_update():
    """
    Required JSON fields:
      - name
      - belong_to_house
    Optional fields:
      - size
      - floor
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_house"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    # Validate optional fields
    if "size" in data:
        try:
            _ = validate_int_positive(data["size"], "size")
        except ValueError as e:
            return make_error_response(str(e))

    if "floor" in data:
        try:
            _ = validate_int_positive(data["floor"], "floor")
        except ValueError as e:
            return make_error_response(str(e))

    return jsonify({"message": "Room updated successfully."}), 200

@app.route('/room/query', methods=['POST'])
def room_query():
    """
    Should pass name and belong_to_house in the JSON if needed.
    """
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({"message": "Room query success.", "data": []}), 200

##################################
# DEVICE
##################################
@app.route('/device/add', methods=['POST'])
def device_add():
    """
    Required JSON fields:
      - name
      - belong_to_room
      - type
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_room", "type"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "Device added successfully."}), 201

@app.route('/device/remove', methods=['POST'])
def device_remove():
    """
    Required JSON fields:
      - name
      - belong_to_room
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_room"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "Device removed successfully."}), 200

@app.route('/device/update', methods=['POST'])
def device_update():
    """
    Required JSON fields:
      - name
      - belong_to_room
    Optional fields:
      - type
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_room"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "Device updated successfully."}), 200

@app.route('/device/query', methods=['POST'])
def device_query():
    """
    Can pass name, belong_to_room in the JSON if needed.
    """
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({"message": "Device query success.", "data": []}), 200

##################################
# DEVICE SENSOR REPORT
##################################
@app.route('/device/sensor_report', methods=['POST'])
def device_sensor_report():
    """
    Endpoint to receive sensor data.
    Example required fields (design your own):
      - name
      - belong_to_room
      - sensor_type
      - sensor_value
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["name", "belong_to_room", "sensor_type", "sensor_value"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    # You could also validate sensor_value or sensor_type here
    return jsonify({"message": "Sensor data received successfully."}), 200

##################################
# USERS
##################################
@app.route('/users/add', methods=['POST'])
def users_add():
    """
    Example required JSON fields:
      - user_id
      - name
      - email
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["user_id", "name", "email"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    # Optional example: check for valid email format, etc.
    return jsonify({"message": "User added successfully."}), 201

@app.route('/users/remove', methods=['POST'])
def users_remove():
    """
    Required JSON fields:
      - user_id
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["user_id"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "User removed successfully."}), 200

@app.route('/users/update', methods=['POST'])
def users_update():
    """
    Required JSON fields:
      - user_id
    Optional fields:
      - name
      - email
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    if "user_id" not in data:
        return make_error_response("'user_id' is required.")

    return jsonify({"message": "User updated successfully."}), 200

@app.route('/users/query', methods=['POST'])
def users_query():
    """
    Can pass user_id, name, etc. in the JSON if needed.
    """
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({"message": "Users query success.", "data": []}), 200

##################################
# HOUSE-USER RELATIONSHIP
##################################
@app.route('/house_user/add', methods=['POST'])
def house_user_add():
    """
    Required JSON fields:
      - house_uid
      - user_id
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["house_uid", "user_id"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "House-User relation added successfully."}), 201

@app.route('/house_user/remove', methods=['POST'])
def house_user_remove():
    """
    Required JSON fields:
      - house_uid
      - user_id
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return make_error_response("Invalid or missing JSON.")

    required = ["house_uid", "user_id"]
    valid, error = check_required_fields(data, required)
    if not valid:
        return make_error_response(error)

    return jsonify({"message": "House-User relation removed successfully."}), 200

@app.route('/house_user/query', methods=['POST'])
def house_user_query():
    """
    Can pass house_uid, user_id in the JSON if needed.
    """
    data = request.get_json(force=True, silent=True) or {}
    return jsonify({"message": "House-User relation query success.", "data": []}), 200

##################################
# MAIN
##################################
if __name__ == '__main__':
    app.run(debug=True)
