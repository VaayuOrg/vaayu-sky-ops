# high level drone services module

from adapters.dronekit_adapter.connection import ConnectionHandler
from adapters.dronekit_adapter.flight_control import FlightController
from adapters.dronekit_adapter.motors import MotorController
from adapters.dronekit_adapter.network import Network
from adapters.dronekit_adapter.planner import Planner
from adapters.dronekit_adapter.upload import WaypointUploader

from models.telemetry_model import TelemetryModel

from core.utils.portmanager import PortManager
from core.config.config import config

from mission.scan_mission import Scan

import os, time

class DroneService:
    
    def __init__(self):
        self.conn = ConnectionHandler()
        self.network = Network()
        self.manager = PortManager()
        self.control = None
        self.motors = None
        self.plan = None
        self.upload = None
        self.telemetry = None

    def start_connection(self):
        self.manager.free_port(config["serial_port"])
        message = self.conn.connect(config["serial_port"],config["baud"])
      #   message = self.conn.connect_sitl(config["tcp_conn_string"],config["baud"])

        if message == True:
           self.control = FlightController(self.conn.vehicle,self.conn.is_connected)
           self.upload = WaypointUploader(self.conn.vehicle)  # initiallizing waypointuploader class with drone conn instance
           self.telemetry = TelemetryModel(self.conn.vehicle) # initallizing telemetry
           self.is_connected = True
        else:
           print("vehicle not connected")    
        return message

    def stop_connection(self):
      #   if self.conn.is_connected == True:       commented out for testing
           message = self.conn.disconnect()
           return message
        
    def monitor_vehicle(self):
        while True:
           if self.conn.is_connected == False:
              return True
         #   if self.conn.state["armed"] == False:
         #      self.control.disarm_vehicle()
         #    #   print("disarmed")
           time.sleep(1)

    def send_heartbeat(self):
         # if self.network.network_monitoring:
            # self.network.network_monitoring = True
         return self.network.heartbeat()

    def acknowledge(self,ack):
           self.network.ack = ack
           return True 

    def trigger_failsafe(self):
        if self.control.is_arm and self.plan:
            self.plan.set_mode('LAND')
                     

    def start_to_arm(self):
        if self.conn.is_connected == True:
           message = self.control.arm_vehicle()
           self.motors = MotorController(self.conn.vehicle)
           if message == True:
            #   self.control.is_arm = True
              self.plan = Planner(self.conn.vehicle)   
           return message

    def start_to_disarm(self):
        if self.conn.is_connected:
            if self.control.is_arm == True:
               message = self.control.disarm_vehicle()
               if message == True:
                  # self.control.is_arm = False
                  self.plan = None   
            return message
            
    def start_motors(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.throttle_up()
        return message

    def stop_motors(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.throttle_down()
           return message

    def start_roll(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.roll_right()
           return message
        
    def stop_roll(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.roll_left()
           return message 

    def start_pitch(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.pitch_forward()
           return message

    def stop_pitch(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.pitch_backward()
           return message

    def start_yaw(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.yaw_clockwise()
           return message

    def stop_yaw(self):
        if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.motors.yaw_anticlockwise()
           return message               

    def hold_alt(self,alt):
      #  print(float(self.data["height"]),2)
       if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.plan.takeoff_and_hold(alt)
            #   self.data = {}  #empty the dict for reuse
           return message
       
    def return_to_land(self):
       if self.conn.is_connected == True:
           if self.control.is_arm == True:
              message = self.plan.emergency_land()
           return message

    def mode_switch(self,mode):
        message = self.plan.set_mode(mode)
        return message
              

    def _safe_call(self, method_name, method, telemetry):
        """Calls a method safely and handles exceptions."""
        try:
            telemetry[method_name] = method()
        except Exception as e:
            telemetry[method_name] = f"⚠️ Error: {str(e)}"

    def send_telemetry(self):
        if not self.conn.is_connected:
         #   print("error : ❌ Drone is not connected.")
           return False
    
        # tm = TelemetryModel(self.conn.vehicle)

        telemetry = {}
        # Call each method safely
        self._safe_call("nav", self.telemetry.get_navigation_data, telemetry)
        self._safe_call("attitude", self.telemetry.get_attitude_data, telemetry)
        self._safe_call("gps", self.telemetry.get_gps_data, telemetry)
        self._safe_call("system", self.telemetry.get_system_status, telemetry)
        self._safe_call("battery", self.telemetry.get_battery_status, telemetry)
        self._safe_call("imu", self.telemetry.get_imu_data, telemetry)

        return telemetry
    
   #  def handle_file_upload(self, data):
    
   #   try:
   #      filename = data.get("filename")
   #      filedata = data.get("data")

   #      if not filename or not filedata:
   #          return {"status": "error", "message": "Invalid file data received."}

   #      # Ensure the directory exists
   #      wp_dir = config.get("wp_files", "wp_files")  # Default to 'wp_files' if not set
   #      os.makedirs(wp_dir, exist_ok=True)  # Create directory if it doesn't exist

   #      # Save the file
   #      file_path = os.path.join(wp_dir, filename)
   #      with open(file_path, "wb") as f:
   #          f.write(filedata)

   #      print(f"✅ File '{filename}' saved successfully at {file_path}")

   #      # Upload the waypoint file to Mission Planner
   #      self._file_upload_helper(file_path)

   #      return {"status": "success", "message": f"File '{filename}' uploaded and sent to Mission Planner successfully."}

   #   except Exception as e:
   #      print("❌ File upload failed:", e)
   #      return {"status": "error", "message": str(e)}

   #  def _file_upload_helper(self, wp_file):
   #   try:
   #      print(f"📡 Uploading waypoints from '{wp_file}' to Mission Planner...")
   #      self.upload.upload_mission(wp_file)
   #      print("✅ Waypoints uploaded successfully!")
   #   except Exception as e:
   #      print(f"❌ Failed to upload waypoints: {e}")



    # takes waypoints from gui, converts it into .wp format file and uploads the file to pixhawk 
   #  def upload_wps(self,data):
   #   try:
   #      waypoints = data
   #      self.upload.save_wp_file(waypoints)
   #    #   self.upload.upload_mission(mission)
   #      print("✅ Waypoints uploaded successfully!")
   #   except Exception as e:
   #      print(f"❌ Failed to upload waypoints: {e}")

   
    def scan(self, waypoints, g_speed):
         try:
            response = self.start_to_arm()
            print(response)
            if response:
               scan = Scan(self.plan, waypoints, g_speed)
               response = scan.start_mission()
               if response == False:
                  self.start_to_disarm() 
            else:
                print("failed to arm")
         except Exception as e:
            print(f"❌ Error occured, failed to start the mission: {e}")
                  