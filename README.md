# Instagram Video and Reels Downloader

A simple GUI application built with Python using Tkinter and Instaloader for downloading videos and reels from Instagram profiles.

## Features

- Download videos and reels from public Instagram profiles.
- User-friendly GUI built with Tkinter.
- Automatically organizes downloaded content into directories.
- Sanitizes filenames to ensure compatibility with the file system.

## Requirements

- Python 3.12
- `tkinter` (included with standard Python installations)
- `instaloader` (for downloading content)


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/variendarkgirl/BulkDownloader
   cd instagram-video-reels-downloader
   
2. Install the required packages:

  pip install instaloader

## Usage
Run the application:
  python app.py
Select the type of content you want to download (Videos or Reels) from the dropdown menu.

Enter the profile link of the Instagram account from which you want to download content.

Click on the "Submit" button to start the download process.

The output will be displayed in the text area, showing the status of each downloaded video or reel.

Example
Select "Videos" from the dropdown.
Enter a profile link like https://www.instagram.com/username/.
Click "Submit."
The application will download the videos and display a message for each successfully downloaded video.

Important Notes
The application can only download content from public Instagram profiles.
Make sure you have sufficient permissions to download content from the specified profiles.
Contributing
Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a new branch for your feature or bug fix. Then, submit a pull request with a description of your changes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
Instaloader - A tool to download Instagram photos, videos, and metadata.
