class TelemetryModel:
    def __init__(self,vehicle):
        self.vehicle = vehicle

    
    def get_navigation_data(self):
        return {
            "latitude": self.vehicle.location.global_frame.lat or 28.5104,
            "longitude": self.vehicle.location.global_frame.lon or 77.37,
            "altitude": self.vehicle.location.global_relative_frame.alt,
            "groundspeed": self.vehicle.groundspeed,
            "airspeed": self.vehicle.airspeed,
            "climbrate": self.vehicle.velocity[2],  # Vertical speed
        }

    # 2️⃣ Attitude & Orientation Data
    def get_attitude_data(self):
        return {
            "yaw": self.vehicle.attitude.yaw,
            "pitch": self.vehicle.attitude.pitch,
            "roll": self.vehicle.attitude.roll,
            "tilt": (self.vehicle.attitude.pitch**2 + self.vehicle.attitude.roll**2) ** 0.5, 
        }

    # 3️⃣ GPS Data
    def get_gps_data(self):
        return {
            "fixtype": self.vehicle.gps_0.fix_type,
            "satellites": self.vehicle.gps_0.satellites_visible,
            "gpsaltitude": self.vehicle.location.global_frame.alt,
        }

    # 4️⃣ System Status & Mode
    def get_system_status(self):
        return {
            "flight_mode": self.vehicle.mode.name,
            "armed": self.vehicle.armed,
            "ekfstatus": self.vehicle.ekf_ok,
        }

    # 5️⃣ Battery & Power Data
    def get_battery_status(self):
        return {
            "voltage": self.vehicle.battery.voltage,
            "current": self.vehicle.battery.current,
            "level": self.vehicle.battery.level,
        }

    # 6️⃣ IMU (Inertial Measurement Unit) Data
    def get_imu_data(self):
        return {
            "acceleration": {
                "x": self.vehicle.acceleration.x,
                "y": self.vehicle.acceleration.y,
                "z": self.vehicle.acceleration.z,
            },
            "gyroscope": {
                "x": self.vehicle.gyro.x,
                "y": self.vehicle.gyro.y,
                "z": self.vehicle.gyro.z,
            },
            "magnetometer": {
                "x": self.vehicle.mag_field.x,
                "y": self.vehicle.mag_field.y,
                "z": self.vehicle.mag_field.z,
            },
        }

    # 7️⃣ RC (Radio Controller) Input Data
    def get_rc_input(self):
        return {
            "channels": {
                "ch1": self.vehicle.channels.get(1, 0),
                "ch2": self.vehicle.channels.get(2, 0),
                "ch3": self.vehicle.channels.get(3, 0),
                "ch4": self.vehicle.channels.get(4, 0),
                "ch5": self.vehicle.channels.get(5, 0),
                "ch6": self.vehicle.channels.get(6, 0),
            },
            "signalstrength": self.vehicle.rangefinder.distance, 
        }

