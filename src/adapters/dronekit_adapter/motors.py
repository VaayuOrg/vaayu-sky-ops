# controls the motors of the UAV

class MotorController:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.min_pwm = 1000  # Minimum PWM value
        self.max_pwm = 1999  # Maximum PWM value
        self.increment = 10  # Step size for adjustments
        
        # Initialize channel overrides
        self.throttle = self.min_pwm
        # self.roll = 1500     # Channel 1: Roll (Left-Right movement)
        # self.pitch = 1500    # Channel 2: Pitch (Forward-Backward movement)
        # self.yaw = 1500      # Channel 4: Yaw (Rotation left-right)
        self.neutral_pwm = 1500

    def throttle_up(self):
        try:
            if self.throttle < self.max_pwm:
                self.throttle += self.increment
                self.vehicle.channels.overrides['3'] = self.throttle
                print(f"✅ Throttle increased to {self.throttle}")
            else:
                print("❌ Throttle cannot exceed 1999.")
        except Exception as e:
            print(f"❌ Failed to increase throttle: {e}")

    def throttle_down(self):
        try:
            if self.throttle > self.min_pwm:
                self.throttle -= self.increment
                self.vehicle.channels.overrides['3'] = self.throttle
                print(f"✅ Throttle decreased to {self.throttle}")
            else:
                print("❌ Throttle cannot go below 1000.")
        except Exception as e:
            print(f"❌ Failed to decrease throttle: {e}")

    def roll_left(self):
        try:
            self.vehicle.channels.overrides['1'] = self.max_pwm
            print(f"✅ Rolling left: {self.max_pwm}")
            self.vehicle.channels.overrides['1'] = self.neutral_pwm
            print(f"🔄 Reset roll to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to roll left: {e}")

    def roll_right(self):
        try:
            self.vehicle.channels.overrides['1'] = self.min_pwm
            print(f"✅ Rolling right: {self.min_pwm}")
            self.vehicle.channels.overrides['1'] = self.neutral_pwm
            print(f"🔄 Reset roll to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to roll right: {e}")

    def pitch_forward(self):
        try:
            self.vehicle.channels.overrides['2'] = self.max_pwm
            print(f"✅ Pitching forward: {self.max_pwm}")
            self.vehicle.channels.overrides['2'] = self.neutral_pwm
            print(f"🔄 Reset pitch to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to pitch forward: {e}")

    def pitch_backward(self):
        try:
            self.vehicle.channels.overrides['2'] = self.min_pwm
            print(f"✅ Pitching backward: {self.min_pwm}")
            self.vehicle.channels.overrides['2'] = self.neutral_pwm
            print(f"🔄 Reset pitch to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to pitch backward: {e}")

    def yaw_clockwise(self):
        try:
            self.vehicle.channels.overrides['4'] = self.max_pwm
            print(f"✅ Yawing clockwise: {self.max_pwm}")
            self.vehicle.channels.overrides['4'] = self.neutral_pwm
            print(f"🔄 Reset yaw to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to yaw clockwise: {e}")

    def yaw_anticlockwise(self):
        try:
            self.vehicle.channels.overrides['4'] = self.min_pwm
            print(f"✅ Yawing anticlockwise: {self.min_pwm}")
            self.vehicle.channels.overrides['4'] = self.neutral_pwm
            print(f"🔄 Reset yaw to neutral: {self.neutral_pwm}")
        except Exception as e:
            print(f"❌ Failed to yaw anticlockwise: {e}")