# custom UAV's task planner for custom missions

from dronekit import LocationGlobalRelative
import time, math
from dronekit import VehicleMode

class Planner:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def set_mode(self, mode_name):
        """Set the flight mode and confirm the switch."""
        try:
            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            print(f"🔄 Switching to {mode_name} mode...")
            self.vehicle.mode = VehicleMode(mode_name)
            time.sleep(2)  # Allow mode switch time

            if self.vehicle.mode.name == mode_name:
                print(f"✅ Successfully switched to {mode_name}.")
                return True
            else:
                print(f"❌ Failed to switch to {mode_name}.")
                return False

        except Exception as e:
            print(f"❌ Error: {e}")
            return False


    def takeoff_and_hold(self, target_alt, hover_mode=None):
     try:
        if not self.vehicle:
            print("❌ No vehicle connected!")
            return False

        target_alt = float(target_alt)  # Ensure valid altitude input

        # Check GPS fix quality
        gps_fix = self.vehicle.gps_0.fix_type  # Fix type (higher is better)
        gps_okay = gps_fix >= 3  # Usually, 3+ means a valid 3D GPS fix

        # Decide the hover mode
        hover_mode = "LOITER" if gps_okay else "LAND"

        print(f"📡 GPS Fix Type: {gps_fix} - {'Good' if gps_okay else 'Poor'}")
        print(f"🔄 Selecting Hover Mode: {hover_mode}")

        # If already at or above target altitude, no need to climb
        if self.vehicle.location.global_relative_frame.alt >= target_alt:
            print(f"🚀 Already at {target_alt}m. No climb needed.")
            return True

        # Switch to GUIDED mode for takeoff
        if not self.set_mode("GUIDED"):
            print("⚠️ Failed to switch to GUIDED mode. Aborting takeoff.")
            return False

        print(f"🚀 Taking off to {target_alt}m...")
        self.vehicle.simple_takeoff(target_alt)

        # Monitor altitude until it reaches target
        while True:
            current_alt = self.vehicle.location.global_relative_frame.alt
            print(f"📡 Current Altitude: {current_alt:.2f} m")

            # If 95% of target altitude is reached, proceed
            if current_alt >= target_alt * 0.95:
                print(f"✅ Altitude {target_alt}m reached.")
                break

            time.sleep(0.5)  # Small delay to avoid excessive polling

        # Immediately check GPS fix before switching hover mode
        gps_fix = self.vehicle.gps_0.fix_type
        gps_okay = gps_fix >= 3
        hover_mode = "LOITER" if gps_okay else "LAND"

        print(f"🔄 Final GPS Check: {gps_fix} - {'Good' if gps_okay else 'Poor'}")
        print(f"🔄 Switching to {hover_mode} mode...")

        if not self.set_mode(hover_mode):
            print("⚠️ Failed to switch hover mode. Landing for safety.")
            self.set_mode("LAND")
            return False

        print(f"✅ Hovering at {target_alt}m in {hover_mode} mode.")
        return True

     except Exception as e:
        print(f"❌ Error: {e}")
        print("⚠️ Emergency Landing for Safety!")
        self.set_mode("LAND")
        return False

    def emergency_land(self):
        """Safely land the drone in case of emergency."""
        try:
            if not self.vehicle:
                print("❌ No vehicle connected!")
                return False

            print("⚠️ Emergency detected! Initiating landing...")

            # Check GPS fix before deciding to LAND or RTL
            if self.vehicle.gps_0.fix_type < 3:  # Weak GPS fix
                print("⚠️ Weak GPS! Performing immediate LAND.")
                self.set_mode("LAND")
            else:
                print("🏡 GPS fix strong. Returning to launch (RTL).")
                self.set_mode("RTL")

            return True

        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        

    def _distance_to_wp(self, target_location):
        """Calculate the ground distance in meters between two LocationGlobalRelative points."""
        dlat = target_location.lat - self.vehicle.location.global_relative_frame.lat
        dlong = target_location.lon - self.vehicle.location.global_relative_frame.lon
        return math.sqrt((dlat * 1.113195e5) ** 2 + (dlong * 1.113195e5) ** 2)

    def goto_wp(self, lat, lon, alt, groundspeed):
        """
        Smoothly navigate the drone to the given GPS waypoint.
        :param lat: Latitude of the target location
        :param lon: Longitude of the target location
        :param alt: Altitude in meters
        :param groundspeed: Groundspeed in m/s (default 5)
        :return: True if reached successfully, False otherwise
        """
        try:
            target_location = LocationGlobalRelative(lat, lon, alt)

            print(f"📍 Navigating to waypoint: ({lat}, {lon}, {alt}m)")

            # Ensure we're in GUIDED mode
            self.set_mode("GUIDED")

            self.vehicle.groundspeed = groundspeed
            self.vehicle.simple_goto(target_location)

            while True:
                distance = self._distance_to_wp(target_location)
                print(f"📡 Distance to waypoint: {distance:.2f} m")

                if distance <= 1.0:  # Threshold for "arrived"
                    print("✅ Reached waypoint.")
                    break

                time.sleep(1)

            return True

        except Exception as e:
            print(f"❌ Navigation error: {e}")
            return False    
    

    def stop(self):
     try:
        # Determine appropriate hold mode
        gps_fix = self.vehicle.gps_0.fix_type
        gps_okay = gps_fix >= 3
        hold_mode = "LOITER" if gps_okay else "BRAKE"

        print(f"📡 GPS Fix Type: {gps_fix} - {'Good' if gps_okay else 'Poor'}")
        print(f"🔄 Switching to Hold Mode: {hold_mode}")

        if not self.set_mode(hold_mode):
            print("⚠️ Failed to switch to hold mode.")
            return False

        print("🛑 Drone is now holding position.")
        return True

     except Exception as e:
        print(f"❌ Error during hold: {e}")
        return False



  