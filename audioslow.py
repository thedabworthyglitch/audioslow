import os
import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from scipy import signal

class AudioSlowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AudioSlow - Audio Manipulation App")

        self.original_audio = None
        self.sample_rate = None
        self.original_filename = None

        self.create_ui()

    def create_ui(self):
        select_button = tk.Button(self.root, text="Select Audio File", command=self.select_audio_file)
        select_button.pack(pady=10)

        self.speed_slider = tk.Scale(self.root, from_=1, to=200, label="Speed %", orient="horizontal", length=300)
        self.speed_slider.pack()

        manipulate_button = tk.Button(self.root, text="Manipulate Audio", command=self.manipulate_audio)
        manipulate_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", wraplength=400)
        self.status_label.pack(pady=10)

    def manipulate_audio(self):
        if self.original_audio is None:
            self.status_label.config(text="Please select an audio file first.")
            return

        speed_factor = self.speed_slider.get() / 100.0

        new_audio = self.change_speed(self.original_audio, speed_factor)

        output_filename = self.generate_output_filename(speed_factor)

        # Create "processed" subdirectory in the same location as the selected audio file
        output_directory = os.path.join(os.path.dirname(self.original_filename), "processed")
        os.makedirs(output_directory, exist_ok=True)

        output_filepath = os.path.join(output_directory, output_filename)
        sf.write(output_filepath, new_audio, self.sample_rate)

        self.status_label.config(text="Audio manipulation completed and saved as: " + output_filepath)

    def change_speed(self, audio, speed_factor):
        num_samples = len(audio)
        new_num_samples = int(num_samples / speed_factor)
        new_audio = signal.resample(audio, new_num_samples)
        return new_audio

    def generate_output_filename(self, speed_factor):
        filename, extension = os.path.splitext(self.original_filename)
        if speed_factor > 1:
            speed_type = "sped_up"
        else:
            speed_type = "slowed"
        new_filename = f"{filename}_{speed_type}_{int(abs(speed_factor) * 100)}_percent{extension}"
        return new_filename

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac")])
        self.original_audio, self.sample_rate = sf.read(file_path)
        self.original_filename = file_path
        self.status_label.config(text="Selected audio file: " + self.original_filename)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSlowApp(root)
    root.mainloop()
