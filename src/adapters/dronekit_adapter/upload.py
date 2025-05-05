import time, os
from dronekit import Command
from pymavlink import mavutil, mavwp

class WaypointUploader:
    def __init__(self, vehicle):
        self.vehicle = vehicle

    def upload_mission(self, waypoint_file):
     try:
        print(f"📂 Reading waypoints from {waypoint_file}...")

        with open(waypoint_file, 'r') as file:
            lines = file.readlines()

        # Ensure correct format (QGC WPL 110)
        if not lines or "QGC WPL 110" not in lines[0]:
            print("❌ Invalid waypoint file format!")
            return False

        waypoints = lines[1:]  # Skip the header line

        cmds = self.vehicle.commands
        cmds.clear()
        time.sleep(1)

        for i, line in enumerate(waypoints):
            items = line.strip().split('\t')
            if len(items) < 12:
                continue  # Skip invalid lines

            lat = float(items[8])
            lon = float(items[9])
            alt = float(items[10])
            command = int(items[3])

            # Convert lat/lon to integer format for MISSION_ITEM_INT
            lat_int = int(lat * 1e7)
            lon_int = int(lon * 1e7)

            print(f"📌 Sending MISSION_ITEM_INT: lat={lat}, lon={lon}, alt={alt}, cmd={command}")

            # Send MISSION_ITEM_INT
            self.vehicle.message_factory.mission_item_int_send(
                0,  # Target system
                0,  # Target component
                i,  # Sequence
                mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
                command,
                0,  # Current (0=not current, 1=current)
                0,  # Autocontinue
                0, 0, 0, 0,  # Params 1-4
                lat_int,  # Latitude in 1e7 format
                lon_int,  # Longitude in 1e7 format
                alt  # Altitude
            )

            time.sleep(0.1)  # Small delay for stability
        
        self.verify_mission()
        print("✅ All waypoints sent as MISSION_ITEM_INT!")
        return True

     except Exception as e:
        print("❌ Mission upload failed:", e)
        return False


    def verify_mission(self):
        """
        Verifies the uploaded mission by downloading and counting waypoints.
        """
        try:
            print("📡 Fetching stored mission for verification...")
            self.vehicle.commands.download()
            time.sleep(2)  # Allow time for commands to sync
            self.vehicle.commands.wait_ready()
            
            cmds_list = list(self.vehicle.commands)  # Convert to list to force evaluation
            total_waypoints = len(cmds_list)

            print(f"✅ Mission verification complete: {total_waypoints} waypoints uploaded!")

            if total_waypoints == 0:
                print("⚠️ Warning: No waypoints found! Try re-uploading or check MAVLink compatibility.")

        except Exception as e:
            print(f"❌ Mission verification failed: {e}")

    def _generate_wp_content(self, waypoints):
     try:
        content = "QGC WPL 110\n"

        # Home location (first WP)
        home = waypoints[0]
        content += f"0\t1\t0\t16\t0\t0\t0\t0\t{home['lat']}\t{home['lon']}\t{home['alt']}\t1\n"

        # Waypoints
        for index, wp in enumerate(waypoints, start=1):
            content += f"{index}\t0\t3\t16\t0\t0\t0\t0\t{wp['lat']}\t{wp['lon']}\t{wp['alt']}\t1\n"

        return content

     except Exception as e:
        print(f"❌ Error while generating waypoint content: {e}")
        return None


    def save_wp_file(self, waypoints, filename="mission.waypoints"):
     try:
        content = self._generate_wp_content(waypoints)
        if content is None:
            return False

        # Find root directory (where main script resides)
        root_dir = os.path.dirname(os.path.abspath(__file__))

        # Create 'wp_files' inside root dir
        dir_path = os.path.join(root_dir, "wp_files")
        os.makedirs(dir_path, exist_ok=True)

        # Complete path to the file
        file_path = os.path.join(dir_path, filename)

        # Write content to file
        with open(file_path, "w") as f:
            f.write(content)

        print(f"✅ Waypoint file saved at: {file_path}")
        return True

     except Exception as e:
        print(f"❌ Failed to save .waypoints file: {e}")
        return False


