import socket
import logging
from logging.handlers import RotatingFileHandler
import threading

class SyslogServer:
    def __init__(self, host='0.0.0.0', port=514):
        self.host = host
        self.port = port
        self.log_file = 'log/syslog.log'
        
        # Setup logger
        self.logger = logging.getLogger('SyslogServer')
        self.logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(self.log_file, maxBytes=5000000, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((self.host, self.port))
        while True:
            data, addr = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            formatted_message = f'{addr[0]} - {message}'
            self.logger.info(formatted_message)
            
    def run_in_background(self):
        server_thread = threading.Thread(target=self.start)
        server_thread.daemon = True
        server_thread.start()
