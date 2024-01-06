import random
import music21  # Make sure to install the music21 library

def generate_random_melody(scale_type, key, allowed_intervals, length, tempo, time_signature):
    # Create a music21 stream for the melody
    melody_stream = music21.stream.Stream()

    # Define the chosen scale based on the scale_type and key
    if scale_type == "Major":
        chosen_scale = music21.scale.MajorScale(key)
    elif scale_type == "Minor":
        chosen_scale = music21.scale.NaturalMinorScale(key)
    elif scale_type == "Natural Minor":
        chosen_scale = music21.scale.NaturalMinorScale(key)
    elif scale_type == "Harmonic Minor":
        chosen_scale = music21.scale.HarmonicMinorScale(key)
    elif scale_type == "Chromatic":
        chosen_scale = music21.scale.ChromaticScale(key)
    else:
        # Default to Major scale if scale_type is not recognized
        chosen_scale = music21.scale.MajorScale(key)

    # Set the time signature
    melody_stream.append(music21.meter.TimeSignature(time_signature))

    # Generate the melody
    current_note = random.choice(chosen_scale.getPitches(key, key.octave, key.octave + 1))
    for _ in range(length):
        melody_stream.append(music21.note.Note(current_note))
        # Randomly select the next interval
        next_interval = random.choice(allowed_intervals)
        # Calculate the next note based on the interval
        next_note_index = chosen_scale.getScale().index(current_note.name)
        next_note_index += music21.interval.Interval(next_interval).semitones
        current_note = chosen_scale.getScale()[next_note_index]

    # Add a tempo mark to the melody
    melody_stream.append(music21.tempo.MetronomeMark("q = " + str(tempo)))

    return melody_stream
