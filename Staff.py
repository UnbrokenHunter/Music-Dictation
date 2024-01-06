import music21
from music21 import metadata
from tkinter import *
from PIL import Image, ImageTk
import os, shutil
import time

latest_file = None  # Global variable to keep track of the latest file

def generate_unique_filename(base="temp_score", extension=".png"):
    timestamp = int(time.time())  # Current time as a unique identifier
    return f"{base}_{timestamp}{extension}"

def staff(app, root):

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

        # Load the new image
        img = Image.open(image_path)
        img = img.resize((500, int(1.41 * 500)))  # Resize as needed
        img_photo = ImageTk.PhotoImage(img)

        # Update or recreate the label with the new image
        label = Label(window, image=img_photo)
        label.image = img_photo  # Keep a reference to the image

        # Configure the grid layout to center the label
        window.grid_rowconfigure(0, weight=1)
        window.grid_rowconfigure(2, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_columnconfigure(2, weight=1)
    
        label.grid(row=0, column=1)

    # Assuming app.melody is a music21 stream object containing your melody
    # Generate sheet music image
    image_path = generate_sheet_music_image(app.melody)

    # Inside the staff function
    print(f"Image Path: {str(image_path)}")

    # Display the sheet music image in Tkinter
    display_sheet_music(root, image_path)
