# Social Media Bulk Downloader and Media Scrapper

A simple GUI application built with Python using Tkinter and Instaloader for bulk/mass downloading/scrapping Photos, Videos, Playlists and reels from different Social Media profiles.

![image](https://github.com/user-attachments/assets/e25a62f7-dc18-4885-b02b-cf9c09829821)
   
 

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
   cd BulkDownloader
   ```

2. Install the required package:

   ```bash
   pip install instaloader
   pip install tinker
   ```

## Usage

1. Run the application:

   ```bash
   python downloader.py
   ```

2. Select the type of content you want to download (Videos or Reels) from the dropdown menu.

3. Enter the profile link of the Instagram account from which you want to download content.

4. Click on the "Submit" button to start the download process.

5. The output will be displayed in the text area, showing the status of each downloaded video or reel.

### Example

- Select "Videos" from the dropdown.
- Enter a profile link like `https://www.instagram.com/username/`.
- Click "Submit".
- The application will download the videos and display a message for each successfully downloaded video.

## Important Notes

- The application can only download content from public Instagram profiles.
- Make sure you have sufficient permissions to download content from the specified profiles.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a new branch for your feature or bug fix. Then, submit a pull request with a description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Instaloader - A tool to download Instagram photos, videos, and metadata.

