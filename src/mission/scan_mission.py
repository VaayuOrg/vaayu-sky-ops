# customized scan mission, called in drone_services with params as waypoints and planner object

import time

class Scan:
    def __init__(self, planner, waypoints, g_speed):
        self.planner = planner
        self.waypoints = waypoints
        self.ground_speed = g_speed
        # self.start_mission(waypoints)

    def start_mission(self):
     max_retries = 3
     print("🚀 Starting scan mission with waypoints...")

     try:
        if not self.waypoints or len(self.waypoints[0]) != 3:
            print("❌ Invalid waypoints data. Aborting mission.")
            return False

        # Fetch altitude from the first waypoint
        _, _, initial_alt = self.waypoints[0]

        # Perform Takeoff and Hold at initial altitude
        print(f"🛫 Taking off and holding at {initial_alt}m before starting mission...")
        takeoff_success = self.planner.takeoff_and_hold(initial_alt)

        if not takeoff_success:
            print("❌ Takeoff failed. Aborting mission.")
            return False

        # Start navigating through waypoints
        for index, wp in enumerate(self.waypoints):
            lat, lon, alt = wp
            print(f"📍 Navigating to Waypoint {index + 1}/{len(self.waypoints)}: ({lat}, {lon}, {alt}m)")

            attempt = 0
            success = False

            while attempt < max_retries:
                success = self.planner.goto_wp(lat, lon, alt, self.ground_speed)

                if success:
                    print(f"✅ Reached Waypoint {index + 1}")
                    break  # Go to next waypoint

                attempt += 1
                print(f"⚠️ Failed attempt {attempt}/{max_retries} for Waypoint {index + 1}. Retrying...")
                self.planner.stop()  # Stop and reset before retrying
                time.sleep(1)

            if not success:
                print(f"❌ Failed to reach Waypoint {index + 1} after {max_retries} retries. Returning home...")
                self.planner.emergency_land()
                return False

        print("✅ Scan mission complete. Returning to launch...")
        self.planner.emergency_land()
        return True

     except Exception as e:
        print(f"❌ Unexpected Error during mission: {e}")
        print("⚠️ Triggering emergency landing!")
        self.planner.emergency_land()
        return False
