import random
import music21

def generate_random_melody(generation_mode, scale_type, key, scale_degrees, intervals_list, length, tempo, time_signature, min_octave, max_octave):
    # Create a music21 stream for the melody
    melody_stream = music21.stream.Stream()

    # Function to safely convert string to integer
    def safe_str_to_int(s, default=0):
        try:
            return int(s)
        except ValueError:
            return default

    # Define the chosen scale based on the scale_type and key
    scale_classes = {
        "Major": music21.scale.MajorScale,
        "Minor": music21.scale.MinorScale,
        "Melodic Minor": music21.scale.MelodicMinorScale,
        "Harmonic Minor": music21.scale.HarmonicMinorScale,
        "Chromatic": music21.scale.ChromaticScale
    }

    # Define the dictionary for scale note mapping
    scale_note_to_int = {
        "Tonic": 1,
        "Supertonic": 2,
        "Mediant": 3,
        "Subdominant": 4,
        "Dominant": 5,
        "Submediant": 6,
        "Leading Tone": 7
    }

    # Generate the melody
    if generation_mode == "Interval":
        chosen_scale = music21.scale.ChromaticScale
    elif generation_mode == "Scale":
        chosen_scale = scale_classes.get(scale_type, music21.scale.MajorScale)(key)

    # Set the time signature
    melody_stream.append(music21.meter.TimeSignature(time_signature))

    # Set the key signature
    key = music21.key.Key(key)
    key_signature = key.asKey()
    melody_stream.append(key_signature)

    # Set the time signature
    melody_stream.append(music21.meter.TimeSignature(time_signature))

    # Generate the melody
    if generation_mode == "Interval":
        # Generate melody based on intervals
        current_pitch = music21.pitch.Pitch("C4")

        # Convert min and max octave values to integers
        min_octave = safe_str_to_int(min_octave, default=3)  # default to 3 if conversion fails
        max_octave = safe_str_to_int(max_octave, default=5)  # default to 5 if conversion fails

        allowedIntervals = []

        for interval in intervals_list:
            print(f"I: {intervals_list[interval]}")
            if intervals_list[interval] == True:
                allowedIntervals.append(interval)

        for _ in range(length):
            melody_stream.append(music21.note.Note(current_pitch))

            # Choose a random interval from the allowed ones
            next_interval_name = random.choice(allowedIntervals)

            # Randomly choose to go up or down
            direction = random.choice([-1, 1])

            # Function to transpose and check octave range
            def transpose_and_check(pitch, interval_name, direction):
                interval_obj = music21.interval.Interval(interval_name)
                interval_semitones = direction * interval_obj.semitones
                next_interval = music21.interval.Interval(interval_semitones)
                new_pitch = pitch.transpose(next_interval)
                return new_pitch

            # Transpose the current pitch by the chosen interval and check the octave
            new_pitch = transpose_and_check(current_pitch, next_interval_name, direction)

            # If the new note is outside the desired octave range, flip the interval direction
            if not (min_octave <= new_pitch.octave <= max_octave):
                new_pitch = transpose_and_check(current_pitch, next_interval_name, -direction)

            # Update the current pitch and append the note to the melody stream
            current_pitch = new_pitch

    elif generation_mode == "Scale":
        # Generate melody based on intervals
        note_pitch = music21.pitch.Pitch("C4")

        # Convert min and max octave values to integers
        min_octave = safe_str_to_int(min_octave, default=3)  # default to 3 if conversion fails
        max_octave = safe_str_to_int(max_octave, default=5)  # default to 5 if conversion fails

        allowedDegrees = []

        for degree in scale_degrees:
            print(f"I: {scale_degrees[degree]}")
            if scale_degrees[degree] == True:
                allowedDegrees.append(degree)


        # Generate melody based on scale degrees
        for _ in range(length):
            scale_degree_name = random.choice(allowedDegrees)
            note_pitch = chosen_scale.pitchFromDegree(scale_note_to_int[scale_degree_name])
            
            # Randomly choose to go up or down
            direction = random.choice([-1, 1])

            # Function to transpose and check octave range
            def transpose_and_check(pitch, interval_name, direction):
                interval_obj = music21.interval.Interval(interval_name)
                interval_semitones = direction * interval_obj.semitones
                next_interval = music21.interval.Interval(interval_semitones)
                new_pitch = pitch.transpose(next_interval)
                return new_pitch

            # Transpose the current pitch by the chosen interval and check the octave
            new_pitch = transpose_and_check(note_pitch, "P8", direction)

            # If the new note is outside the desired octave range, flip the interval direction
            if not (min_octave <= new_pitch.octave <= max_octave):
                new_pitch = transpose_and_check(note_pitch, "P8", -direction)

            # Update the current pitch and append the note to the melody stream
            note_pitch = new_pitch
            melody_stream.append(music21.note.Note(note_pitch))


    # Add a tempo mark to the melody
    # Create a metronome mark for the desired tempo
    metronome_mark = music21.tempo.MetronomeMark(number=tempo)
    melody_stream.insert(0, metronome_mark)
    
    return melody_stream
