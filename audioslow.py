import os
import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from scipy import signal

# Function to change the speed of audio using resampling
def change_speed(audio, sample_rate, speed_factor):
    num_samples = len(audio)
    new_num_samples = int(num_samples / speed_factor)
    new_audio = signal.resample(audio, new_num_samples)
    return new_audio

# Function to apply reverb effect
def apply_reverb(audio, amount):
    reverb = np.random.normal(size=len(audio))
    audio_with_reverb = audio + amount * reverb
    return audio_with_reverb

# Function to generate output filename based on manipulation
def generate_output_filename(original_filename, speed_factor, reverb_strength):
    filename, extension = os.path.splitext(original_filename)
    speed_type = "slowed" if speed_factor < 1 else "sped_up"
    reverb_str = f"_reverb_{int(reverb_strength * 100)}" if reverb_strength > 0 else ""
    new_filename = f"{filename}_{speed_type}_{int(speed_factor * 100)}_percent{reverb_str}{extension}"
    return new_filename

# Function to manipulate audio
def manipulate_audio():
    global original_audio, sample_rate
    speed_factor = speed_slider.get() / 100.0
    reverb_strength = reverb_slider.get() / 100.0

    new_audio = change_speed(original_audio, sample_rate, speed_factor)
    
    if reverb_strength > 0:
        new_audio = apply_reverb(new_audio, reverb_strength)
    
    output_filename = generate_output_filename(original_filename, speed_factor, reverb_strength)
    sf.write(output_filename, new_audio, sample_rate)
    status_label.config(text="Audio manipulation completed and saved as: " + output_filename)
    export_button.config(state=tk.NORMAL)  # Enable the export button

# Function to update the progress bar
def update_progress(value):
    progress_bar["value"] = value
    root.update_idletasks()

# Function to select an audio file
def select_audio_file():
    global original_audio, sample_rate, original_filename
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac")])
    original_audio, sample_rate = sf.read(file_path)
    original_filename = os.path.basename(file_path)
    status_label.config(text="Selected audio file: " + original_filename)
    update_progress(0)  # Reset progress bar
    export_button.config(state=tk.DISABLED)  # Disable the export button until manipulation is done

# Create the main GUI window
root = tk.Tk()
root.title("Audio Manipulation App")

# Create UI components
select_button = tk.Button(root, text="Select Audio File", command=select_audio_file)
speed_slider = tk.Scale(root, from_=1, to=200, label="Speed %", orient="horizontal", length=300)
reverb_slider = tk.Scale(root, from_=0, to=100, label="Reverb Strength %", orient="horizontal", length=300)
manipulate_button = tk.Button(root, text="Process Audio", command=manipulate_audio)
export_button = tk.Button(root, text="Export Audio", command=export_audio, state=tk.DISABLED)
progress_bar = ttk.Progressbar(root, mode="determinate")
status_label = tk.Label(root, text="", wraplength=400)

# Position UI components using grid layout
select_button.grid(row=0, column=0, padx=10, pady=10)
speed_slider.grid(row=1, column=0, padx=10, pady=10)
reverb_slider.grid(row=2, column=0, padx=10, pady=10)
manipulate_button.grid(row=3, column=0, padx=10, pady=10)
export_button.grid(row=4, column=0, padx=10, pady=10)
progress_bar.grid(row=5, column=0, padx=10, pady=10)
status_label.grid(row=6, column=0, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
