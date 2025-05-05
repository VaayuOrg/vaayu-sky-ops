from core.utils.portmanager import PortManager

config = {
    "serial_port" : "/dev/ttyACM0",  # "COM16"" # "COM21" PortManager().get_usb_port, /dev/ttyACM0
    "tcp_conn_string" : "tcp:127.0.0.1:5760",
    "baud" : "115200", #57600
    "server_port" : "5000",
    "host" : "0.0.0.0",
    "wp_files": "wp_files"
}

