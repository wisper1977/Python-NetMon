# Python NetMon - 1.1.4

Welcome to the Python NetMon repository! Python NetMon is a simple, intuitive network monitoring tool built with Python and Tkinter. It allows users to manage network devices, monitor their status, and view detailed ping statistics in real-time.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Wiki](#wiki)
- [Version History](#version-history)
- [Future Plans](#future-plans)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Device Management**: Add, edit, and delete network devices.
- **Real-Time Monitoring**: Continuously ping devices to monitor their status.
- **User Interface**: Simple and clean GUI for easy operation.
- **Logging**: Detailed logging of application activities and errors.
- **Keyboard Shortcuts**: Quick access to common actions using keyboard shortcuts.
- **Syslog Server**: Integrated Syslog Server and Syslog Viewer.
- **SpeedTest**: Integrated a SpeedTest funciton.

## Requirements

- Python 3.x
- Tkinter (typically included with Python)
- Pygame (  `pip install pygame `), will auto install when you run the program
- Speedtest-cli ( `pip install speedtest-cli `), will auto install when you run the program
- Additional Python libraries: `csv`, `configparser`, `subprocess`, `platform`, `ipaddress`, `logging`, `threading`, `queue`, `re`, `webbrowser`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wisper1977/Python/tree/a3544690fe81d7580825c59a1b9e0a7137ccabeb/Python%20NetMon

2. Navigate to the project directory:
   ```bash
   cd Python\ NetMon\
   
  No additional installation required if you have Python installed.

## Usage
To run the application, navigate to the directory containing the script and run:

   python netmon.py

If using on Windows you will have to `Run As Administrator`

## Wiki

Please check out the [Wiki](https://github.com/wisper1977/Python-NetMon/wiki) to see how to use Features.

## Version History

### v1.1.4 - SpeedTest and Minor Enhancements
**Release Date:** Dev

- Bug Fixes: Fixed minor bugs in the user interface and improved the responsiveness.
- **New Features**:
  - SpeedTest: Added a SpeedTest function under Tools menu.
  - Setup Environment: Add a setup environment to check and make sure all packages are installed and firewall rules are inserted.

## Future Plans
- Detailed Device Views: Implement functionality for users to click on a device in the list and display detailed information or statistics in a separate dialog or pane.
- Input Validation: Implement rigorous input validation to secure against potential injection attacks, particularly for inputs affecting network operations or subprocess invocations.
- SNMP Integration: Introduce an SNMP check to verify that a device is operational before attempting to ping it.
- SQLite Integration: Develop a more effective format for managing logs and syslogs using SQLite for improved storage and retrieval.
- Simple FTP Server: Build a basic FTP server to facilitate file transfers within the network.
- Penetration Testing: Conduct penetration testing to identify and address potential security vulnerabilities.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.
