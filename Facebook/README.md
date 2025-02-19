# Facebook Videos and Reels Downloader

A Python application with a graphical user interface for downloading videos and reels from Facebook. This tool allows you to easily download public Facebook videos and reels without requiring login credentials.

![image](https://github.com/user-attachments/assets/e898ffe6-4503-45c0-b35d-a9aa396bbde7)


## Features 

- Simple and intuitive graphical user interface
- Download public Facebook videos and reels
- No Facebook login required
- Progress tracking with status updates
- Custom download directory selection
- Support for both desktop and mobile Facebook URLs

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `tkinter` (usually comes with Python)
  - `requests`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/variendarkgirl/BulkDownloader.git
cd BulkDownloader/Facebook
```

2. Install required packages:
```bash
pip install requests
```

## Usage

1. Run the application:
```bash
python FBdownloader.py
```

2. In the application:
   - Enter the Facebook video/reel URL in the input field
   - Choose your download directory (or use the default)
   - Click "Start Download"
   - Monitor the progress in the status window

### Supported URL Formats

- Regular video posts: `https://www.facebook.com/watch?v=...`
- Reels: `https://www.facebook.com/reel/...`
- Mobile URLs: `https://m.facebook.com/...`

## Features in Detail

- **Progress Tracking**: Real-time download progress with percentage completion
- **Status Updates**: Detailed status messages showing the current operation
- **Custom Directory**: Choose where to save your downloaded videos
- **Error Handling**: Comprehensive error messages if something goes wrong
- **Automatic Naming**: Files are saved with timestamps to avoid duplicates

## Common Issues and Solutions

1. **Video Not Downloading**
   - Make sure the video is public and accessible without login
   - Try using the mobile version of the URL
   - Check your internet connection

2. **Permission Error**
   - Ensure you have write permissions in the selected download directory
   - Try running the application with appropriate permissions

3. **URL Error**
   - Verify that the URL is from Facebook and is complete
   - Make sure the video/reel is still available

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License

## Disclaimer

This tool is for personal use only. Please respect Facebook's terms of service and content creators' rights. Only download videos that you have permission to download.

## Acknowledgments

- Thanks to all contributors who have helped with the project
- Built using Python's tkinter for the GUI
- Uses the requests library for handling downloads

## Support

If you encounter any issues or have questions, please:
1. Check the Common Issues section above
2. Look through existing issues in the GitHub repository
3. Create a new issue if your problem isn't already reported

## Future Plans

- Add support for batch downloads
- Implement playlist/album download support
- Add quality selection options
- Include thumbnail previews
- Add support for other social media platforms

---

Made with ❤️ by [Str1k3r0p]
