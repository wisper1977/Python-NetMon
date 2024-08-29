# Python NetMon - 1.1.3.1

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

## Requirements

- Python 3.x
- Tkinter (typically included with Python)
- Pygame (  `pip install pygame `)
- Additional Python libraries: `csv`, `configparser`, `subprocess`, `platform`, `ipaddress`, `logging`, `threading`, `queue`, `re`, `webbrowser`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wisper1977/Python/tree/a3544690fe81d7580825c59a1b9e0a7137ccabeb/Python%20NetMon

2. Navigate to the project directory:
   ```bash
   cd Python\ NetMon\

3. Create a firewall rule for the Syslog server 

   Windows PowerShell
      ```bash
      New-NetFirewallRule -DisplayName "Allow Syslog Server" -Direction Inbound -Protocol UDP -LocalPort 514 -Action Allow

  Linux unsing ipTables
      ```bash
      sudo iptables -A INPUT -p udp --dport 514 -j ACCEPT
      sudo iptables-save | sudo tee /etc/sysconfig/iptables
      sudo systemctl restart iptables
    
  No additional installation required if you have Python installed.

## Usage
To run the application, navigate to the directory containing the script and run:

   python netmon.py

If using on Windows you will have to `Run As Administrator`

## Wiki

Please check out the [Wiki](https://github.com/wisper1977/Python-NetMon/wiki) to see how to use Features.

## Version History

### v1.1.3.1 - Syslog Server and Minor Enhancements
**Release Date:** August 28, 2024

- Bug Fixes: Fixed minor bugs in the user interface and improved the responsiveness.
- Restructure of file system to a module based system.
- Cleanup of code for easier understanding of functionality.
- **New Features**:
  - Syslog Server: Added the capability of using as a Syslog Server.
  - Syslog Viewer: Added a Syslog viewer.

### v1.1.3 - Log Viewer and Minor Enhancements
**Release Date:** May 20, 2024

- Bug Fixes: Fixed minor bugs in the user interface and improved the responsiveness.
- Code Refactoring: Improved code structure for better maintainability.
- Security Updates: Enhanced input validation to prevent potential security issues.
- **New Features**:
  - Log Viewer: Added a log viewer with filtering, archiving, and clearing capabilities.
  - Alert Sound: Implemented an alert sound for device status changes. Users can acknowledge the alert, and it will clear once the device comes back online.

### v1.1.2 - Error Handling and Logging
**Release Date:** May 10, 2024

Security Enhancements:
- Granular Error Handling: Refined error reporting across various parts of the application:
- Configuration Management: Now captures specific exceptions related to configuration errors, such as parsing errors and missing configuration files.
- Device Management: Enhanced file operation error handling, including specific exceptions when reading, writing, and updating device information.
- Network Operations: Improved error handling during network activities such as pinging, capturing specific network-related exceptions like timeouts and subprocess errors.
- Logging Improvements: Extended the logging functionality to provide more detailed information regarding the operation status and errors, aiding in easier diagnostics and troubleshooting.
- GUI Adjustments: Minor updates to the GUI components for better user interaction and error feedback, ensuring a more responsive and user-friendly interface.
- Code Refinements: Adjusted existing code for better clarity and efficiency, focusing on robust handling of potential runtime exceptions and ensuring the stability of the application.

### v1.1.1 - GUI Update
**Release Date:** May 8, 2024

Major Improvements:
- Logging Enhancements: Introduced granular logging setup with a dedicated LogManager class to manage application-wide logging. Configured file and console handlers to capture logs, easing debugging and monitoring operations.
- Error Handling Improvements: Expanded error handling in networking and configuration tasks to catch and log specific exceptions. This improves diagnostics and helps in maintaining system stability and debugging issues related to network timeouts and configuration errors.
- User Interface Adjustments: Enhanced the treeview display to include an additional column for "Average Ping", providing more detailed feedback on network status directly in the main application window. Improved UI responsiveness by handling UI updates through asynchronous callbacks, ensuring the application remains responsive during network operations.
- Performance Optimization: Implemented more efficient network operation handling with a thread-safe queue, allowing more reliable and controlled execution of network ping tasks. Optimized the device loading and sorting mechanism, reducing the computational overhead when refreshing device statuses.
- Feature Extensions: Added capabilities for modifying network ping settings through a dedicated settings dialog, giving users the flexibility to adjust the number of attempts and timeout settings dynamically. Introduced functionality to edit and delete device configurations directly from the UI, enhancing user interaction and ease of management.
- Code Refactoring: Refactored major parts of the codebase for better readability and maintainability. Segregated functionalities into clearer, purpose-driven modules and classes. Enhanced comments and documentation within the code to align with Python best practices, aiding future contributors and maintainers of the project.
- Security and Validation: Implemented rigorous validation for device IP addresses upon entry to prevent errors related to malformed inputs. Enhanced error handling mechanisms to prevent application crashes and ensure user operations are handled gracefully.

Bug Fixes:
- Addressed issues where the application could become unresponsive during prolonged network activities.
- Fixed bugs related to device configuration saving and loading that could cause incorrect data handling.

### v1.1.0 - Major Update
**Release Date:** April 20, 2024

Major Improvements:
- Introduced the device editing and deleting functionality.
- Added validation for IP addresses when adding or editing devices.
- Enhanced performance for device status updates.
- Redesigned the entire user interface for a more modern look.
- Introduced a multi-threaded approach for handling network operations.
- Added a logging system with file output for troubleshooting.

### v1.0.4 - Additional Features
**Release Date:** April 5, 2024

New Features:
- Implemented device editing and deletion capabilities.
- Added support for saving device configurations.

### v1.0.3 - User Interface Improvements
**Release Date:** March 20, 2024

UI Updates:
- Enhanced user interface with better layout and navigation.
- Added color coding to status indicators for devices.

### v1.0.2 - Performance Enhancements
**Release Date:** March 15, 2024

- Fixed a bug in the network pinging process where timeouts were not handled correctly.
- Updated UI responsiveness during network scans.
- Optimized the network ping process for faster response times.
- Reduced CPU usage during idle periods.

### v1.0.1 - Bug Fixes
**Release Date:** February 25, 2024

- Minor bug fixes in the configuration management.
- Improved error messages for easier troubleshooting.
- Fixed an issue where ping results were not updating correctly.
- Minor UI adjustments for better readability.

### v1.0.0 - Initial Release
**Release Date:** February 10, 2024

- Features Introduced:
- Basic network monitoring capabilities.
- Ping devices manually to check connectivity.
- Display results in a simple user interface.

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
