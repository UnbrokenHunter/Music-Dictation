import music21
from music21 import stream, clef, note, metadata, pitch, duration, chord
from tkinter import *
from PIL import Image, ImageTk
import os, shutil
import time
from copy import deepcopy

latest_file = None  # Global variable to keep track of the latest file
img_photo = None
dots = []  # List to store the coordinates of the dots
canvas = None

def convert_fraction_to_float(input_str):
    try:
        if '/' in input_str:
            # Handle as a fraction
            numerator, denominator = input_str.split('/')
            return float(numerator) / float(denominator)
        else:
            # Handle as a regular integer or float
            return float(input_str)
    except (ValueError, ZeroDivisionError):
        print("Invalid input or division by zero")
        return None  # or a default value

def create_no_notes_version(melody_stream):
    # Create a deep copy of the melody stream using Python's deepcopy
    no_notes_stream = deepcopy(melody_stream)

    # A flag to track if the first note/chord has been encountered
    first_note_encountered = False

    # Iterate over the elements and replace notes with rests starting from the second note
    for element in no_notes_stream.recurse():
        if isinstance(element, (music21.note.Note, music21.chord.Chord)):
            if first_note_encountered:
                # Replace the note or chord with a rest of the same duration
                rest = music21.note.Rest(duration=element.duration)
                index = element.getOffsetBySite(no_notes_stream)
                no_notes_stream.remove(element, recurse=True)
                no_notes_stream.insert(index, rest)
            else:
                first_note_encountered = True  # Mark that the first note/chord has been encountered

    return no_notes_stream

def generate_unique_filename(base="temp_score", extension=".png"):
    timestamp = int(time.time())  # Current time as a unique identifier
    return f"{base}_{timestamp}{extension}"

def crop_to_black_pixels(image_path, padding=20):
    # Open the image
    img = Image.open(image_path)

    # Convert the image to grayscale
    grayscale = img.convert('L')

    # Initialize min/max values
    left, top, right, bottom = img.width, img.height, 0, 0

    # Process each pixel
    for x in range(img.width):
        for y in range(img.height):
            # Check if the pixel is not white (assuming black or colored pixels)
            if grayscale.getpixel((x, y)) < 250:  # Threshold for non-white; may need adjustment
                # Update the bounds for cropping
                if x < left:
                    left = x
                if y < top:
                    top = y
                if x > right:
                    right = x
                if y > bottom:
                    bottom = y

    # Check if any non-white pixel found
    if left < right and top < bottom:
        # Apply padding
        left = max(left - padding, 0)
        top = max(top - padding, 0)
        right = min(right + padding, img.width)
        bottom = min(bottom + padding, img.height)

        # Crop the image
        img_cropped = img.crop((left, top, right, bottom))
        return img_cropped
    else:
        # No non-white pixels found; return original image
        return img

