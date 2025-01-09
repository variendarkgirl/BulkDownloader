import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import json
import random
import time

class ProxyFetcher:
    def __init__(self):
        self.proxies = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def fetch_proxies(self):
        try:
            url = 'https://spys.one/en/https-ssl-proxy/'
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            proxy_rows = soup.find_all('tr', class_=['spy1x', 'spy1xx'])
            valid_proxies = []
            
            for row in proxy_rows:
                try:
                    columns = row.find_all('td')
                    if len(columns) >= 2:
                        ip = columns[0].text.strip()
                        port = columns[1].text.strip()
                        if self.is_valid_proxy(ip, port):
                            valid_proxies.append(f'https://{ip}:{port}')
                except:
                    continue
            
            return valid_proxies
        except Exception as e:
            print(f"Error fetching proxies: {str(e)}")
            return []

    def is_valid_proxy(self, ip, port):
        proxy = f'https://{ip}:{port}'
        try:
            test_url = 'https://twitter.com'
            response = requests.get(
                test_url,
                proxies={'https': proxy},
                timeout=5,
                headers=self.headers
            )
            return response.status_code == 200
        except:
            return False

    def get_working_proxy(self):
        if not self.proxies:
            self.proxies = self.fetch_proxies()
        
        while self.proxies:
            proxy = random.choice(self.proxies)
            if self.is_valid_proxy(*proxy.replace('https://', '').split(':')):
                return proxy
            self.proxies.remove(proxy)
        
        self.proxies = self.fetch_proxies()
        return self.get_working_proxy() if self.proxies else None

class TwitterDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter Media Downloader (Proxy Enabled)")
        self.root.geometry("700x800")
        self.root.configure(bg='#2c3e50')

        # Initialize proxy fetcher
        self.proxy_fetcher = ProxyFetcher()
        self.current_proxy = None

        # Color Scheme
        self.bg_color = '#2c3e50'
        self.primary_color = '#3498db'
        self.text_color = '#ecf0f1'
        self.accent_color = '#e74c3c'

        # Headers for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Create Main Frame
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        self.title_label = tk.Label(
            self.main_frame, 
            text="Twitter Media Downloader (Proxy Enabled)", 
            font=('Arial', 18, 'bold'),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.title_label.pack(pady=(0, 20))

        # Proxy Status
        self.proxy_status = tk.Label(
            self.main_frame,
            text="Proxy Status: Not Connected",
            font=('Arial', 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.proxy_status.pack(pady=(0, 10))

        # Refresh Proxy Button
        self.refresh_proxy_btn = tk.Button(
            self.main_frame,
            text="Refresh Proxy",
            command=self.refresh_proxy,
            bg=self.primary_color,
            fg=self.text_color
        )
        self.refresh_proxy_btn.pack(pady=(0, 10))

        # Download Type Selection
        self.type_label = tk.Label(
            self.main_frame, 
            text="Select Download Type:", 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.type_label.pack(fill='x', pady=(0, 5))
        
        self.download_types = ['All Media', 'Photos Only', 'Videos Only']
        self.type_var = tk.StringVar(value=self.download_types[0])
        self.type_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.type_var, 
            values=self.download_types, 
            state='readonly'
        )
        self.type_dropdown.pack(fill='x', pady=(0, 10))

        # URL Input
        self.url_label = tk.Label(
            self.main_frame, 
            text="Enter Twitter Post/Profile URL:", 
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
        
        self.dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "Twitter_Downloads"))
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

    def refresh_proxy(self):
        self.update_status("Fetching new proxy...")
        threading.Thread(target=self._refresh_proxy_thread, daemon=True).start()

    def _refresh_proxy_thread(self):
        try:
            new_proxy = self.proxy_fetcher.get_working_proxy()
            if new_proxy:
                self.current_proxy = new_proxy
                self.root.after(0, lambda: self.proxy_status.config(
                    text=f"Proxy Status: Connected ({new_proxy})"
                ))
                self.update_status("Successfully connected to new proxy")
            else:
                self.update_status("Failed to find working proxy")
        except Exception as e:
            self.update_status(f"Error refreshing proxy: {str(e)}")

    def start_download(self):
        url = self.url_entry.get().strip()
        download_type = self.type_var.get()
        download_dir = self.dir_var.get()

        if not url:
            messagebox.showerror("Error", "Please enter a valid Twitter URL")
            return

        if not url.startswith(('http://', 'https://')):
            url = 'https://twitter.com/' + url.lstrip('@')

        os.makedirs(download_dir, exist_ok=True)
        self.download_btn.config(state=tk.DISABLED)
        self.status_text.delete(1.0, tk.END)
        self.overall_progress['value'] = 0

        threading.Thread(
            target=self.download_media,
            args=(url, download_type, download_dir),
            daemon=True
        ).start()

    def make_request(self, url, stream=False):
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                if not self.current_proxy:
                    self.current_proxy = self.proxy_fetcher.get_working_proxy()
                
                proxies = {'https': self.current_proxy} if self.current_proxy else None
                
                response = requests.get(
                    url,
                    headers=self.headers,
                    proxies=proxies,
                    stream=stream,
                    timeout=30
                )
                response.raise_for_status()
                return response
            
            except requests.exceptions.RequestException:
                retry_count += 1
                self.update_status(f"Request failed, trying new proxy (attempt {retry_count}/{max_retries})")
                self.current_proxy = self.proxy_fetcher.get_working_proxy()
                
        raise Exception("Failed to connect after maximum retries")

    def download_media(self, url, download_type, download_dir):
        try:
            if not self.current_proxy:
                self.update_status("Initializing proxy connection...")
                self.current_proxy = self.proxy_fetcher.get_working_proxy()
                if not self.current_proxy:
                    raise Exception("No working proxy found")
                self.proxy_status.config(text=f"Proxy Status: Connected ({self.current_proxy})")

            if '/status/' in url:
                self.download_single_tweet(url, download_dir, download_type)
            else:
                self.download_profile_media(url, download_dir, download_type)
            
            self.root.after(0, self.download_complete)
        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"Download error: {str(e)}"))

    def download_single_tweet(self, url, download_dir, download_type):
        try:
            self.update_status(f"Processing tweet: {url}")
            response = self.make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            media_elements = soup.find_all('div', {'class': 'css-1dbjc4n r-1p0dtai'})
            
            for media in media_elements:
                if download_type in ['All Media', 'Photos Only']:
                    img_elements = media.find_all('img', {'alt': True})
                    for img in img_elements:
                        if 'profile' not in img.get('alt', '').lower():
                            img_url = img.get('src', '')
                            if img_url:
                                self.download_photo(img_url, download_dir)

                if download_type in ['All Media', 'Videos Only']:
                    video_elements = media.find_all('video')
                    for video in video_elements:
                        video_url = video.get('src', '')
                        if video_url:
                            self.download_video(video_url, download_dir)

        except Exception as e:
            self.update_status(f"Error processing tweet: {str(e)}")

    def download_profile_media(self, url, download_dir, download_type):
        try:
            self.update_status(f"Processing profile: {url}")
            response = self.make_request(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tweets = soup.find_all('article')
            
            for tweet in tweets:
                media_container = tweet.find('div', {'data-testid': 'tweetPhoto'})
                if media_container:
                    if download_type in ['All Media', 'Photos Only']:
                        img_elements = media_container.find_all('img', {'alt': True})
                        for img in img_elements:
                            if 'profile' not in img.get('alt', '').lower():
                                img_url = img.get('src', '')
                                if img_url:
                                    self.download_photo(img_url, download_dir)

                    if download_type in ['All Media', 'Videos Only']:
                        video_elements = media_container.find_all('video')
                        for video in video_elements:
                            video_url = video.get('src', '')
                            if video_url:
                                self.download_video(video_url, download_dir)

        except Exception as e:
            self.update_status(f"Error processing profile: {str(e)}")

    def download_photo(self, url, download_dir):
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https:' + url

            photo_dir = os.path.join(download_dir, 'Photos')
            os.makedirs(photo_dir, exist_ok=True)

            filename = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.urandom(4).hex()}.jpg"
            filepath = os.path.join(photo_
