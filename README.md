# LFSP - Local Files Sharing Platform

LFSP provides a safer, more convenient, and more versatile alternative to directly connecting external storage devices via USB. Share your files securely over your local network with password protection, expiration times, and read-only access.

## Features

- **Secure Sharing**: Share files with password protection and set expiration times for links
- **Read-Only Access**: Protect your original files with read-only access by default
- **No USB Needed**: Share files over your network without the security risks of USB connections
- **Multiple Platforms**: Works on Windows, macOS, and Linux systems with any modern browser
- **Dark Mode Support**: Enjoy a comfortable viewing experience with both light and dark themes

## Screenshots

- Modern, responsive interface
- Dashboard to monitor and manage shared links
- Intuitive file browser for accessing shared content

## Requirements

- Python 3.6 or higher
- Flask and dependencies (listed in requirements.txt)
- Windows, macOS, or Linux operating system
- Network connectivity for sharing files

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```
   python app.py
   ```
2. Open a web browser and navigate to the URL displayed in the terminal (usually http://localhost:5000 or http://<your-ip-address>:5000)
3. Select a storage device or folder to share
4. Configure sharing options (password, expiration time, access permissions)
5. Share the generated link with others on your network
6. Use the dashboard to manage your shared links and mounted devices

## Security Notes

- LFSP is designed for use within trusted local networks
- Always use password protection for sensitive files
- Regularly review and revoke unused sharing links
- Be cautious about what directories you choose to share

## Development

The application is built with:
- Flask for the backend
- Tailwind CSS for UI design
- JavaScript for interactive components

## License

MIT License

## Author

nadeeshafdo