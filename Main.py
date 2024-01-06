import tkinter as tk

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
    length_var = None
    melody = None 

    def print_debug(self):
        debug_string = "Debug Information:\n"
        
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
        
        if hasattr(self, 'scale_type_var'):
            debug_string += f"Scales: {self.scale_type_var.get()}\n"
        
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

        if hasattr(self, 'length_var'):
            debug_string += f"Length: {self.length_var.get()}\n"
        
        if hasattr(self, 'melody'):
            debug_string += f"Melody: {self.melody}\n"
        
        print(debug_string)

    def main(self):
        root = tk.Tk()
        root.title("Music Dictation Practice")

        global mode_var
        global interval_vars
        global scale_note_vars
        global scale_type_var
        global key_var
        global tempo_var
        global time_signature_var
        global min_octave_var
        global max_octave_var
        global length_var

        settings(self, root)

        # Buttons for melody generation and playback
        generate_btn = tk.Button(root, text="Generate Melody", command=lambda: app.on_generate_melody(
            root=root,
            generation_mode=app.mode_var.get(), 
            scale_type=app.scale_type_var.get(), 
            key=app.key_var.get(), 
            scale_degrees=app.scale_note_vars, 
            allowed_intervals=app.interval_vars, 
            length=app.length_var.get(), 
            tempo=app.tempo_var.get(), 
            time_signature=app.time_signature_var.get(), 
            min_octave=app.min_octave_var.get(),
            max_octave=app.max_octave_var.get()))
        play_btn = tk.Button(root, text="Play Melody", command=lambda: play_melody(app))

        # Position the buttons below the scale/interval frames
        generate_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        play_btn.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

        # Canvas for displaying music staff - further implementation needed
        canvas = tk.Canvas(root, width=500, height=200)
        canvas.grid(row=7, column=0, columnspan=4, padx=10, pady=10)

        root.mainloop()

    def on_generate_melody(self, root, generation_mode, scale_type, key, scale_degrees, allowed_intervals, length, tempo, time_signature, min_octave, max_octave):
        global melody
        try:
            length = int(length)
            tempo = int(tempo)
            
            scale_degrees_values = {key: var.get() for key, var in scale_degrees.items()}
            allowed_intervals_values = {key: var.get() for key, var in allowed_intervals.items()}
            app.melody = generate_random_melody(generation_mode, scale_type, key, scale_degrees_values, allowed_intervals_values, length, tempo, time_signature, min_octave, max_octave)
            
            if app.melody is None:
                print("Melody generation failed.")
            else:
                print("Melody generated successfully.")
        except ValueError:
            print("Length and tempo must be integers")

        app.print_debug()

        staff(app, root)

if __name__ == "__main__":
    app = App()  # Create an instance of the App class
    app.main()   # Call the main method of the App instance
