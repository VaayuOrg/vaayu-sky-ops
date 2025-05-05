# def generate_waypoints_file(filename, lat, lon, alt=1.5, loiter_time=60):
#     waypoints = f"""QGC WPL 110
# 0\t1\t0\t16\t0\t0\t0\t0\t{lat}\t{lon}\t0\t1
# 1\t0\t3\t22\t0\t0\t0\t0\t{lat}\t{lon}\t{alt}\t1
# 2\t0\t3\t19\t{loiter_time}\t0\t0\t0\t{lat}\t{lon}\t{alt}\t1
# 3\t0\t3\t21\t0\t0\t0\t0\t{lat}\t{lon}\t0\t1
#     """

#     with open(filename, "w") as file:
#         file.write(waypoints)
    
#     print(f"✅ Waypoints file '{filename}' created successfully.")

# # User inputs for GPS coordinates
# home_lat = float(input("Enter Home Latitude: "))
# home_lon = float(input("Enter Home Longitude: "))

# # Generate the waypoints file
# waypoints_filename = "mission.waypoints"
# generate_waypoints_file(waypoints_filename, home_lat, home_lon)

