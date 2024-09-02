import subprocess
from modules.system_log import SystemLog

class NetOpsPing:
    def __init__(self, attempts=5, timeout=1, logger=None):
        self.attempts = attempts
        self.timeout = timeout
        self.logger = logger if logger else SystemLog()  # Use provided logger or default to a new SystemLog instance
        
    def ping_device(self, ip_address):
        try:
            command = ["ping", "-n" if subprocess.os.name == "nt" else "-c", str(self.attempts), ip_address]
            response = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout
            )
            if response.returncode == 0:
                self.logger.log("INFO", f"Ping successful for {ip_address}: {response.stdout.decode()}")
                return True
            else:
                self.logger.log("ERROR", f"Ping failed for {ip_address}: {response.stdout.decode()} {response.stderr.decode()}")
                return False
        except subprocess.TimeoutExpired:
            self.logger.log("ERROR", f"Ping timed out for {ip_address}")
            return False
        except Exception as e:
            self.logger.log("ERROR", f"Ping error for {ip_address}: {str(e)}")
            return False
