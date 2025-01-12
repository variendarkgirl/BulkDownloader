import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pytube
import os
import threading
from pytube import Playlist

class YouTubePlaylistDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Playlist Downloader")
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
            text="YouTube Playlist Downloader", 
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=(0, 20))

        # Download Type Selection
        self.type_label = tk.Label(
            self.main_frame, 
            text="Select Download Type:", 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.type_label.pack(fill='x', pady=(0, 5))
        
        self.download_types = ['Audio', 'Video', 'Highest Quality']
        self.type_var = tk.StringVar(value=self.download_types[0])
        self.type_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.type_var, 
            values=self.download_types, 
            state='readonly'
        )
        self.type_dropdown.pack(fill='x', pady=(0, 10))

        # Playlist URL Input
        self.url_label = tk.Label(
            self.main_frame, 
            text="Enter YouTube Playlist URL:", 
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
        
        self.dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "YouTube_Downloads"))
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

        # Overall Progress Bar
        self.overall_progress_label = tk.Label(
            self.main_frame, 
            text="Overall Progress:", 
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

    def start_download(self):
        # Validate inputs
        url = self.url_entry.get().strip()
        download_type = self.type_var.get()
        download_dir = self.dir_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube Playlist URL")
            return

        # Create download directories
        os.makedirs(download_dir, exist_ok=True)
        videos_dir = os.path.join(download_dir, 'Videos')
        audio_dir = os.path.join(download_dir, 'Audio')
        os.makedirs(videos_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        # Disable download button during download
        self.download_btn.config(state=tk.DISABLED)
        
        # Clear previous status
        self.status_text.delete(1.0, tk.END)
        self.overall_progress['value'] = 0

        # Start download in a separate thread
        threading.Thread(
            target=self.download_playlist, 
            args=(url, download_type, download_dir), 
            daemon=True
        ).start()

    def download_playlist(self, url, download_type, download_dir):
        try:
            # Create playlist object
            playlist = Playlist(url)
            
            # Update progress bar
            self.root.after(0, lambda: self.overall_progress.config(maximum=len(playlist.video_urls)))
            
            # Download each video
            for index, video_url in enumerate(playlist.video_urls, 1):
                try:
                    # Create YouTube object
                    yt = pytube.YouTube(video_url)
                    
                    # Download based on type
                    if download_type == 'Audio':
                        # Download audio
                        audio_dir = os.path.join(download_dir, 'Audio')
                        audio_stream = yt.streams.filter(only_audio=True).first()
                        audio_stream.download(output_path=audio_dir, filename=f"{yt.title}.mp3")
                        
                    elif download_type == 'Video':
                        # Download standard video
                        videos_dir = os.path.join(download_dir, 'Videos')
                        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                        video_stream.download(output_path=videos_dir)
                        
                    elif download_type == 'Highest Quality':
                        # Download highest quality video
                        videos_dir = os.path.join(download_dir, 'Videos')
                        video_stream = yt.streams.get_highest_resolution()
                        video_stream.download(output_path=videos_dir)
                    
                    # Update status and progress
                    self.update_status(f"Downloaded: {yt.title}")
                    self.root.after(0, lambda x=index: self.overall_progress.config(value=x))
                
                except Exception as video_error:
                    self.update_status(f"Error downloading video: {video_error}")
            
            # Complete download
            self.root.after(0, self.download_complete)
        
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def update_status(self, message):
        self.root.after(0, lambda: self.status_text.insert(tk.END, message + '\n'))
        self.root.after(0, lambda: self.status_text.see(tk.END))

    def show_error(self, message):
        messagebox.showerror("Download Error", message)
        self.download_btn.config(state=tk.NORMAL)

    def download_complete(self):
        messagebox.showinfo("Download Complete", "Playlist download finished successfully!")
        self.download_btn.config(state=tk.NORMAL)
        self.overall_progress['value'] = 0

def main():
    root = tk.Tk()
    app = YouTubePlaylistDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