def staff(app, root, is_chromatic, display_notes=False):

    if display_notes == False:
        dots.clear()

    def generate_sheet_music_image(streams):
        global latest_file

        if not os.path.exists("img"):
            os.mkdir("img")
        else:
            folder = 'img'
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

        # Generate a new unique filename
        file_path = generate_unique_filename(base="img/temp_score")

        def split_into_staves(streams):
            treble_staff = stream.PartStaff()
            treble_staff.clef = clef.TrebleClef()

            bass_staff = stream.PartStaff()
            bass_staff.clef = clef.BassClef()

            # Define the cutoff pitch (e.g., Middle C)
            cutoff_pitch = pitch.Pitch('C4')
            current_offset = 0.0  # Keep track of the current offset

            print("\nStaff Notes\n-----------\n")
            print(f"Is Chromatic: {is_chromatic}")

            key = streams.keySignature

            for element in streams.recurse():
                if isinstance(element, note.Note):
                    # Decide the staff based on the pitch of the note
                    if element.pitch >= cutoff_pitch:
                        treble_staff.insert(current_offset, element)
                    else:
                        bass_staff.insert(current_offset, element)
                    current_offset += element.duration.quarterLength
                    
                    if not is_chromatic:
                        nStep = element.pitch.step
                        rightAccidental = key.accidentalByStep(nStep)
                        element.pitch.accidental = rightAccidental

                    # print(f"{element.pitch} \n")

                elif isinstance(element, chord.Chord):
                    # For chords, check if the root note is above or below the cutoff
                    if element.root().pitch >= cutoff_pitch:
                        treble_staff.insert(current_offset, element)
                    else:
                        bass_staff.insert(current_offset, element)
                    current_offset += element.duration.quarterLength
                elif isinstance(element, note.Rest):
                    # For rests, place a quarter rest in both staves
                    quarter_rest = note.Rest(duration=duration.Duration("quarter"))
                    treble_staff.append(quarter_rest)
                    bass_staff.append(quarter_rest)
                elif isinstance(element, (music21.meter.TimeSignature, music21.key.KeySignature)):
                    # Insert time signatures and key signatures at the beginning
                    treble_staff.insert(0, deepcopy(element))
                    bass_staff.insert(0, deepcopy(element))

            return treble_staff, bass_staff

        # Create PartStaff objects for treble and bass
        treble_staff = stream.PartStaff()
        bass_staff = stream.PartStaff()
    
        # Assign clefs to each staff
        treble_staff.clef = clef.TrebleClef()
        bass_staff.clef = clef.BassClef()
    
        # Add a whole rest to each staff to ensure they are displayed
        whole_rest = note.Rest(duration=duration.Duration("whole"))
        treble_staff.append(whole_rest)
        bass_staff.append(whole_rest)
    
        # Split notes into treble and bass staves
        treble_staff, bass_staff = split_into_staves(streams)
    
        # Create a grand staff (a Score object) and add the treble and bass PartStaffs
        grand_staff = stream.Score()
        grand_staff.insert(0, treble_staff)
        grand_staff.insert(0, bass_staff)
    
        # Remove titles and other metadata
        grand_staff.metadata = metadata.Metadata()
        grand_staff.metadata.title = " "
        grand_staff.metadata.composer = " "

        # Write the grand staff to a MusicXML file
        musicxml_path = grand_staff.write('musicxml')
    
        # Set the path to MuseScore and convert MusicXML to PNG
        music21.environment.set('musescoreDirectPNGPath', r"C:\\Program Files\\MuseScore 4\\bin\\MuseScore4.exe")
        png_path = music21.converter.parse(musicxml_path).write('musicxml.png', fp=file_path)
    
        # Update the latest_file variable
        latest_file = png_path
        return png_path

    def display_sheet_music(window, image_path):
        global img_photo  # Use a global variable to keep a reference to the image
        global canvas

        # Load the image from the file path
        img = Image.open(image_path)

        # Desired width or height
        input_str = app.ui_scale_var.get()  # Get the string from the Entry widget
        ui_scale = convert_fraction_to_float(input_str)
        desired_width = int(window.winfo_screenwidth() * ui_scale)
        desired_height = 500

        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height

        # Resize while maintaining aspect ratio
        if img.width > img.height:
            new_width = desired_width
            new_height = int(desired_width / aspect_ratio)
        else:
            new_height = desired_height
            new_width = int(desired_height * aspect_ratio)

        img = img.resize((new_width, new_height))

        # Convert the Image object to a format that Tkinter can use
        img_photo = ImageTk.PhotoImage(img)

        # Create and place the canvas
        canvas = Canvas(window, width=new_width, height=new_height)
        canvas.create_image(new_width // 2, new_height // 2, anchor='center', image=img_photo)

        # Configure the grid layout to center the canvas
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)

        canvas.grid(row=0, column=1)

        # Function to handle mouse clicks on the canvas
        def on_canvas_click(event):
            # x and y are the coordinates of the mouse click
            x, y = event.x, event.y

            # Create a semi-transparent red marker
            radius = 5
            marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red', stipple='gray50')

            # Store the coordinates of the dot in the dots list
            dots.append((x, y))

            # Convert the dots list to a string and print it
            dots_str = ", ".join(map(str, dots))
            print("Dots added: " + dots_str)

        # Bind the mouse click event to the canvas
        canvas.bind("<Button-1>", on_canvas_click)

    # Function to display dots on the canvas
    def display_dots():
        global canvas
        for x, y in dots:
            # Create a semi-transparent red marker
            radius = 5
            marker = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill='red', stipple='gray50')


    # Use a flag `display_notes` to determine which version to display

    if display_notes:
        # Generate the image with notes
        image_path = generate_sheet_music_image(app.melody)
    else:
        # Generate the image without notes
        image_path = generate_sheet_music_image(create_no_notes_version(app.melody))  # Assume you have this version

    # Crop the image to black pixels and add padding
    cropped_image = crop_to_black_pixels(image_path)

    # Ensure the 'img' directory exists
    if not os.path.exists('img'):
        os.mkdir('img')

    # Generate a unique filename for the cropped image
    cropped_image_path = generate_unique_filename(base="img/temp_cropped")

    # Save the cropped image
    cropped_image.save(cropped_image_path)

    # Display the cropped image in Tkinter
    display_sheet_music(root, cropped_image_path)

    # Display the dots on the canvas    
    display_dots()
