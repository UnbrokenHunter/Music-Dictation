import tkinter as tk
from tkinter import ttk
from tkinter import font

def settings(app, root):
    title_font = font.Font(family="Helvetica", size=12, weight="bold")

    # General settings section title
    general_settings_label = tk.Label(root, text="General Settings", font=title_font)
    general_settings_label.grid(row=1, column=0, columnspan=4, sticky='w', padx=10, pady=5)
    general_settings_line = tk.Frame(root, height=2, bg="black")
    general_settings_line.grid(row=2, column=0, columnspan=4, sticky='ew', padx=10)

    general_settings_frame = tk.Frame(root)
    general_settings_frame.grid(row=3, column=0, columnspan=4, sticky='w', padx=10, pady=10)

    # Function to update mode and display relevant options
    def update_mode():
        scale_interval_label.grid(row=4, column=0, columnspan=4, sticky='w', padx=10, pady=5)
        scale_interval_line.grid(row=5, column=0, columnspan=4, sticky='ew', padx=10)

        if app.mode_var.get() == "Scale":
            interval_frame.grid_remove()
            scale_frame.grid(row=6, column=0, columnspan=4, sticky='w', padx=10, pady=10)
        else:
            scale_frame.grid_remove()
            interval_frame.grid(row=6, column=0, columnspan=4, sticky='w', padx=10, pady=10)
            scale_interval_label.config(text="Interval Settings")

    # Mode selection (Scale or Interval) in General Settings Frame
    app.mode_var = tk.StringVar(value="Scale")
    scale_mode_rb = tk.Radiobutton(general_settings_frame, text="Scale Mode", variable=app.mode_var, value="Scale", command=update_mode)
    interval_mode_rb = tk.Radiobutton(general_settings_frame, text="Interval Mode", variable=app.mode_var, value="Interval", command=update_mode)
    scale_mode_rb.grid(row=1, column=0, sticky='w', padx=10, pady=5)
    interval_mode_rb.grid(row=1, column=1, sticky='w', padx=10, pady=5)

    # Number of Notes (Text Input) with default value
    length_label = tk.Label(general_settings_frame, text="Number of notes:")
    length_label.grid(row=2, column=0, sticky='w')
    app.length_var = tk.Entry(general_settings_frame)
    app.length_var.insert(0, "8")  # Default value
    app.length_var.grid(row=2, column=1, sticky='w')

    # Keys (Dropdown) with default value
    key_label = tk.Label(general_settings_frame, text="Select key:")
    key_label.grid(row=2, column=2, sticky='w')
    app.key_var = ttk.Combobox(general_settings_frame, values=["Random", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"], state="readonly")
    app.key_var.set("C")  # Default value
    app.key_var.grid(row=2, column=3, sticky='w')

    # Tempo (Text Input) with default value
    tempo_label = tk.Label(general_settings_frame, text="Tempo (BPM):")
    tempo_label.grid(row=2, column=4, sticky='w')
    app.tempo_var = tk.Entry(general_settings_frame)
    app.tempo_var.insert(0, "120")  # Default value
    app.tempo_var.grid(row=2, column=5, sticky='w')

    # Time Signature (Dropdown)
    time_signature_label = tk.Label(general_settings_frame, text="Time Signature:")
    time_signature_label.grid(row=2, column=6, sticky='w')
    app.time_signature_var = ttk.Combobox(general_settings_frame, values=["4/4", "3/4", "2/4", "6/8", "5/4", "7/8", "15/16"], state="readonly")
    app.time_signature_var.set("4/4")  # Default value
    app.time_signature_var.grid(row=2, column=7, sticky='w')

    # Min Octave (Text Input) with default value
    min_octave_label = tk.Label(general_settings_frame, text="Min Octave:")
    min_octave_label.grid(row=3, column=0, sticky='w')
    app.min_octave_var = tk.Entry(general_settings_frame)
    app.min_octave_var.insert(0, "3")  # Default value
    app.min_octave_var.grid(row=3, column=1, sticky='w')

    # Max Octave (Text Input) with default value
    max_octave_label = tk.Label(general_settings_frame, text="Max Octave:")
    max_octave_label.grid(row=3, column=2, sticky='w')  # Adjusted the row for proper layout
    app.max_octave_var = tk.Entry(general_settings_frame)
    app.max_octave_var.insert(0, "5")  # Default value
    app.max_octave_var.grid(row=3, column=3, sticky='w')

    # UI Scale (Text Input) with default value
    ui_scale_label = tk.Label(general_settings_frame, text="UI Scale:")
    ui_scale_label.grid(row=3, column=4, sticky='w')  # Adjusted the row for proper layout
    app.ui_scale_var = tk.Entry(general_settings_frame)
    app.ui_scale_var.insert(0, "2/3")  # Default value
    app.ui_scale_var.grid(row=3, column=5, sticky='w')

    # Scale or Interval settings section title
    scale_interval_label = tk.Label(root, text="Scale Settings", font=title_font)
    scale_interval_label.grid(row=4, column=0, columnspan=4, sticky='w', padx=10, pady=5)
    scale_interval_line = tk.Frame(root, height=2, bg="black")
    scale_interval_line.grid(row=5, column=0, columnspan=4, sticky='ew', padx=10)

    # Frame for Scale options
    scale_frame = tk.Frame(root)
    scale_notes = ["Tonic", "Supertonic", "Mediant", "Subdominant", "Dominant", "Submediant", "Leading Tone"]
    for i, note in enumerate(scale_notes):
        var = tk.BooleanVar()
        app.scale_note_vars[note] = var
        checkbox = tk.Checkbutton(scale_frame, text=note, variable=var)
        checkbox.grid(row=i // 4, column=i % 4, sticky='w', padx=5, pady=2)

    # Dropdown for scale types
    scale_types = ["Major", "Minor", "Natural Minor", "Harmonic Minor", "Chromatic"]
    app.scale_type_var = ttk.Combobox(scale_frame, values=scale_types,  textvariable="Major")
    app.scale_type_var.current(0)
    app.scale_type_var.grid(row=4, columnspan=4, padx=5, pady=2)

    # Frame for Interval options
    interval_frame = tk.Frame(root)
    intervals = ["P1", "m2", "M2", "m3", "M3", "P4", "P5", "m6", "M6", "m7", "M7", "P8"]
    for i, interval in enumerate(intervals):
        var = tk.BooleanVar()
        app.interval_vars[interval] = var
        checkbox = tk.Checkbutton(interval_frame, text=interval, variable=var)
        checkbox.grid(row=i // 6, column=i % 6, sticky='w', padx=5, pady=2)

    update_mode()
