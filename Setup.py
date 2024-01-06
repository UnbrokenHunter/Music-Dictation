import sys
from cx_Freeze import setup, Executable
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    executables = [Executable("Music Dictation", base=base)]
    setup(name="Music Dictation",
        version='version',
        description='desc',
        executables=executables
    )
