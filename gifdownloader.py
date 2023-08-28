import os
import requests
import tkinter as tk
from tkinter import filedialog

class GIFDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF Downloader")

        self.gif_url = tk.StringVar()

        self.create_ui()

    def create_ui(self):
        url_entry = tk.Entry(self.root, textvariable=self.gif_url)
        url_entry.pack(pady=10)

        download_button = tk.Button(self.root, text="Download GIF", command=self.download_gif)
        download_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", wraplength=400)
        self.status_label.pack(pady=10)

    def download_gif(self):
        gif_url = self.gif_url.get()
        if not gif_url:
            self.status_label.config(text="Please enter a GIF URL.")
            return

        try:
            response = requests.get(gif_url)
            if response.status_code == 200:
                content_type = response.headers.get("content-type")
                if "image/gif" in content_type:
                    gif_data = response.content
                    filename = gif_url.split("/")[-1]
                    save_path = self.get_save_path(filename)

                    with open(save_path, "wb") as f:
                        f.write(gif_data)

                    self.status_label.config(text=f"GIF downloaded and saved as: {save_path}")
                else:
                    self.status_label.config(text="The provided URL is not a valid GIF.")
            else:
                self.status_label.config(text="Error downloading GIF.")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def get_save_path(self, filename):
        default_dir = os.path.expanduser("~")
        save_path = filedialog.asksaveasfilename(
            initialdir=default_dir,
            initialfile=filename,
            defaultextension=".gif",
            filetypes=[("GIF Files", "*.gif")]
        )
        return save_path

if __name__ == "__main__":
    root = tk.Tk()
    app = GIFDownloaderApp(root)
    root.mainloop()
