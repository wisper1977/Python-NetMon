# Network Monitor App
# network_monitor.py
# version: 1.2
# description: Handles the monitoring of network devices, including performing ping and SNMP checks and updating device status in the GUI.

import threading
import asyncio
from modules.gui_utils import GUIUtils

class NetworkMonitor:
    def __init__(self, app, update_queue, device_manager_gui):
        self.app = app
        self.update_queue = update_queue
        self.device_manager_gui = device_manager_gui

        self.ping = app.ping
        self.snmp = app.snmp
        self.settings_manager = app.settings_manager
        self.logger = app.logger  # Adding logger reference

        self.consecutive_failures = {}
        self.consecutive_successes = {}
        self.failure_threshold = 2
        self.success_threshold = 2
        self.acknowledged_devices = set()

        self.refresh_interval = self.settings_manager.config.getint('Network', 'refreshinterval') * 1000
        self.remaining_time = self.refresh_interval // 1000  # Initial time in seconds

    def monitor_devices(self):
        devices = self.device_manager_gui.device_manager.get_all_devices()
        if devices is None:
            return

        threads = []
        for device in devices:
            t = threading.Thread(target=self.check_device_status, args=(device,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        # After all threads have completed, update the GUI
        self.update_queue.put(lambda: self.app.gui.update_treeview_with_devices(self.device_manager_gui.device_manager.get_all_devices()))

    def check_device_status(self, device):
        device_id, name, ip_address, location, device_type, snmp_status, ping_status, last_status = [
            val if val is not None else '' for val in device[:8]
        ]

        snmp_status = "Failed"
        ping_status = "Failed"
        overall_status = last_status  # Default to last status

        # Run SNMP and ping checks
        snmp_result = asyncio.run(self.snmp.snmp_get(ip_address, '1.3.6.1.2.1.1.1.0'))
        if snmp_result:
            snmp_status = "Success"
            self.logger.log("INFO", f"SNMP check succeeded for {name} ({ip_address})")

        ping_result = self.ping.ping_device(ip_address)
        if ping_result:
            ping_status = "Success"
            self.logger.log("INFO", f"Ping check succeeded for {name} ({ip_address})")

        # Log failures if they occur
        if snmp_status == "Failed":
            self.logger.log("ERROR", f"SNMP check failed for {name} ({ip_address})")
        if ping_status == "Failed":
            self.logger.log("ERROR", f"Ping check failed for {name} ({ip_address})")

        # Determine overall status based on the results
        if not snmp_result and not ping_result:
            self.consecutive_successes[device_id] = 0
            self.consecutive_failures[device_id] = self.consecutive_failures.get(device_id, 0) + 1
            if self.consecutive_failures[device_id] >= self.failure_threshold:
                overall_status = "Unreachable"
        else:
            self.consecutive_failures[device_id] = 0
            self.consecutive_successes[device_id] = self.consecutive_successes.get(device_id, 0) + 1
            if self.consecutive_successes[device_id] >= self.success_threshold:
                overall_status = "Reachable"

        # Log the overall status
        self.logger.log("INFO", f"Overall status for {name} ({ip_address}) updated to {overall_status}")

        # Update the device status in the database
        self.device_manager_gui.device_manager.update_status(device_id, snmp_status, ping_status, overall_status)

        # Update the GUI
        self.update_queue.put(lambda: self.app.gui.update_device_status(device_id, snmp_status, ping_status, overall_status))

        # Trigger alert sound if device is unreachable and not acknowledged
        if overall_status == "Unreachable" and device_id not in self.acknowledged_devices:
            self.update_queue.put(lambda: GUIUtils.play_alert_sound('media/alert.wav'))

    def start_monitoring(self):
        threading.Thread(target=self.monitor_devices, daemon=True).start()
        self.update_queue.put(self.app.gui.schedule_next_check)
        self.update_queue.put(lambda: self.app.gui.update_refresh_clock_display(self.remaining_time))