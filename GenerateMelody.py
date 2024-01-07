import random
import music21

def generate_random_melody(generation_mode, key, scale_degrees, intervals_list, length, tempo, time_signature, min_octave, max_octave):
    # Create a music21 stream for the melody
    melody_stream = music21.stream.Stream()

    possible_keys = ["C", "G", "D", "A", "E", "B", "F#", "C#", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]
    is_chromatic = False

    if key == "Random":
        key = random.choice(possible_keys)

    if key == "Chromatic":
        key = "C"    
        is_chromatic = True
        
    # Function to safely convert string to integer
    def safe_str_to_int(s, default=0):
        try:
            return int(s)
        except ValueError:
            return default

    def transpose_and_check(pitch, interval_name, direction):
        try:
            interval_obj = music21.interval.Interval(interval_name)
            interval_semitones = direction * interval_obj.semitones
            next_interval = music21.interval.Interval(interval_semitones)
            return pitch.transpose(next_interval)
        except Exception as e:
            print(f"Error in transposition: {e}")
            return pitch  # Return the original pitch in case of error

    def get_key_pitches(key_name, min_octave, max_octave):
        key = music21.key.Key(key_name)
        scale = key.getScale()
        key_pitches = []

        for octave in range(min_octave, max_octave + 1):
            for pitch_name in scale.getPitches():
                pitch = music21.pitch.Pitch(pitch_name.name)
                pitch.octave = octave
                key_pitches.append(pitch.nameWithOctave)

        return key_pitches

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

    # Set the time signature
    melody_stream.append(music21.meter.TimeSignature(time_signature))

    key_str = key
    key = music21.key.Key(key)
    key_signature = key.asKey()
    melody_stream.append(key_signature)

    # Generate the melody
    if generation_mode == "Interval":
        # Generate melody based on intervals
        current_pitch = music21.pitch.Pitch("C4")

        # Convert min and max octave values to integers
        min_octave = safe_str_to_int(min_octave, default=3)  # default to 3 if conversion fails
        max_octave = safe_str_to_int(max_octave, default=5)  # default to 5 if conversion fails

        allowedIntervals = []

        for interval in intervals_list:
            if intervals_list[interval] == True:
                allowedIntervals.append(interval)

        print("\nGeneration Notes\n-----------\n")

        for _ in range(length):
            melody_stream.append(music21.note.Note(current_pitch))

            if is_chromatic:
                next_interval_name = random.choice(allowedIntervals)
                direction = random.choice([-1, 1])
                new_pitch = transpose_and_check(current_pitch, next_interval_name, direction)
            else:
                key_pitches = get_key_pitches(key_str, min_octave, max_octave)
                valid_intervals = []

                for interval in allowedIntervals:
                    interval_obj = music21.interval.Interval(interval)
                    test_pitch = current_pitch.transpose(interval_obj)
                    if test_pitch.nameWithOctave in key_pitches:
                        valid_intervals.append(interval)

                if not valid_intervals:
                    new_pitch = key.tonic
                else:
                    next_interval_name = random.choice(valid_intervals)
                    direction = random.choice([-1, 1])
                    new_pitch = transpose_and_check(current_pitch, next_interval_name, direction)

            if isinstance(new_pitch, music21.pitch.Pitch) and new_pitch.octave is not None:
                # Check octave range
                if not (min_octave <= new_pitch.octave <= max_octave):
                    new_pitch = transpose_and_check(current_pitch, next_interval_name, -direction)
            
            current_pitch = new_pitch

    elif generation_mode == "Scale":
        # Generate melody based on intervals
        note_pitch = music21.pitch.Pitch("C4")

        # Convert min and max octave values to integers
        min_octave = safe_str_to_int(min_octave, default=3)  # default to 3 if conversion fails
        max_octave = safe_str_to_int(max_octave, default=5)  # default to 5 if conversion fails

        allowedDegrees = []

        for degree in scale_degrees:
            if scale_degrees[degree] == True:
                allowedDegrees.append(degree)

        for degree in allowedDegrees:
            note_pitch = key.pitchFromDegree(scale_note_to_int[degree])
            print(note_pitch)

        # Generate melody based on scale degrees
        for _ in range(length):
            scale_degree_name = random.choice(allowedDegrees)
            note_pitch = key.pitchFromDegree(scale_note_to_int[scale_degree_name])

            # Randomly choose to go up or down
            direction = random.choice([-1, 1])

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
