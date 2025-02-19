# Smart Home API

~~Due to SCC maintainance, the users part and github actions is not yet added.~~



## **Overview**
The storage part is not yet implemented. Only error messages, input validation and endpoints are defined.

This documentation took this [repo](https://github.com/lgc-NB2Dev/YetAnotherPicSearch) as reference.

ChatGPT-o1 model is used for generating code. (AI not invloved in designing)

Github aciton included for automatically running `test_app.py`.
### **Features:**
- **Create (Add)**: Add houses, rooms, devices, and users.
- **Delete (Remove)**: Remove specified resources.
- **Update (Modify)**: Update existing resources.
- **Query (Retrieve)**: Fetch information about resources.

All API endpoints use JSON format for data transmission. (storage is not yet implemented)

---

## **1. House API**
### **1.1 Add a House**
- **Endpoint**: `POST /house/add`
- **Function**: Add a new house.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `name` | `string` | ✅ | House name |
  | `lat` | `float` | ✅ | Latitude (-90 to 90) |
  | `lon` | `float` | ✅ | Longitude (-180 to 180) |
  | `addr` | `string` | ✅ | Address |
  | `uid` | `string` | ✅ | Unique identifier |
  | `floors` | `int` | ✅ | Number of floors (must be positive) |
  | `size` | `int` | ✅ | House size (must be positive) |

- **Example Request:**
  ```json
  {
    "name": "Seaside Villa",
    "lat": 30.5,
    "lon": 120.1,
    "addr": "Some addr",
    "uid": "house001",
    "floors": 3,
    "size": 200
  }
  ```

- **Success Response:**
  ```json
  {
    "message": "House added successfully"
  }
  ```

- **Error Example (Missing Parameter):**
  ```json
  {
    "error": "Missing required parameter: size"
  }
  ```

---

### **1.2 Remove a House**
- **Endpoint**: `POST /house/remove`
- **Function**: Remove a specified house.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `uid` | `string` | ✅ | House UID to be deleted |

- **Example Request:**
  ```json
  {
    "uid": "house001"
  }
  ```

- **Success Response:**
  ```json
  {
    "message": "House with uid=house001 removed"
  }
  ```

---

### **1.3 Update House Information**
- **Endpoint**: `POST /house/update`
- **Function**: Update an existing house.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `uid` | `string` | ✅ | Target house UID |
  | `name` | `string` | ❌ | (Optional) New house name |
  | `lat` | `float` | ❌ | (Optional) New latitude |
  | `lon` | `float` | ❌ | (Optional) New longitude |
  | `addr` | `string` | ❌ | (Optional) New address |
  | `floors` | `int` | ❌ | (Optional) New number of floors |
  | `size` | `int` | ❌ | (Optional) New house size |

- **Example Request:**
  ```json
  {
    "uid": "house001",
    "name": "HouseNo1"
  }
  ```

- **Success Response:**
  ```json
  {
    "message": "House with uid=house001 updated"
  }
  ```

---

### **1.4 Query Houses**
- **Endpoint**: `POST /house/query`
- **Function**: Query houses based on parameters.
- **Request Parameters (JSON or Query String)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `uid` | `string` | ❌ | (Optional) Query by UID |
  | `name` | `string` | ❌ | (Optional) Query by name |
  | `lat` | `float` | ❌ | (Optional) Query by latitude |
  | `lon` | `float` | ❌ | (Optional) Query by longitude |

- **Example Request (GET):**
  ```
  GET /house/query?uid=house001
  ```

- **Success Response:**
  ```json
  {
    "message": "House query result",
    "query_params": {
      "uid": "house001"
    }
  }
  ```

---

## **2. Room Management (Room API)**
### **2.1 Add a Room**
- **Endpoint**: `POST /room/add`
- **Function**: Add a new room.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `name` | `string` | ✅ | Room name |
  | `belong_to_house` | `string` | ✅ | UID of the house it belongs to |
  | `size` | `int` | ✅ | Room size |
  | `floor` | `int` | ✅ | Floor number |

---

## **3. Device Management (Device API)**
### **3.1 Add a Device**
- **Endpoint**: `POST /device/add`
- **Function**: Add a new device.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `name` | `string` | ✅ | Device name |
  | `belong_to_room` | `string` | ✅ | Room UID it belongs to |
  | `type` | `string` | ✅ | Device type |

---

## **4. User Management (Users API)**
### **4.1 Add a User**
- **Endpoint**: `POST /users/add`
- **Function**: Add a new user.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `user_id` | `string` | ✅ | Unique user ID |
  | `name` | `string` | ✅ | User name |

---

## **5. House-User Relationship (House-User API)**
### **5.1 Link User to House**
- **Endpoint**: `POST /house-user/add`
- **Function**: Create a relationship between a user and a house.
- **Request Parameters (JSON)**:

  | Parameter | Type | Required | Description |
  |-----------|------|----------|-------------|
  | `user_id` | `string` | ✅ | User ID |
  | `house_uid` | `string` | ✅ | House UID |

---

## **Error Responses**
- **Missing Parameter**
  ```json
  {
    "error": "Missing required parameter: name"
  }
  ```
- **Invalid Data Type**
  ```json
  {
    "error": "Invalid 'lat' or 'lon': must be valid floating-point numbers"
  }
  ```

---

