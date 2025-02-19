import pytest
from app import app

@pytest.fixture
def client():
    """
    Pytest fixture to create a Flask test client.
    This allows sending requests to the Flask app
    without running a real server.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

##################################
# HOUSE TESTS
##################################
def test_house_add_success(client):
    payload = {
        "name": "My House",
        "lat": 45.0,
        "lon": 100.0,
        "addr": "123 Test St",
        "uid": "unique-123",
        "floors": 2,
        "size": 100
    }
    response = client.post('/house/add', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "House added successfully."

def test_house_add_missing_field(client):
    # Missing 'lat'
    payload = {
        "name": "My House",
        "lon": 100.0,
        "addr": "123 Test St",
        "uid": "unique-123",
        "floors": 2,
        "size": 100
    }
    response = client.post('/house/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'lat' is required." in data["error"]

def test_house_add_invalid_lat(client):
    # lat out of range
    payload = {
        "name": "My House",
        "lat": 999,  # invalid
        "lon": 100.0,
        "addr": "123 Test St",
        "uid": "unique-123",
        "floors": 2,
        "size": 100
    }
    response = client.post('/house/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "out of range" in data["error"]

def test_house_remove_success(client):
    payload = {
        "uid": "unique-123"
    }
    response = client.post('/house/remove', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "House removed successfully."

def test_house_remove_missing_uid(client):
    payload = {}
    response = client.post('/house/remove', json=payload)
    assert response.status_code == 400
    # data = response.get_json()
    # assert "'uid' is required." in data["error"]

def test_house_update_success(client):
    # Only 'uid' is required to identify the house,
    # and we optionally update other fields
    payload = {
        "uid": "unique-123",
        "lat": 40.0,
        "lon": -70.0,
        "floors": 3
    }
    response = client.post('/house/update', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "House updated successfully."

def test_house_update_missing_uid(client):
    payload = {
        "lat": 40.0,
        "lon": -70.0
    }
    response = client.post('/house/update', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'uid' is required." in data["error"]

def test_house_query_success(client):
    # The query endpoint doesn't strictly require any fields;
    # we can just test it returns status 200 and some default data structure.
    payload = {"name": "Test House"}
    response = client.post('/house/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "House query success."
    assert isinstance(data["data"], list)

##################################
# ROOM TESTS
##################################
def test_room_add_success(client):
    payload = {
        "name": "Living Room",
        "belong_to_house": "house-123",
        "size": 50,
        "floor": 1
    }
    response = client.post('/room/add', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Room added successfully."

def test_room_add_missing_field(client):
    payload = {
        # Missing 'name'
        "belong_to_house": "house-123",
        "size": 50,
        "floor": 1
    }
    response = client.post('/room/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'name' is required." in data["error"]

def test_room_remove_success(client):
    payload = {
        "name": "Living Room",
        "belong_to_house": "house-123"
    }
    response = client.post('/room/remove', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Room removed successfully."

def test_room_remove_missing_field(client):
    payload = {
        "name": "Living Room"
        # Missing 'belong_to_house'
    }
    response = client.post('/room/remove', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'belong_to_house' is required." in data["error"]

def test_room_update_success(client):
    payload = {
        "name": "Living Room",
        "belong_to_house": "house-123",
        "size": 60  # optional field
    }
    response = client.post('/room/update', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Room updated successfully."

def test_room_update_missing_field(client):
    payload = {
        # Missing 'name'
        "belong_to_house": "house-123"
    }
    response = client.post('/room/update', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'name' is required." in data["error"]

def test_room_query_success(client):
    payload = {"name": "Living Room"}
    response = client.post('/room/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Room query success."
    assert isinstance(data["data"], list)

##################################
# DEVICE TESTS
##################################
def test_device_add_success(client):
    payload = {
        "name": "Thermostat",
        "belong_to_room": "room-123",
        "type": "temperature_sensor"
    }
    response = client.post('/device/add', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Device added successfully."

def test_device_add_missing_field(client):
    payload = {
        "name": "Thermostat",
        # Missing "belong_to_room"
        "type": "temperature_sensor"
    }
    response = client.post('/device/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'belong_to_room' is required." in data["error"]

def test_device_remove_success(client):
    payload = {
        "name": "Thermostat",
        "belong_to_room": "room-123"
    }
    response = client.post('/device/remove', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Device removed successfully."

def test_device_remove_missing_field(client):
    payload = {
        "name": "Thermostat"
        # Missing "belong_to_room"
    }
    response = client.post('/device/remove', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'belong_to_room' is required." in data["error"]

def test_device_update_success(client):
    payload = {
        "name": "Thermostat",
        "belong_to_room": "room-123",
        "type": "humidity_sensor"  # optional
    }
    response = client.post('/device/update', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Device updated successfully."

def test_device_update_missing_field(client):
    payload = {
        "name": "Thermostat"
        # Missing "belong_to_room"
    }
    response = client.post('/device/update', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'belong_to_room' is required." in data["error"]

def test_device_query_success(client):
    payload = {"name": "Thermostat"}
    response = client.post('/device/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Device query success."
    assert isinstance(data["data"], list)

##################################
# DEVICE SENSOR REPORT TESTS
##################################
def test_device_sensor_report_success(client):
    payload = {
        "name": "Thermostat",
        "belong_to_room": "room-123",
        "sensor_type": "temperature",
        "sensor_value": 22.5
    }
    response = client.post('/device/sensor_report', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Sensor data received successfully."

def test_device_sensor_report_missing_field(client):
    payload = {
        "name": "Thermostat",
        "belong_to_room": "room-123",
        # Missing "sensor_type"
        "sensor_value": 22.5
    }
    response = client.post('/device/sensor_report', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'sensor_type' is required." in data["error"]

##################################
# USERS TESTS
##################################
def test_users_add_success(client):
    payload = {
        "user_id": "user123",
        "name": "Alice",
        "email": "alice@example.com"
    }
    response = client.post('/users/add', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "User added successfully."

def test_users_add_missing_field(client):
    payload = {
        "user_id": "user123",
        # Missing "name" or "email"
        "email": "alice@example.com"
    }
    response = client.post('/users/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    # assert "'name' is required." in data["error"]

def test_users_remove_success(client):
    payload = {"user_id": "user123"}
    response = client.post('/users/remove', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User removed successfully."

def test_users_remove_missing_field(client):
    payload = {}
    response = client.post('/users/remove', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    # assert "'user_id' is required." in data["error"]

def test_users_update_success(client):
    payload = {
        "user_id": "user123",
        "name": "New Name"
    }
    response = client.post('/users/update', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User updated successfully."

def test_users_update_missing_field(client):
    payload = {
        "name": "New Name"
        # Missing 'user_id'
    }
    response = client.post('/users/update', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    # assert "'user_id' is required." in data["error"]

def test_users_query_success(client):
    payload = {"user_id": "user123"}
    response = client.post('/users/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Users query success."
    assert isinstance(data["data"], list)

##################################
# HOUSE-USER RELATIONSHIP TESTS
##################################
def test_house_user_add_success(client):
    payload = {
        "house_uid": "house-123",
        "user_id": "user123"
    }
    response = client.post('/house_user/add', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "House-User relation added successfully."

def test_house_user_add_missing_field(client):
    payload = {
        "house_uid": "house-123"
        # Missing "user_id"
    }
    response = client.post('/house_user/add', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'user_id' is required." in data["error"]

def test_house_user_remove_success(client):
    payload = {
        "house_uid": "house-123",
        "user_id": "user123"
    }
    response = client.post('/house_user/remove', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "House-User relation removed successfully."

def test_house_user_remove_missing_field(client):
    payload = {
        "house_uid": "house-123"
        # Missing "user_id"
    }
    response = client.post('/house_user/remove', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "'user_id' is required." in data["error"]

def test_house_user_query_success(client):
    payload = {"house_uid": "house-123"}
    response = client.post('/house_user/query', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "House-User relation query success."
    assert isinstance(data["data"], list)
