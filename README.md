<!DOCTYPE html>
<html lang="en">
<body>

# VAAYU-Sky-Ops Project

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/skyops.git
cd skyops
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Application

### 4. Navigate to the `src/` Directory
```bash
cd src
```

### 5. Run the Application
```bash
python main.py
```

---

## Running Tests
To run test cases, execute:
```bash
pytest tests/
```

<h1>VAAYU-SkyOps Project Structure</h1>
<pre>
skyops/
│
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── utils/                 (utilities / helper functions)
│   │   ├── config/                (configurations to configure this application)
│   │
│   ├── communication/
│   │   ├── mavlink/       
│   │   │   ├── handler.py         (handles conn-disconn with the vehicle via mavlink)
│   │
│   ├── mission/
│   │   ├── controls/
│   │   │   ├── controller.py      (handles arming/disarming of the vehicle)
│   │   │   ├── motors.py          (handles motion of drones ie yaw pitch roll throttle)
│   │   ├── planner/
│   │       ├── planner.py         (contains custom missions)
│   │       ├── upload.py          (writes the .waypoints file to pixhawk) 
│   │
│   ├── models/                    (contains data model in schematic form)
│   │   ├── telemetry_model.py     (telemetry data model)
│   │
│   ├── routes/
│   │   ├── http_routes.py         (http routes for half duplex communication with UI (client) )
│   │   ├── websocket_routes.py    (WS routes for full duplex communication with UI (client) )
|   |   
│   ├── ui/                        (high level functions to interact with the User Interface.)
│   │   ├── controllers/
│   │       ├── ui_controller.py   
│   │
│   ├── security/
│   │   ├── auth.py                (authorization for role based access control)
│   │   ├── encryption.py          (for data encryption while wireless communication)
│   │
│   ├── plugins/                   (for future plugins)
│   │
│   ├── tests/                     (defines test cases)
│
├── docs/
│   ├── README.md
│
├── logs/
│   ├── .gitkeep
│
├── data/
│   ├── .gitkeep
│
├── requirements.txt
├── README.md
└── LICENSE
</pre>
<br>    
<p>Project Skyops - is a python application and a gcs that works on the top of dronekit and pymavlink in order to communicate with the aerial vehicle (pixhawk-ardupilot) via mavlink and a user interface (currently electron.js) via web sockets.</p><br>
<h2>High-Level System Architecture</h2>
    <ul>
        <li><strong>Ground Control Station Interface (GCS)</strong>: User interface for mission planning, telemetry visualization, and drone control.</li>
        <li><strong>Raspberry Pi Backend</strong>: Handles communication between the GCS and the UAV, relaying telemetry and control commands.</li>
        <li><strong>Pixhawk Flight Controller</strong>: Executes commands received from the Raspberry Pi running ArduPilot.</li>
        <li><strong>Live Video Feed</strong>: Real-time video streaming from the UAV camera to the GCS.</li>
    </ul><br>
<h2>System Communication Flow</h2>
    <p>The communication flow is as follows:</p>
    <ul>
        <li>The gcs interface sends mission commands to the Raspberry Pi.</li>
        <li>The Raspberry Pi processes these commands and communicates with the Pixhawk flight controller via MAVLink.</li>
        <li>Telemetry data is sent back from Pixhawk to the Raspberry Pi and then relayed to the gcs interface.</li>
        <li>The UAV camera streams live video to the GCS for real-time monitoring.</li>
    </ul>
</body>
</html>
