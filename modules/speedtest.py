#Description:
#Version:1.1.4

import speedtest  # Ensure speedtest-cli is installed

class SpeedTest:
    def __init__(self):
        self.st = speedtest.Speedtest()

    def get_speeds(self):
        # Get the best server, run download and upload tests, and measure ping
        self.st.get_best_server()
        download_speed = self.st.download() / 1_000_000  # Convert to Mbps
        upload_speed = self.st.upload() / 1_000_000  # Convert to Mbps
        ping = self.st.results.ping
        return download_speed, upload_speed, ping