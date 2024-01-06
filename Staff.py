import music21
from music21 import metadata
from tkinter import *
from PIL import Image, ImageTk
import os, shutil
import time
from copy import deepcopy

latest_file = None  # Global variable to keep track of the latest file
img_photo = None

def create_no_notes_version(melody_stream):
    # Create a deep copy of the melody stream using Python's deepcopy
    no_notes_stream = deepcopy(melody_stream)

    i = 0

    # Iterate over the elements and replace notes with rests
    for element in no_notes_stream.recurse():
        if i > 1:
            if isinstance(element, music21.note.Note) or isinstance(element, music21.chord.Chord):
                # Replace the note or chord with a rest of the same duration
                rest = music21.note.Rest(duration=element.duration)
                index = element.getOffsetBySite(no_notes_stream)
                no_notes_stream.remove(element, recurse=True)
                no_notes_stream.insert(index, rest)
        i += 1

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

def staff(app, root, display_notes=False):

    print("Staff Method")

    def generate_sheet_music_image(stream):
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

        # Remove titles and other metadata
        stream.metadata = metadata.Metadata()
        stream.metadata.title = " "
        stream.metadata.composer = " "

        # Set page layout settings to minimize background
        # Adjust as necessary to suit your needs
        for pageLayout in stream.recurse(classFilter=('PageLayout',)):
            pageLayout.leftMargin = 10
            pageLayout.rightMargin = 10
            pageLayout.topMargin = 10
            pageLayout.bottomMargin = 10

        # Adjust system layout settings
        for systemLayout in stream.recurse().getElementsByClass('SystemLayout'):
            systemLayout.systemDistance = 150  # Adjust this value as needed

        # Generate the score and write it to a MusicXML file
        musicxml_path = stream.write('musicxml')

        # Set the path to MuseScore
        # Replace 'path_to_musescore' with the actual path to the MuseScore3.exe file on your system
        music21.environment.set('musescoreDirectPNGPath', "C:\Program Files\MuseScore 4\\bin\MuseScore4.exe")

        # Convert MusicXML to PNG using music21
        # The write method returns the path to the generated PNG file
        fp = music21.converter.parse(musicxml_path).write('musicxml.png', fp=file_path)
        # Update the latest_file variable
        latest_file = fp
        return fp

    def display_sheet_music(window, image_path):
        global img_photo  # Use a global variable to keep a reference to the image

        # Load the image from the file path
        img = Image.open(image_path)

        # Desired width or height
        desired_width = int(window.winfo_screenwidth() * 2/3)
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

        # Bind the mouse click event to the canvas
        canvas.bind("<Button-1>", on_canvas_click)

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
