# Version: 1.1.3.1
# Description: Module for performing network operations such as pinging devices.

import os, re, subprocess
from concurrent.futures import ThreadPoolExecutor
from modules.log_manager import LogManager

class NetworkOperations:
    def __init__(self, config, update_callback, max_workers=10):
        """Initialize the NetworkOperations class with a ThreadPoolExecutor."""
        try:
            self.config = config
            self.update_callback = update_callback
            self.executor = ThreadPoolExecutor(max_workers=max_workers)
            self.logger = LogManager.get_instance()
            self.logger.log_debug("NetworkOperations initialized with ThreadPoolExecutor.")
        except Exception as e:
            self.logger.log_error(f"Failed to initialize NetworkOperations: {e}")
            raise e

    def ping_device(self, ip):
        """Submit a ping task to the ThreadPoolExecutor for the given IP address."""
        try:
            future = self.executor.submit(self._ping, ip)
            future.add_done_callback(lambda x: self.process_ping_result(x, ip))
        except Exception as e:
            self.logger.log_error(f"Error submitting ping task for device {ip}: {e}")
            self.update_callback(ip, "Error: Failed to submit ping task")

    def _ping(self, ip):
        """Perform a ping operation on the given IP address."""
        try:
            self.logger.log_info(f"Pinging device with IP: {ip}")
            attempts = int(self.config.get_setting('PING', 'attempts', '3'))
            timeout = int(self.config.get_setting('PING', 'timeout', '100'))
            command = self._construct_ping_command(ip, attempts, timeout)
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            return result
        except subprocess.TimeoutExpired:
            return "Offline, Ping Timeout"
        except subprocess.CalledProcessError as e:
            self.logger.log_error(f"Error pinging {ip}: {e}")
            return f"Offline, Ping Error: {e}"
        except Exception as e:
            self.logger.log_error(f"Unexpected error pinging {ip}: {e}")
            return f"Offline, Unexpected Error: {e}"

    def process_ping_result(self, future, ip):
        """Process the result of the ping operation and update the device status."""
        try:
            result = future.result()
            if isinstance(result, str):
                status = result
            else:
                if result.returncode == 0:
                    status = self._parse_ping_output(result.stdout)
                else:
                    status = "Offline, Host Unreachable" if "Destination Host Unreachable" in result.stdout else "Offline, Ping Failed"
            self.update_callback(ip, status)
            self.logger.log_info(f"Result for device with IP {ip}: {status}")
        except Exception as e:
            self.logger.log_error(f"Error processing ping result for device {ip}: {e}")
            self.update_callback(ip, "Error: Failed to process ping result")

    def _construct_ping_command(self, ip, attempts, timeout):
        """Construct the ping command based on the OS."""
        try:
            # Use the -c option for Unix-like systems and -n for Windows
            count_option = '-c' if os.name != 'nt' else '-n'
            # Use the -W option for Unix-like systems and -w for Windows
            timeout_option = '-W' if os.name != 'nt' else '-w'
            # Convert the timeout to milliseconds for Windows
            timeout_value = str(timeout * 1000) if os.name == 'nt' else str(timeout)
            return ['ping', count_option, str(attempts), timeout_option, timeout_value, ip]
        except Exception as e:
            self.logger.log_error(f"Error constructing ping command: {e}")
            return []
    
    def _parse_ping_output(self, output):
        """Parse the output of the ping command to extract the average time."""
        try:
            ping_lines = output.splitlines()
            time_matches = [re.search(r'time=(\d+)ms', line) for line in ping_lines]
            times = [float(match.group(1)) for match in time_matches if match]
            if times:
                avg_time = sum(times) / len(times)
                return f"Online, Avg ping: {avg_time:.2f} ms"
            return "Online, No time reported"
        except Exception as e:
            self.logger.log_error(f"Error parsing ping output: {e}")
            return "Online, Error parsing ping output"
   
    def shutdown(self):
        """Shutdown the ThreadPoolExecutor for network operations."""
        try:
            self.executor.shutdown(wait=False)
            self.logger.log_info("NetworkOperations shutdown initiated.")
        except Exception as e:
            self.logger.log_error(f"Error shutting down NetworkOperations: {e}")