# handles connection-disconenction to the UAV, additionally monitors vehicle status by fetching its state/hearbeat.

import threading
import time
from dronekit import connect
from models.heartbeat_model import HeartbeatModel

class ConnectionHandler:
    def __init__(self):
        self.vehicle = None
        self.is_connected = False
        self.mode = None
        self.thread = None
        self.state = None
        self.current_heartbeat = None
        self.last_heartbeat_time = time.time()  # Initial timestamp
        self.monitoring = False

    def connect(self, connection_string, baud):
        if self.vehicle is not None:  # Prevent multiple connections
            print("⚠️ Already connected.")
            return True
        try:
            self.vehicle = connect(connection_string, wait_ready=True, baud=baud)
            self.is_connected = True
            print("✅ Successfully connected to the Pixhawk.")
            self._start_monitoring()
            return True
        except Exception as e:
            self.is_connected = False
            print("❌ Connection failed:", {e})
            return False
        
    def connect_sitl(self, connection_string, baud):
        if self.vehicle is not None:  # Prevent multiple connections
            print("⚠️ Already connected.")
            return True
        try:
            self.vehicle = connect(connection_string, wait_ready=True, baud=baud)
            self.is_connected = True
            print("✅ Successfully connected to the Pixhawk.")
            self._start_monitoring()
            return True
        except Exception as e:
            self.is_connected = False
            print("❌ Connection failed:", {e})
            return False    

    def disconnect(self):
        try:
            if self.vehicle:
                self.vehicle.close()
                self.is_connected = False
                self.vehicle = None
            print("✅ Disconnected from the Pixhawk.")
            self._stop_monitoring()
            return True
        except Exception as e:
            print("❌ No active connection to disconnect.")
            return False

    def _get_vehicle_state(self):
        try:
            return HeartbeatModel(self.vehicle).get_heartbeat()
        except Exception as e:
            return {"error": f"Failed to retrieve vehicle status: {e}"}

    def _monitor_vehicle(self):
        """Continuously monitor vehicle status and heartbeat."""
        self.monitoring = True
        stale_heartbeat_count = 0  # Track consecutive stale heartbeats

        while self.monitoring:
         self.state = self._get_vehicle_state()

         if self.vehicle and self.state:
            
            if self.current_heartbeat != self.state["last_heartbeat"]:  # Check if heartbeat is new
                self.current_heartbeat = self.state["last_heartbeat"]  # Get latest heartbeat
                self.last_heartbeat_time = time.time()  # Reset timeout
                stale_heartbeat_count = 0  # Reset redundancy counter
                # print(self.state)
                # print("✅ Heartbeat received.")

            else:
                stale_heartbeat_count += 1  # Increment redundant heartbeat counter
                print(f"⚠️ Redundant heartbeat detected ({stale_heartbeat_count}/5)")

            # If 5 redundant heartbeats occur or no heartbeat for 5 seconds → Disconnect
            if stale_heartbeat_count >= 5 or (time.time() - self.last_heartbeat_time) > 5:
                print("⚠️ No valid heartbeat detected! Disconnecting...")
                self.disconnect()
                break  # Exit monitoring loop

         time.sleep(1)  # Blocking delay

    def _start_monitoring(self):
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._monitor_vehicle, daemon=True)
            self.thread.start()
            print("Started vehicle monitoring.")

    def _stop_monitoring(self):
        self.monitoring = False
        if self.thread:
            self.thread.join()
            self.thread = None
        print("Stopped vehicle monitoring.")
