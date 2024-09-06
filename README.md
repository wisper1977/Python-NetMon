# Python NetMon - 1.2.0.1

Welcome to the Python NetMon repository! 

Python NetMon is a versatile and user-friendly application designed to help IT professionals effectively monitor, manage, and troubleshoot network devices and services. With a focus on ease of use and powerful functionality, this tool provides a range of features that streamline network management tasks and enhance your IT infrastructure's reliability and performance.
 
## Key Features:
- Device Monitoring: Continuously monitor the status of network devices using Ping and SNMP protocols to ensure they are online and functioning correctly.
- FTP Server Management: Easily set up and manage FTP servers directly from the tool, enabling seamless file sharing and management across your network.
- Syslog Integration: Collect, monitor, and analyze syslog messages to keep track of critical events and system logs, providing valuable insights into network operations.
- Speed Test: Measure your network's download and upload speeds, as well as latency, to ensure optimal performance and quickly diagnose connectivity issues.
- Modular Design: The tool is built with a modular architecture, allowing for easy expansion with additional plugins, such as future pentesting capabilities or device-specific checks.
- Intuitive GUI: A clean, intuitive graphical user interface makes it easy to navigate through the various features and quickly access the information you need.

## Benefits:
- Proactive Monitoring: Stay ahead of potential issues with continuous monitoring and real-time alerts for device status changes.
- Centralized Management: Manage multiple aspects of your network, from device health to file transfers, all within a single application.
- Scalability: The tool’s modular design ensures that it can grow with your network, allowing you to add new features and capabilities as your needs evolve.
- User-Friendly: Designed with IT professionals in mind, the tool offers a straightforward setup process and an intuitive interface, minimizing the learning curve and maximizing productivity.

Whether you're a network administrator managing a small office network or an IT professional overseeing a complex infrastructure, our Network Monitoring Tool provides the features and flexibility you need to maintain a robust and efficient network.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Wiki](#wiki)
- [Version History](#version-history)
- [Known Bugs](#known-bugs)
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
- **FTP Server**: Integrated a FTP Server funciton.

## Requirements

- Python 3.x
- Tkinter (typically included with Python)
- Should be handled by `setup_env.py`
  - Pygame (  `pip install pygame `)
  - Speedtest-cli ( `pip install speedtest-cli `)
  - Pyasn1 ( `pip install pyasn1`)
  - Pysmi ( `pip install pysmi`)
  - SNMPCliTools ( `pip install snmpclitools`)
  - PySnmp ( `pip install pysnmp`)
  - PyFTPlib ( `pip install pyftpdlib`)
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

### v1.2 - Performance Enhancing
**Release Date:** TBD
- Fixed issues with the database locking
- Fixed issues with a delay to acknowledging devices

### v1.2 - SNMP, SQLLite, Plugins
**Release Date:** 9/2/2024

**Core Enhancements**

*SNMP Integration:*
- Implemented SNMP monitoring using the NetOpsSNMP class.
- Added SNMP status checks to determine device reachability, with fallback to ping if SNMP fails.
- Configurable SNMP community strings via config.ini.

*SQLite Integration:*
- Integrated SQLite database for storing device information, logs, and status updates.
- Introduced SystemLog class to manage program logs, including error handling and informational messages.
- Environment setup now ensures database and required folders are created if they do not exist.

**Plugins Architecture**

*Plugin System:*
-Introduced a plugins folder for modular functionality.
-Dynamic Tools menu loads and executes plugins at runtime.

*Syslog Plugin:*
- Developed a Syslog server plugin that listens for syslog messages and stores them in SQLite.
- Integrated Syslog Viewer in the Tools menu to display and filter syslog messages.
  
*Speed Test Plugin:*
- Added a speed test plugin utilizing speedtest-cli.
- GUI for running speed tests and displaying download, upload speeds, and ping.
- Thread-safe GUI updates within the plugin.

**Performance and Stability Improvements**

*Thread-Safe Queue Management:*
- Implemented a thread-safe queue (update_queue) for managing GUI updates from background threads.
- Ensured all GUI interactions from background threads are routed through this queue.

*Device Status Tracking:*
- Introduced counters for tracking consecutive successes and failures for device checks to prevent intermittent "flashing" statuses.
- Threshold-based mechanism for determining device reachability based on multiple checks.

*Error Handling and Logging:*
- Improved error handling across modules, with comprehensive logging for easier troubleshooting.
- Enhanced System Log viewer with log level filters and search functionality.

**User Interface and Usability**

*Reduced Application Size:*

- Optimized the codebase, reducing the overall size by approximately 50%.
- Simplified GUI code while adding new features, ensuring a cleaner and more maintainable codebase.

*Improved Device Management:*
- Streamlined device management dialogs (add, edit, delete) for easier interaction.
- Correctly tracks and highlights acknowledged devices in the Treeview.

*Enhanced Visual Feedback:*
- Improved visual indicators in the Treeview for device statuses, with color-coding for reachable and unreachable devices.
- Added a countdown timer and progress bar for refresh intervals, giving users clear feedback on the next check.

**Environment Setup**

*Automated Setup:*
- Automated environment setup ensures all necessary Python packages are installed.
- Added firewall configuration steps for both Windows and Linux to allow Syslog traffic on UDP port 514.

## Known Bugs
- Performance issue, program locking up.
  
## Future Plans
- Detailed Device Views: Implement functionality for users to click on a device in the list and display detailed information or statistics in a separate dialog or pane.
- Input Validation: Implement rigorous input validation to secure against potential injection attacks, particularly for inputs affecting network operations or subprocess invocations.
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
