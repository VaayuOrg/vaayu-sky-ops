class HeartbeatModel:
    """
    Data Model for structuring heartbeat messages received from the vehicle.
    """

    def __init__(self, vehicle):
        self.vehicle = vehicle  # Store the vehicle instance

    def get_heartbeat(self):
        """Extracts and returns structured heartbeat data from the vehicle."""

        if not self.vehicle:
            return {"error": "No vehicle connection available."}

        return {
            "last_heartbeat": self.vehicle.last_heartbeat,  # Time since last heartbeat (seconds)
            "system_status": self.vehicle.system_status.state,  # System status (e.g., active, critical)
            "mode": self.vehicle.mode.name,  # Current flight mode (e.g., STABILIZE, LOITER)
            "armed": self.vehicle.armed,  # True if drone is armed, False otherwise
            "gps_fix": self.vehicle.gps_0.fix_type,  # GPS fix type (0 = No fix, 3 = 3D fix)
            "battery": self.vehicle.battery.level if self.vehicle.battery else "N/A"  # Battery level %
        }
