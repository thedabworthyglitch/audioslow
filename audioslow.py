import os
import numpy as np
import soundfile as sf
import tkinter as tk
from tkinter import filedialog

# Function to slow down or speed up audio
def manipulate_audio():
    global original_audio, sample_rate
    speed_factor = speed_slider.get() / 100.0
    new_audio = change_speed(original_audio, sample_rate, speed_factor)
    
    if reverb_var.get():
        reverb_amount = reverb_slider.get() / 100.0
        new_audio = apply_reverb(new_audio, reverb_amount)
    
    output_filename = generate_output_filename(speed_factor)
    sf.write(output_filename, new_audio, sample_rate)
    status_label.config(text="Audio manipulation completed and saved as: " + output_filename)

# Function to change the speed of audio
def change_speed(audio, sample_rate, speed_factor):
    new_length = int(len(audio) / speed_factor)
    
    # Flatten the audio array
    flat_audio = audio.flatten()
    
    new_audio = np.interp(
        np.linspace(0, len(flat_audio) - 1, new_length),
        np.arange(len(flat_audio)),
        flat_audio
    )
    return new_audio

# Function to apply reverb effect
def apply_reverb(audio, amount):
    reverb = np.random.normal(size=len(audio))
    audio_with_reverb = audio + amount * reverb
    return audio_with_reverb

# Function to generate output filename based on manipulation
def generate_output_filename(speed_factor):
    if speed_factor < 1:
        speed_type = "slowed"
    else:
        speed_type = "sped_up"
    
    return f"audio_{speed_type}_{int(speed_factor * 100)}_percent.wav"

# Function to select an audio file
def select_audio_file():
    global original_audio, sample_rate
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.flac")])
    original_audio, sample_rate = sf.read(file_path)
    status_label.config(text="Selected audio file: " + os.path.basename(file_path))

# Create the main GUI window
root = tk.Tk()
root.title("Audio Manipulation App")

# Create UI components
select_button = tk.Button(root, text="Select Audio File", command=select_audio_file)
speed_slider = tk.Scale(root, from_=0, to=200, label="Speed %")
reverb_var = tk.IntVar()
reverb_checkbox = tk.Checkbutton(root, text="Enable Reverb", variable=reverb_var)
reverb_slider = tk.Scale(root, from_=0, to=100, label="Reverb Amount %")
manipulate_button = tk.Button(root, text="Manipulate Audio", command=manipulate_audio)
status_label = tk.Label(root, text="")

# Position UI components using grid layout
select_button.grid(row=0, column=0, pady=10)
speed_slider.grid(row=1, column=0, pady=10)
reverb_checkbox.grid(row=2, column=0, pady=10)
reverb_slider.grid(row=3, column=0, pady=10)
manipulate_button.grid(row=4, column=0, pady=10)
status_label.grid(row=5, column=0, pady=10)

# Start the GUI event loop
root.mainloop()