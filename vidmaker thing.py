import os
import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from scipy import signal
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip

class AudioVideoSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AudioVideoSync - Audio and Video Manipulation App")

        self.original_audio = None
        self.sample_rate = None
        self.original_audio_filename = None
        self.original_video_filename = None

        self.create_ui()

    def create_ui(self):
        audio_select_button = tk.Button(self.root, text="Select Audio File", command=self.select_audio_file)
        audio_select_button.pack(pady=10)

        video_select_button = tk.Button(self.root, text="Select Video/GIF File", command=self.select_video_file)
        video_select_button.pack(pady=10)

        self.speed_slider = tk.Scale(self.root, from_=1, to=200, label="Speed %", orient="horizontal", length=300)
        self.speed_slider.pack()

        manipulate_button = tk.Button(self.root, text="Process and Create Video", command=self.process_and_create_video)
        manipulate_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", wraplength=400)
        self.status_label.pack(pady=10)

    def process_and_create_video(self):
        if self.original_audio is None or self.original_video_filename is None:
            self.status_label.config(text="Please select an audio file and a video/GIF file first.")
            return

        speed_factor = self.speed_slider.get() / 100.0
        audio_output_filename = self.generate_output_filename(speed_factor, "audio")

        new_audio = self.change_speed(self.original_audio, speed_factor)

        output_directory = os.path.dirname(self.original_audio_filename)
        audio_output_filepath = os.path.join(output_directory, audio_output_filename)
        sf.write(audio_output_filepath, new_audio, self.sample_rate, format='FLAC')

        video_clip = VideoFileClip(self.original_video_filename)
        audio_clip = AudioFileClip(audio_output_filepath)
        audio_clip = audio_clip.subclip(0, video_clip.duration)

        final_video_clip = video_clip.set_audio(audio_clip)

        output_video_filename = self.generate_output_filename(speed_factor, "video") + ".mp4"
        output_video_filepath = os.path.join(output_directory, output_video_filename)

        final_video_clip.write_videofile(output_video_filepath, codec="libx264")

        self.status_label.config(text="Audio and video processing completed. Created video: " + output_video_filepath)

    def change_speed(self, audio, speed_factor):
        num_samples = len(audio)
        new_num_samples = int(num_samples / speed_factor)
        new_audio = signal.resample(audio, new_num_samples)
        return new_audio

    def generate_output_filename(self, speed_factor, file_type):
        filename, _ = os.path.splitext(self.original_audio_filename)
        speed_type = "sped_up" if speed_factor > 1 else "slowed"
        return f"{filename}_{speed_type}_{int(abs(speed_factor) * 100)}_{file_type}"

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac")])
        self.original_audio, self.sample_rate = sf.read(file_path)
        self.original_audio_filename = file_path
        self.status_label.config(text="Selected audio file: " + self.original_audio_filename)

    def select_video_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video/GIF Files", "*.mp4 *.gif")])
        self.original_video_filename = file_path
        self.status_label.config(text="Selected video/GIF file: " + self.original_video_filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioVideoSyncApp(root)
    root.mainloop()
