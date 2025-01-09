import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
from datetime import datetime
import requests
import re
from urllib.parse import unquote

class FacebookDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facebook Media Downloader")
        self.root.geometry("700x800")
        self.root.configure(bg='#2c3e50')

        # Color Scheme
        self.bg_color = '#2c3e50'
        self.primary_color = '#3498db'
        self.text_color = '#ecf0f1'
        self.accent_color = '#e74c3c'

        # Create Main Frame
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Facebook Media Downloader", 
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=(0, 20))

        # URL Input
        self.url_label = tk.Label(
            self.main_frame, 
            text="Enter Facebook Video/Reel URL:", 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.url_label.pack(fill='x', pady=(0, 5))
        
        self.url_entry = tk.Entry(
            self.main_frame, 
            width=50, 
            font=('Arial', 10)
        )
        self.url_entry.pack(fill='x', pady=(0, 10))

        # Download Directory Selection
        self.dir_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.dir_frame.pack(fill='x', pady=(0, 10))
        
        self.dir_label = tk.Label(
            self.dir_frame, 
            text="Download Directory:", 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.dir_label.pack(side=tk.LEFT)
        
        self.dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "Facebook_Downloads"))
        self.dir_entry = tk.Entry(
            self.dir_frame, 
            textvariable=self.dir_var, 
            width=30, 
            font=('Arial', 10)
        )
        self.dir_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        self.browse_btn = tk.Button(
            self.dir_frame, 
            text="Browse", 
            command=self.browse_directory,
            bg=self.primary_color,
            fg=self.text_color
        )
        self.browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Download Button
        self.download_btn = tk.Button(
            self.main_frame, 
            text="Start Download", 
            command=self.start_download,
            bg=self.accent_color,
            fg=self.text_color,
            font=('Arial', 12, 'bold')
        )
        self.download_btn.pack(fill='x', pady=(10, 10))

        # Progress Bar
        self.overall_progress_label = tk.Label(
            self.main_frame, 
            text="Download Progress:", 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.overall_progress_label.pack()
        
        self.overall_progress = ttk.Progressbar(
            self.main_frame, 
            orient='horizontal', 
            length=100, 
            mode='determinate'
        )
        self.overall_progress.pack(fill='x', pady=(0, 10))

        # Status Text Area
        self.status_text = tk.Text(
            self.main_frame, 
            height=10, 
            width=70, 
            wrap=tk.WORD,
            font=('Courier', 10)
        )
        self.status_text.pack(fill='both', expand=True)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_var.set(directory)

    def update_status(self, message):
        self.root.after(0, lambda: self.status_text.insert(tk.END, message + '\n'))
        self.root.after(0, lambda: self.status_text.see(tk.END))

    def extract_video_url(self, html_content):
        try:
            # Try multiple patterns to find the video URL
            patterns = [
                r'hd_src:"([^"]+)"',
                r'sd_src:"([^"]+)"',
                r'"playable_url":"([^"]+)"',
                r'"playable_url_quality_hd":"([^"]+)"',
                r'<meta property="og:video" content="([^"]+)"',
                r'<meta property="og:video:url" content="([^"]+)"'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, html_content)
                if match:
                    video_url = match.group(1)
                    video_url = video_url.replace('\\/', '/')
                    return unquote(video_url)
            
            return None
        except Exception as e:
            self.update_status(f"Error extracting URL: {str(e)}")
            return None

    def download_video(self, url, download_dir):
        try:
            # Custom headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }

            # Get the page content
            self.update_status("Fetching video page...")
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to access page: Status code {response.status_code}")

            # Extract video URL
            video_url = self.extract_video_url(response.text)
            
            if not video_url:
                # Try mobile URL if desktop URL fails
                mobile_url = url.replace('www.facebook', 'm.facebook')
                response = requests.get(mobile_url, headers=headers)
                video_url = self.extract_video_url(response.text)
                
                if not video_url:
                    raise Exception("Could not find video URL in the page")

            self.update_status(f"Found video URL!")

            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"facebook_video_{timestamp}.mp4"
            filepath = os.path.join(download_dir, filename)

            # Download the video
            self.update_status("Starting download...")
            response = requests.get(video_url, headers=headers, stream=True)
            response.raise_for_status()

            # Get file size for progress tracking
            file_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded = 0

            with open(filepath, 'wb') as f:
                for data in response.iter_content(block_size):
                    downloaded += len(data)
                    f.write(data)
                    if file_size:
                        progress = int((downloaded / file_size) * 100)
                        self.root.after(0, lambda p=progress: self.overall_progress.configure(value=p))
                        if progress % 10 == 0:  # Update status every 10%
                            self.update_status(f"Downloaded: {progress}%")

            if os.path.getsize(filepath) > 0:
                self.update_status(f"Successfully downloaded: {filename}")
                return True
            else:
                raise Exception("Downloaded file is empty")

        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            return False

    def start_download(self):
        # Get URL and directory
        url = self.url_entry.get().strip()
        download_dir = self.dir_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a Facebook video/reel URL")
            return

        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        # Disable download button and reset progress
        self.download_btn.config(state=tk.DISABLED)
        self.status_text.delete(1.0, tk.END)
        self.overall_progress['value'] = 0

        # Start download in a separate thread
        def download_thread():
            try:
                if self.download_video(url, download_dir):
                    self.root.after(0, lambda: messagebox.showinfo("Success", "Video downloaded successfully!"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("Error", "Failed to download video"))
            finally:
                self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.overall_progress.configure(value=0))

        threading.Thread(target=download_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = FacebookDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
