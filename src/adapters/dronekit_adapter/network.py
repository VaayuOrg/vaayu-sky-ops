import time, threading

class Network:
    def __init__(self):
        # self.network_monitoring = False
        self.ack = None
        # self.timestamp_stack = []
        # self._start_monitoring()

    def heartbeat(self):
        return {
            "source":"raspberrypi",
            "hb_timestamp":time.time(),
            "ack_timestamp":None,
            "strength":None,
            "status":"active",
            "ack":False
        }
    
    def network_strength(self):
        pass

    # def check_ack(self):
    #     """Monitor acknowledgments when network monitoring is active."""
    #     while True:
    #         if self.ack:
    #             if not self.timestamp_stack or self.timestamp_stack[-1] != self.ack["ack_timestamp"]:
    #                self.timestamp_stack.append(self.ack["ack_timestamp"])
    #                print(self.timestamp_stack)
    #             else:
    #                count = 0
    #                while count<3:
    #                    if self.timestamp_stack[-1] != self.ack["ack_timestamp"]:
    #                       self.timestamp_stack.append(self.ack["ack_timestamp"])
    #                       break
    #                    count = count + 1
    #                    time.sleep(1)
    #                if count>3:
    #                    self.network_monitoring = False
    #                    print("Connection Lost from ground unit, triggering failsafe")
    #                    self._stop_monitoring()
    #         time.sleep(1)  # Check every sec (buffer time)        
                

    # def _start_monitoring(self):
    #     self.monitoring_thread = threading.Thread(target=self.check_ack)
    #     self.monitoring_thread.daemon = True
    #     self.monitoring_thread.start()

    # def _stop_monitoring(self):
    #     """Stop the monitoring thread safely."""
    #     if self.monitoring_thread.is_alive():
    #         self.monitoring_thread.join()

