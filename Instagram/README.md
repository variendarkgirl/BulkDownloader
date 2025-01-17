# Instagram Image Downloader HD   

This script allows you to download all visible images from an Instagram profile page in high definition. It uses dynamic scrolling to load additional images and offers a batch download feature.

## Features
- Fetches and downloads images directly from the Instagram feed.
- Detects images loaded dynamically with scrolling.
- Displays a status panel showing download progress.
- Provides options to stop the download or batch download all found images.

## Prerequisites
- A modern browser (Chrome, Firefox, Edge, etc.).
- Access to the Instagram profile page you want to download images from.

## Installation
No installation is required. You can run this script directly in the browser’s Developer Console.

## How to Use
1. Open the Instagram profile page containing the images you want to download.
2. Open the browser Developer Tools (usually F12 or right-click > "Inspect").
3. Navigate to the "Console" tab.
4. Paste the entire script into the console and press Enter.
5. The status panel will appear on the page, showing download progress and available controls.

### Controls
- **Download All Images**: Starts downloading all found images in batch.
- **Stop Download**: Stops the download process immediately.

## Script Overview
- **Dynamic Image Detection**: Automatically identifies `srcset` attributes for high-definition images.
- **Smooth Scrolling**: Scrolls down the page to load more images dynamically.
- **Progress Tracking**: Keeps track of the number of images found, scroll attempts, and empty scroll counts.

## Usage Notes
- Ensure you are logged into Instagram to access profile content.
- Some images may be unavailable if the account is private and you are not a follower.
- This script may need updates if Instagram’s DOM structure changes.

## Disclaimer
This tool is for educational and personal use only. Respect copyright laws and Instagram's terms of service when using this script.

## Example Output
```
Images Found: 20
Scroll Count: 3
Consecutive Empty Scrolls: 0/5
Scan complete! Found 20 images. Click "Download All Images" to start downloading.
```

