import tkinter as tk
from tkinter import ttk

from Settings import settings
from GenerateMelody import generate_random_melody
from PlayMelody import play_melody
from Staff import staff

class App: 
    # Global variables
    mode_var = None 
    interval_vars = {}
    scale_note_vars = {}
    scale_type_var = None
    key_var = None
    tempo_var = None
    time_signature_var = None
    min_octave_var = None
    max_octave_var = None    
    ui_scale_var = None    
    length_var = None
    melody = None 
    questions_answered = 0
    questions_answered_var = None

    def print_debug(self):
        debug_string = "\nDebug Information:\n----------------------------\n"
        
        if hasattr(self, 'mode_var'):
            debug_string += f"Mode: {self.mode_var.get()}\n"

        # If Mode equals Scale
        if (hasattr(self, 'interval_vars') and self.mode_var.get() == "Interval"):
            interval_vars_str = ', '.join(f'{key}: {val.get()}' for key, val in self.interval_vars.items() if val.get())
            debug_string += f"Intervals: {{{interval_vars_str}}}\n"
        
        # If Mode equals Interval
        if (hasattr(self, 'scale_note_vars') and self.mode_var.get() == "Scale"):
            scale_note_vars_str = ', '.join(f'{key}: {val.get()}' for key, val in self.scale_note_vars.items() if val.get())
            debug_string += f"Scale Degrees: {{{scale_note_vars_str}}}\n"
                
        if hasattr(self, 'key_var'):
            debug_string += f"Key: {self.key_var.get()}\n"
        
        if hasattr(self, 'tempo_var'):
            debug_string += f"Tempo: {self.tempo_var.get()}\n"
        
        if hasattr(self, 'time_signature_var'):
            debug_string += f"Time Signature: {self.time_signature_var.get()}\n"
        
        if hasattr(self, 'min_octave_var'):
            debug_string += f"Min Octave: {self.min_octave_var.get()}\n"

        if hasattr(self, 'max_octave_var'):
            debug_string += f"Max Octave: {self.max_octave_var.get()}\n"

        if hasattr(self, 'ui_scale_var'):
            debug_string += f"UI Scale: {self.ui_scale_var.get()}\n"

        if hasattr(self, 'length_var'):
            debug_string += f"Length: {self.length_var.get()}\n"
        
        if hasattr(self, 'questions_answered'):
            debug_string += f"Questions Answered: {self.questions_answered}\n"

        if hasattr(self, 'melody'):
            debug_string += f"Melody: {self.melody}\n"
        
        print(debug_string)

    def main(self):
        root = tk.Tk()
        root.title("Music Dictation Practice")

        global mode_var
        global interval_vars
        global scale_note_vars
        global key_var
        global tempo_var
        global time_signature_var
        global min_octave_var
        global max_octave_var
        global ui_scale_var
        global length_var
        global questions_answered
        global questions_answered_var

        settings(self, root)

        # Create a frame for the buttons
        buttons_frame = tk.Frame(root)
        buttons_frame.grid(row=7, column=0, columnspan=4, sticky="ew")

        # Configure the grid to allow the frame to expand and fill the space
        root.grid_rowconfigure(7, weight=1)
        root.grid_columnconfigure(0, weight=1)

        # Buttons for melody generation and playback
        generate_btn = tk.Button(buttons_frame, text="Generate Melody", command=lambda: app.on_generate_melody(
            root=root,
            generation_mode=app.mode_var.get(), 
            key=app.key_var.get(), 
            scale_degrees=app.scale_note_vars, 
            allowed_intervals=app.interval_vars, 
            length=app.length_var.get(), 
            tempo=app.tempo_var.get(), 
            time_signature=app.time_signature_var.get(), 
            min_octave=app.min_octave_var.get(),
            max_octave=app.max_octave_var.get()))
        reveal_btn = tk.Button(buttons_frame, text="Reveal Notes", command=lambda: self.on_reveal_melody(root))
        play_btn = tk.Button(buttons_frame, text="Play Melody", command=lambda: play_melody(self))

        # Pack the buttons in the buttons frame with padding and expand/fill options
        generate_btn.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.BOTH)
        reveal_btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.BOTH)
        play_btn.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.BOTH)

        # Canvas for displaying music staff - further implementation needed
        canvas = tk.Canvas(root, width=500, height=0)
        canvas.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

        questions_answered_var = tk.StringVar()
        questions_answered = 0
        questions_answered_var.set(f"Questions Answered: {questions_answered}")

        questions_answered_label = tk.Label(root, textvariable=questions_answered_var)
        questions_answered_label.grid(row=1, column=2, sticky='w', padx=10, pady=10)

        root.mainloop()

    def update_questions_answered(self):
        global questions_answered
        global questions_answered_var
        questions_answered += 1
        questions_answered_var.set(f"Questions Answered: {questions_answered}")


    def on_reveal_melody(self, root):
        staff(app, root, app.key_var == "Chromatic", display_notes=True)
        app.update_questions_answered()

    def on_generate_melody(self, root, generation_mode, key, scale_degrees, allowed_intervals, length, tempo, time_signature, min_octave, max_octave):
        
        print("\nGenerating Melody \n----------------\n\n")
        global melody
        try:
            length = int(length)
            tempo = int(tempo)
            
            scale_degrees_values = {key: var.get() for key, var in scale_degrees.items()}
            allowed_intervals_values = {key: var.get() for key, var in allowed_intervals.items()}
            app.melody = generate_random_melody(generation_mode, key, scale_degrees_values, allowed_intervals_values, length, tempo, time_signature, min_octave, max_octave)
            
            if app.melody is None:
                print("Melody generation failed.")
            else:
                print("Melody generated successfully.")
        except ValueError:
            print("Length and tempo must be integers")

        app.print_debug()

        staff(app, root, key == "Chromatic")
        play_melody(self)

if __name__ == "__main__":
    app = App()  # Create an instance of the App class
    app.main()   # Call the main method of the App instance
