import os
import signal
import platform
import subprocess
import re

class PortManager:
    @staticmethod
    def free_port(port):
        try:
            system = platform.system()

            if system == "Windows":
                result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
                for line in result.stdout.splitlines():
                    if f":{port}" in line:
                        parts = line.split()
                        pid = parts[-1]  # PID is the last column
                        if pid.isdigit():
                            os.system(f"taskkill /F /PID {pid}")
                            print(f"✅ Process {pid} using port {port} has been killed.")

            else:  # Linux / macOS
                result = subprocess.run(["lsof", "-i", f":{port}"], capture_output=True, text=True)
                for line in result.stdout.splitlines()[1:]:  # Skip the header
                    parts = line.split()
                    pid = parts[1]  # PID is in the second column
                    os.kill(int(pid), signal.SIGKILL)
                    print(f"✅ Process {pid} using port {port} has been killed.")

            print(f"Port is now free.")
            return True
        
        except Exception as e:
            print(f"❌ Error freeing port {port}: {e}")
            return False

    @staticmethod
    def get_usb_port():
        system = platform.system()
        
        try:
            if system == "Windows":
                result = subprocess.run(
                    ["wmic", "path", "Win32_SerialPort", "get", "DeviceID,PNPDeviceID"],
                    capture_output=True, text=True
                )
                ports = re.findall(r'(COM\d+)', result.stdout)
                if ports:
                    print(f"✅ USB device detected on port: {ports[0]}")
                    return ports[0]
                else:
                    print("❌ No USB device found.")

            elif system in ["Linux", "Darwin"]:  # Linux/macOS
                result = subprocess.run(["ls", "/dev/"], capture_output=True, text=True)
                ports = re.findall(r'(ttyUSB\d+|ttyACM\d+)', result.stdout)
                if ports:
                    print(f"✅ USB device detected on port: /dev/{ports[0]}")
                    return f"/dev/{ports[0]}"
                else:
                    print("❌ No USB device found.")

        except Exception as e:
            print(f"❌ Error detecting USB port: {e}")
            return None
