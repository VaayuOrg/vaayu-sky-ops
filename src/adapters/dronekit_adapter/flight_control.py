# controls the arming and disarming of the UAV 

from dronekit import VehicleMode
import time

class FlightController():
    def __init__(self,vehicle,is_connected):
        self.vehicle = vehicle
        self.is_connected = is_connected
        self.is_arm = False

    def arm_vehicle(self):
     if not self.is_connected or not self.vehicle:
        print("❌ Vehicle not connected.")
        return False

     try:
        self.disable_prearm_checks()
        # Switch to STABILIZE mode
        print("⏳ Switching to STABILIZE mode...")
        self.vehicle.mode = VehicleMode("STABILIZE")

        timeout = 10  # Timeout for mode change
        start_time = time.time()

        while self.vehicle.mode.name != "STABILIZE":
            if time.time() - start_time > timeout:
                print("⚠️ Mode switch timeout: Unable to enter STABILIZE mode.")
                return False
            time.sleep(0.5)

        print("✅ Mode set to STABILIZE. Attempting to arm the vehicle...")

        # Attempt to arm the vehicle
        self.vehicle.armed = True
        timeout = 10  # Timeout for arming
        start_time = time.time()

        while not self.vehicle.armed:
            if time.time() - start_time > timeout:
                print("⚠️ Arming timeout: Unable to arm the vehicle.")
                return False
            
            print("⏳ Waiting for arming...")
            time.sleep(1)

        self.is_arm = True
        print("✅ Vehicle armed successfully.")
        return True

     except Exception as e:
        print(f"❌ Arming failed: {e}")
        return False

    def disarm_vehicle(self):
        if not self.is_connected or not self.vehicle:
            return "❌ Vehicle not connected."

        try:
            if not self.vehicle.armed:
                return "✅ Vehicle is already disarmed."

            self.vehicle.armed = False
            self.is_arm = False
            print("✅ Vehicle is disarming...")
            return True
        except Exception as e:
            print("❌ Failed to disarm the vehicle: ",{e})
            return False
        
    def disable_prearm_checks(self):
        if self.vehicle is None:
            print("❌ Vehicle not connected. Cannot disable pre-arm checks.")
            return

        try:
            # Disable all pre-arm checks
            self.vehicle.parameters['ARMING_CHECK'] = 0
            print("✅ Pre-arm checks disabled successfully!")
        except Exception as e:
            print(f"❌ Failed to disable pre-arm checks: {e}")

        