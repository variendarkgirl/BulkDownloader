import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import instaloader
import os
import threading
from datetime import datetime

class InstagramDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Media Downloader")
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
            text="Instagram Media Downloader", 
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
        
        self.download_types = ['Posts', 'Photos', 'Videos', 'Reels']
        self.type_var = tk.StringVar(value=self.download_types[0])
        self.type_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.type_var, 
            values=self.download_types, 
            state='readonly'
        )
        self.type_dropdown.pack(fill='x', pady=(0, 10))

        # Profile URL Input
        self.url_label = tk.Label(
            self.main_frame, 
            text="Enter Instagram Profile/Post URL:", 
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
        
        self.dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "Instagram_Downloads"))
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
            messagebox.showerror("Error", "Please enter a valid Instagram profile/post URL")
            return

        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)

        # Disable download button during download
        self.download_btn.config(state=tk.DISABLED)
        
        # Clear previous status
        self.status_text.delete(1.0, tk.END)
        self.overall_progress['value'] = 0

        # Start download in a separate thread
        threading.Thread(
            target=self.download_media, 
            args=(url, download_type, download_dir), 
            daemon=True
        ).start()

    def download_media(self, url, download_type, download_dir):
        try:
            L = instaloader.Instaloader(
                download_pictures=True,
                download_videos=True,
                download_video_thumbnails=False,
                download_geotags=False,
                download_comments=False,
                save_metadata=False
            )

            # Determine download method based on type
            if download_type == 'Posts':
                self.download_posts(L, url, download_dir)
            elif download_type == 'Photos':
                self.download_photos(L, url, download_dir)
            elif download_type == 'Videos':
                self.download_videos(L, url, download_dir)
            elif download_type == 'Reels':
                self.download_reels(L, url, download_dir)

            # Update UI after download
            self.root.after(0, self.download_complete)

        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def download_posts(self, L, url, download_dir):
        try:
            # Check if it's a post or profile
            if '/p/' in url:
                # Single post download
                post = instaloader.Post.from_shortcode(L.context, url.split('/')[-2])
                self.download_single_post(L, post, download_dir)
            else:
                # Profile posts download
                profile = instaloader.Profile.from_username(L.context, url.split('/')[-1])
                posts = list(profile.get_posts())
                
                # Update progress bar
                self.root.after(0, lambda: self.overall_progress.config(maximum=len(posts)))
                
                for i, post in enumerate(posts, 1):
                    self.download_single_post(L, post, download_dir)
                    # Update progress
                    self.root.after(0, lambda x=i: self.overall_progress.config(value=x))
        except Exception as e:
            self.update_status(f"Error downloading posts: {e}")

    def download_single_post(self, L, post, download_dir):
        try:
            # Determine file path based on post type
            if post.is_video:
                target_dir = os.path.join(download_dir, 'Videos')
            else:
                target_dir = os.path.join(download_dir, 'Photos')
            
            # Create directory if not exists
            os.makedirs(target_dir, exist_ok=True)
            
            # Download post
            L.download_post(post, target=target_dir)
            
            # Update status
            self.update_status(f"Downloaded: {post.date_utc}")
        except Exception as e:
            self.update_status(f"Error downloading post: {e}")

    def download_photos(self, L, url, download_dir):
        profile = instaloader.Profile.from_username(L.context, url.split('/')[-1])
        photo_dir = os.path.join(download_dir, 'Photos')
        os.makedirs(photo_dir, exist_ok=True)
        
        posts = [post for post in profile.get_posts() if not post.is_video]
        
        # Update progress bar
        self.root.after(0, lambda: self.overall_progress.config(maximum=len(posts)))
        
        for i, post in enumerate(posts, 1):
            L.download_post(post, target=photo_dir)
            # Update progress
            self.root.after(0, lambda x=i: self.overall_progress.config(value=x))
            self.update_status(f"Downloaded Photo: {post.date_utc}")

    def download_videos(self, L, url, download_dir):
        profile = instaloader.Profile.from_username(L.context, url.split('/')[-1])
        video_dir = os.path.join(download_dir, 'Videos')
        os.makedirs(video_dir, exist_ok=True)
        
        posts = [post for post in profile.get_posts() if post.is_video]
        
        # Update progress bar
        self.root.after(0, lambda: self.overall_progress.config(maximum=len(posts)))
        
        for i, post in enumerate(posts, 1):
            L.download_post(post, target=video_dir)
            # Update progress
            self.root.after(0, lambda x=i: self.overall_progress.config(value=x))
            self.update_status(f"Downloaded Video: {post.date_utc}")

    def download_reels(self, L, url, download_dir):
        profile = instaloader.Profile.from_username(L.context, url.split('/')[-1])
        reels_dir = os.path.join(download_dir, 'Reels')
        os.makedirs(reels_dir, exist_ok=True)
        
        posts = [post for post in profile.get_posts() if post.is_video and post.video_view_count > 0]
        
        # Update progress bar
        self.root.after(0, lambda: self.overall_progress.config(maximum=len(posts)))
        
        for i, post in enumerate(posts, 1):
            L.download_post(post, target=reels_dir)
            # Update progress
            self.root.after(0, lambda x=i: self.overall_progress.config(value=x))
            self.update_status(f"Downloaded Reel: {post.date_utc}")

    def update_status(self, message):
        self.root.after(0, lambda: self.status_text.insert(tk.END, message + '\n'))
        self.root.after(0, lambda: self.status_text.see(tk.END))

    def show_error(self, message):
        messagebox.showerror("Download Error", message)
        self.download_btn.config(state=tk.NORMAL)

    def download_complete(self):
        messagebox.showinfo("Download Complete", "Media download finished successfully!")
        self.download_btn.config(state=tk.NORMAL)
        self.overall_progress['value'] = 0

def main():
    root = tk.Tk()
    app = InstagramDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
