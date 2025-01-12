# Twitter Media Downloader

A JavaScript-based tool that allows you to download all images from a Twitter/X profile's media tab in high definition. The script runs directly in your browser's console and doesn't require any external dependencies.

![image](https://github.com/user-attachments/assets/a6a0ee21-a37c-46a9-8105-57e78d4e1c89)


## Short Description
Twitter Media Downloader is a browser-based script that automatically scans and downloads all images from a Twitter profile's media tab while maintaining their original HD quality. It features a user-friendly interface with progress tracking, batch downloading capabilities, and the ability to pause/stop the download process at any time.

## Detailed Documentation

### Features
- 🖼️ Downloads images in original HD quality
- 📱 Works on any Twitter/X profile's media tab
- 🚀 Automatic scrolling and image detection
- 📊 Real-time progress tracking
- ⏸️ Pause/Stop functionality
- 📦 Batch download support
- 🔒 Works within Twitter's security constraints
- 💻 No external dependencies required

### Prerequisites
- A modern web browser (Chrome, Firefox, Edge, etc.)
- Access to browser's developer console (F12)
- A Twitter/X account (to access profile pages)

### Installation
1. No installation required! This is a browser-based script.
2. Copy the entire script code provided at https://github.com/variendarkgirl/BulkDownloader/blob/main/Twitter/XDownloader.js.

### Usage Instructions

1. **Navigate to Twitter Profile**
   ```
   Go to the Twitter/X profile whose images you want to download
   ```

2. **Access Media Tab**
   ```
   Click on the "Media" tab of the profile
   ```

3. **Open Developer Console**
   ```
   Press F12 or right-click -> Inspect -> Console
   ```

4. **Run the Script**
   - Paste the script into the console
   - Press Enter to run

5. **Using the Interface**
   - Watch the status display in the top-right corner
   - Let the script scan through all available images
   - Use the "Download All Images" button to start downloading
   - Use "Stop Download" if needed

### How It Works

The script operates in two phases:

1. **Scanning Phase**
   - Automatically scrolls through the media tab
   - Detects and catalogs all available images
   - Converts image URLs to HD quality
   - Tracks progress and new discoveries

2. **Download Phase**
   - Triggered by clicking "Download All Images"
   - Downloads each image in original quality
   - Implements delays to prevent browser throttling
   - Shows real-time download progress
  
   ![image](https://github.com/user-attachments/assets/b107832b-1417-4659-8e37-4effbcd6cd87)


### Configuration
The script includes several customizable parameters:

```javascript
const scrollAmount = 1000;  // Pixels to scroll each time
const duration = 1000;      // Scroll animation duration
const maxAttempts = 5;      // Maximum consecutive empty scrolls before stopping
```

### Error Handling
The script includes robust error handling:
- Checks for media tab presence
- Validates image URLs
- Handles network errors
- Prevents duplicate downloads

### Known Limitations
- Browser download limits may affect batch sizes
- Twitter rate limiting may slow down image fetching
- Some browsers may require enabling multiple downloads
- Works only on publicly accessible profiles

### Troubleshooting

**Common Issues:**

1. **Downloads not starting:**
   - Ensure you're on the Media tab
   - Check browser download permissions
   - Clear browser cache

2. **Script stops early:**
   - Increase scroll attempts
   - Check internet connection
   - Verify profile accessibility

3. **Images not in HD:**
   - Verify original image availability
   - Check URL conversion success

### Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Disclaimer
This tool is for personal use only. Please respect Twitter's terms of service and use responsibly. Always ensure you have the right to download and use the images.

### Support
For support, please open an issue in the GitHub repository.

## Version History
- v1.0.0 (2024-01-12)
  - Initial release
  - Basic downloading functionality
  - Progress tracking
  - Batch download support

### Author
variendarkgirl

### Contributor
Str1k3r0p
