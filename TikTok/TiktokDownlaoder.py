import tkinter as tk
from tkinter import messagebox
import instaloader
import os

class TiktokDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tiktok Video and Reels Downloader")
        self.root.geometry("500x400")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select Type:", font=("Helvetica", 12, "bold"))
        self.label.pack(pady=10)

        self.type_var = tk.StringVar()
        self.type_var.set("Videos")

        self.type_menu = tk.OptionMenu(self.root, self.type_var, "Videos", "Reels")
        self.type_menu.config(width=20, font=("Helvetica", 10))
        self.type_menu.pack(pady=10)

        self.link_label = tk.Label(self.root, text="Enter Profile Link:", font=("Helvetica", 12, "bold"))
        self.link_label.pack(pady=10)

        self.link_entry = tk.Entry(self.root, width=50)
        self.link_entry.pack(pady=10)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, bg="blue", fg="white", font=("Helvetica", 10, "bold"))
        self.submit_button.pack(pady=20)

        self.output_text = tk.Text(self.root, height=10, width=60)
        self.output_text.pack(pady=10)

    def submit(self):
        self.output_text.delete(1.0, tk.END)
        content_type = self.type_var.get()
        profile_link = self.link_entry.get()

        if not profile_link:
            messagebox.showerror("Error", "Profile link cannot be empty")
            return

        self.crawl_Tiktok(profile_link, content_type)

    def crawl_Tiktok(self, profile_link, content_type):
        try:
            L = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(L.context, profile_link.strip("/").split("/")[-1])
            videos = [post for post in profile.get_posts() if post.is_video]
            reels = [post for post in profile.get_posts() if post.typename == "GraphVideo"]
            video_count = len(videos)
            reel_count = len(reels)

            self.output_text.insert(tk.END, f"Downloaded {video_count} videos and {reel_count} reels on Tiktok.\n")

            if content_type == "Videos":
                self.download_Tiktok_content(L, videos, "Videos")
            elif content_type == "Reels":
                self.download_Tiktok_content(L, reels, "Reels")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to crawl Tiktok profile: {e}")

    def download_Tiktok_content(self, loader, content_posts, content_type):
        target_dir = f"downloads/Tiktok/{content_type}"
        os.makedirs(target_dir, exist_ok=True)

        for idx, post in enumerate(content_posts, start=1):
            try:
                # Use the post's description as the title
                title = post.caption if post.caption else f"{post.owner_username}_{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S')}"
                sanitized_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                
                # Download the post (best quality by default)
                loader.download_post(post, target=target_dir)

                # Rename downloaded video file
                video_file_path = None
                for file in os.listdir(target_dir):
                    if file.endswith(".mp4") and sanitized_title in file:
                        video_file_path = os.path.join(target_dir, file)
                        break

                if video_file_path:
                    new_video_file_name = os.path.join(target_dir, f"{sanitized_title}.mp4")
                    os.rename(video_file_path, new_video_file_name)
                    print(f"Video {idx}: {sanitized_title} has been downloaded")
                    self.output_text.insert(tk.END, f"Video {idx}: {sanitized_title} has been downloaded\n")

                # Remove non-video files
                for file in os.listdir(target_dir):
                    if not file.endswith(".mp4"):
                        os.remove(os.path.join(target_dir, file))

            except Exception as e:
                print(f"Failed to download video: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TiktokDownloaderApp(root)
    root.mainloop()
