import os
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment

class AudioConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Converter")

        self.input_file_path = None
        self.target_format = tk.StringVar()
        self.target_format.set("mp3")  # Default target format

        self.create_ui()

    def create_ui(self):
        input_button = tk.Button(self.root, text="Select Input File", command=self.select_input_file)
        input_button.pack(pady=10)

        target_format_label = tk.Label(self.root, text="Select Target Format:")
        target_format_label.pack()

        format_options = ["mp3", "aac", "m4a", "flac", "wav"]
        target_format_menu = tk.OptionMenu(self.root, self.target_format, *format_options)
        target_format_menu.pack()

        export_button = tk.Button(self.root, text="Export Converted Audio", command=self.export_audio)
        export_button.pack(pady=10)

        self.status_label = tk.Label(self.root, text="", wraplength=400)
        self.status_label.pack(pady=10)

    def select_input_file(self):
        self.input_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.aac *.m4a *.flac *.wav")])
        self.status_label.config(text="Selected input file: " + self.input_file_path)

    def export_audio(self):
        if self.input_file_path is None:
            self.status_label.config(text="Please select an input file.")
            return

        input_filename, input_ext = os.path.splitext(os.path.basename(self.input_file_path))
        target_ext = self.target_format.get()
        output_file_path = os.path.join(os.path.dirname(self.input_file_path), f"{input_filename}.{target_ext}")

        try:
            audio = AudioSegment.from_file(self.input_file_path)
            audio.export(output_file_path, format=target_ext)
            self.status_label.config(text=f"Audio converted and exported to: {output_file_path}")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioConverterApp(root)
    root.mainloop()
