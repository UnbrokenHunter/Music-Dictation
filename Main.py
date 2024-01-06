import tkinter as tk
from tkinter import ttk
from tkinter import font

from GenerateMelody import generate_random_melody
from PlayMelody import play_melody

# Global variables for interval and scale type selection
interval_vars = {}
scale_note_vars = {}
scale_type_var = None
melody = None  # Initialize melody as None


def main():
    root = tk.Tk()
    root.title("Music Dictation Practice")

    title_font = font.Font(family="Helvetica", size=12, weight="bold")

    # General settings section title
    general_settings_label = tk.Label(root, text="General Settings", font=title_font)
    general_settings_label.grid(row=0, column=0, columnspan=4, sticky='w', padx=10, pady=5)
    general_settings_line = tk.Frame(root, height=2, bg="black")
    general_settings_line.grid(row=1, column=0, columnspan=4, sticky='ew', padx=10)

    general_settings_frame = tk.Frame(root)
    general_settings_frame.grid(row=2, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    # Function to update mode and display relevant options
    def update_mode():
        scale_interval_label.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        scale_interval_line.grid(row=4, column=0, columnspan=4, sticky='ew', padx=10)

        if mode_var.get() == "Scale":
            interval_frame.grid_remove()
            scale_frame.grid(row=5, column=0, columnspan=4, sticky='w', padx=10, pady=10)
        else:
            scale_frame.grid_remove()
            interval_frame.grid(row=5, column=0, columnspan=4, sticky='w', padx=10, pady=10)
            scale_interval_label.config(text="Interval Settings")

    # Mode selection (Scale or Interval) in General Settings Frame
    mode_var = tk.StringVar(value="Scale")
    scale_mode_rb = tk.Radiobutton(general_settings_frame, text="Scale Mode", variable=mode_var, value="Scale", command=update_mode)
    interval_mode_rb = tk.Radiobutton(general_settings_frame, text="Interval Mode", variable=mode_var, value="Interval", command=update_mode)
    scale_mode_rb.grid(row=0, column=0, sticky='w', padx=10, pady=5)
    interval_mode_rb.grid(row=0, column=1, sticky='w', padx=10, pady=5)

    # Number of Notes (Text Input) with default value
    length_label = tk.Label(general_settings_frame, text="Number of notes:")
    length_label.grid(row=1, column=0, sticky='w')
    length_input = tk.Entry(general_settings_frame)
    length_input.insert(0, "8")  # Default value
    length_input.grid(row=1, column=1, sticky='w')

    # Keys (Dropdown) with default value
    key_label = tk.Label(general_settings_frame, text="Select key:")
    key_label.grid(row=1, column=2, sticky='w')
    key_input = ttk.Combobox(general_settings_frame, values=["C", "D", "E", "F", "G", "A", "B"], state="readonly")
    key_input.set("C")  # Default value
    key_input.grid(row=1, column=3, sticky='w')

    # Tempo (Text Input) with default value
    tempo_label = tk.Label(general_settings_frame, text="Tempo (BPM):")
    tempo_label.grid(row=1, column=4, sticky='w')
    tempo_input = tk.Entry(general_settings_frame)
    tempo_input.insert(0, "120")  # Default value
    tempo_input.grid(row=1, column=5, sticky='w')

    # Time Signature (Dropdown)
    time_signature_label = tk.Label(general_settings_frame, text="Time Signature:")
    time_signature_label.grid(row=1, column=6, sticky='w')
    time_signature_input = ttk.Combobox(general_settings_frame, values=["4/4", "3/4", "2/4", "6/8"], state="readonly")
    time_signature_input.set("4/4")  # Default value
    time_signature_input.grid(row=1, column=7, sticky='w')

    # Scale or Interval settings section title
    scale_interval_label = tk.Label(root, text="Scale Settings", font=title_font)
    scale_interval_label.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=5)
    scale_interval_line = tk.Frame(root, height=2, bg="black")
    scale_interval_line.grid(row=4, column=0, columnspan=4, sticky='ew', padx=10)

    # Frame for Scale options
    scale_frame = tk.Frame(root)
    scale_notes = ["Tonic", "Supertonic", "Mediant", "Subdominant", "Dominant", "Submediant", "Leading Tone"]
    for i, note in enumerate(scale_notes):
        var = tk.BooleanVar()
        scale_note_vars[note] = var
        checkbox = tk.Checkbutton(scale_frame, text=note, variable=var)
        checkbox.grid(row=i // 4, column=i % 4, sticky='w', padx=5, pady=2)

    # Dropdown for scale types
    scale_types = ["Major", "Minor", "Natural Minor", "Harmonic Minor", "Chromatic"]
    scale_type_var = tk.StringVar(value=scale_types[0])
    scale_type_dropdown = ttk.Combobox(scale_frame, values=scale_types, textvariable=scale_type_var)
    scale_type_dropdown.grid(row=2, columnspan=4, padx=5, pady=2)

    # Frame for Interval options
    interval_frame = tk.Frame(root)
    intervals = ["Unison", "m2", "M2", "m3", "M3", "P4", "P5", "m6", "M6", "m7", "M7", "P8"]
    for i, interval in enumerate(intervals):
        var = tk.BooleanVar()
        interval_vars[interval] = var
        checkbox = tk.Checkbutton(interval_frame, text=interval, variable=var)
        checkbox.grid(row=i // 6, column=i % 6, sticky='w', padx=5, pady=2)

    # Buttons for melody generation and playback
    generate_btn = tk.Button(root, text="Generate Melody", command=lambda: on_generate_melody(scale_type_dropdown.get(), key_input.get(), interval_vars, length_input.get(), tempo_input.get(), time_signature_input.get()))
    play_btn = tk.Button(root, text="Play Melody", command=lambda: play_melody(melody))

    # Position the buttons below the scale/interval frames
    generate_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    play_btn.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

    # Canvas for displaying music staff - further implementation needed
    canvas = tk.Canvas(root, width=400, height=200)
    canvas.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    # Initialize with Scale mode
    update_mode()

    root.mainloop()

def on_generate_melody(scale_type, key, allowed_intervals, length, tempo, time_signature=None):
    global melody
    try:
        length = int(length)
        tempo = int(tempo)
        
        # Generate the melody
        melody = generate_random_melody(scale_type, key, allowed_intervals, length, tempo, time_signature)
        
        if melody is None:
            print("Melody generation failed.")
        else:
            print("Melody generated successfully.")
    except ValueError:
        print("Length and tempo must be integers")

if __name__ == "__main__":
    main()
