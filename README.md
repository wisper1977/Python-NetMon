# Python NetMon - 1.1.3.1

Welcome to the Python NetMon repository! Python NetMon is a simple, intuitive network monitoring tool built with Python and Tkinter. It allows users to manage network devices, monitor their status, and view detailed ping statistics in real-time.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Device Management](#device-management)
  - [Adding a New Device](#adding-a-new-device)
  - [Editing a Device](#editing-a-device)
  - [Deleting a Device](#deleting-a-device)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Log Viewer](#log-viewer)
  - [Viewing Logs](#viewing-logs)
  - [Filtering Logs](#filtering-logs)
  - [Archiving Logs](#archiving-logs)
  - [Clearing Logs](#clearing-logs)
  - [Acknowledging Alerts](#acknowledging-alerts)
- [Syslog Viewer](#syslog-viewer)
  - [Viewing Syslogs](#viewing-syslogs)
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

## Device Management

### Adding a New Device

To add a new device to the network monitoring list, follow these steps:

1. Open the application.
2. Navigate to `Edit > Add Device` from the menu bar.
3. A dialog box will appear prompting you to enter the device details:
   - **Key**: A unique identifier for the device (usually managed by the system).
   - **Location**: The physical or logical location of the device.
   - **Name**: A descriptive name for the device.
   - **IP**: The IP address of the device.
   - **Type**: The type of device (e.g., router, switch, server).
4. After filling out all the fields, click "OK" to add the device to the list.
5. The device will now appear in the main window with a status of "Pending" until the next refresh, when its status will update based on its response to ping requests.

### Editing a Device

To edit an existing device's details:

1. Select the device you want to edit from the list in the main window.
2. Navigate to `Edit > Edit Device` from the menu bar.
3. The same dialog box used for adding a device will appear, with the fields pre-populated with the device's current details.
4. Change the details as needed:
   - You can modify the Location, Name, IP, and Type fields.
5. Once you've made the necessary changes, click "OK" to update the device's details.
6. The modified details will reflect immediately in the device list.

### Deleting a Device

To remove a device from the monitoring list:

1. Select the device you wish to delete from the list in the main window.
2. Navigate to `Edit > Delete Device` from the menu bar.
3. A confirmation dialog will appear asking if you are sure about removing the device.
4. Click "Yes" to remove the device permanently.
5. The device will be removed from the list and will no longer be monitored.

## Keyboard Shortcuts

The application supports several keyboard shortcuts to make navigation and operations faster and more convenient:

- **Ctrl + N**: Open the dialog to add a new device.
- **Ctrl + E**: Edit the selected device.
- **Ctrl + D**: Delete the selected device.
- **Ctrl + S**: Open settings.
- **F1**: Open online help or documentation.

Make sure a device is selected in the main window for edit or delete shortcuts to work.

## Log Viewer

The Log Viewer is a feature that allows you to view, filter, archive, and clear log entries generated by the application. This is useful for monitoring the application's activities, diagnosing issues, and maintaining records of events.

### Viewing Logs

1. Open the application.
2. Navigate to `View > Log Viewer` from the menu bar.
3. The Log Viewer window will open, displaying a list of log entries with details such as timestamp, log level, and message.

### Filtering Logs

1. In the Log Viewer window, locate the filter options at the top.
2. You can filter logs based on:
   - **Log Level**: Select the log level (e.g., INFO, WARNING, ERROR) from the dropdown to view only the logs of that level.
   - **Date Range**: Set a start and end date to view logs within that specific time frame.
   - **Keyword**: Enter a keyword to search for specific log entries containing that keyword.
3. Click the "Apply Filter" button to update the log view based on your selected filters.

### Archiving Logs

1. In the Log Viewer window, click the "Archive Logs" button.
2. A dialog will appear asking for the destination folder where you want to save the archived log file.
3. Select the folder and click "OK".
4. The logs will be saved to a file in the selected folder, typically named with the current date and time for easy identification.

### Clearing Logs

1. In the Log Viewer window, click the "Clear Logs" button.
2. A confirmation dialog will appear, asking if you are sure you want to clear all logs.
3. Click "Yes" to confirm and clear the logs.
4. The log view will be refreshed, showing no entries.

### Acknowledging Alerts

When the application detects a device status change, an alert sound will play to notify you.

1. To acknowledge the alert, click the "Acknowledge Alert" button in the main window.
2. The alert will stop playing, and the device status will be marked as acknowledged.
3. If the device comes back online, the acknowledgment will be cleared automatically, and the status will update accordingly.

These features ensure that you can effectively monitor and manage the application's log data, keeping track of important events and maintaining system performance.

## Syslog Viewer

The Log Viewer is a feature that allows you to view, filter, archive, and clear log entries generated by the application. This is useful for monitoring the application's activities, diagnosing issues, and maintaining records of events.

### Viewing Sysogs

1. Open the application.
2. Navigate to `Tools > Sysog Viewer` from the menu bar.
3. The Log Viewer window will open, displaying a list of log entries with details such as timestamp, log level, and message.

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
- Code Restructure: Split the code into seperate files to improve proformance.
- Detailed Device Views: Allow users to click on a device in the list to view more detailed information or statistics in a separate dialog or pane.
- Input Validation: Rigorously validate all inputs, especially those that could affect network operations or subprocess invocations, to prevent injection attacks.

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

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/wisper1977/Python/blob/main/Python%20NetMon/License.md) file for details.
