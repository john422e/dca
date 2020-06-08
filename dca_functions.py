from random import choice
from numpy.random import choice as npchoice
import abjad

def make_random_pitch_sequence(offset, length, pitch_range_slider):
    pitches = list(range(pitch_range_slider.value[0], pitch_range_slider.value[1]+1))
    sequence = []
    for note in range(length.value):
        note = choice(pitches)
        sequence.append(note + offset)
    return sequence

# Statistical Feedback functions

def get_probs(weights, counts):
    probs = []
    total = 0
    for i in range(len(weights)):
        total += weights[i] * growth_function(counts[i])

    for i in range(len(weights)):
        prob = weights[i] * growth_function(counts[i]) / total
        probs.append(prob)

    return probs

def growth_function(n): # Tenney's convex growth function
    return 2**n

def make_dca_spaced_pitch_sequence(offset, weights_option, length, pitch_range_slider, show_data=False, print_ly=False):
    pitches = list(range(pitch_range_slider.value[0], pitch_range_slider.value[1]+1))
    counts = [0] * len(pitches)

    weights = []

    if weights_option.value=='equal':
        weights = [1] * len(pitches) # how much to weigh each element's probability

    elif weights_option.value=='favor lower':
        for i, pitch in enumerate(pitches):
            weight = (i+1) ** 2
            weights.append(weight)
        weights.reverse()

    elif weights_option.value=='favor center':
        middle = len(pitches) / 2
        for i in range(1, int(middle)+1):
            weights.append(i**2)
        if middle.is_integer() == False:
            weights.append((middle+0.5) ** 2)
        for i in range(int(middle), 0, -1):
            weights.append(i**2)

    elif weights_option.value=='favor upper':
        for i, pitch in enumerate(pitches):
            weight = (i+1) ** 2
            weights.append(weight)

    print(weights)

    pcprobs = get_probs(weights, counts)

    sequence = []

    note_count = 1
    for note in range(length.value):
        # random choice according to probability
        note_choice = npchoice(pitches, p=pcprobs)
        element = pitches.index(note_choice)
        note = note_choice + offset

        # add note to sequence
        sequence.append(note)

        # now update counts
        for i, pitch in enumerate(pitches):
            if i == element:
                counts[i] = 0
            else:
                counts[i] += 1

        # recalculate pcprobs
        pcprobs = get_probs(weights, counts)

        if show_data:
            print("Note ", note_count, ":")
            print("Random index choice:", note_choice)
            print("Current counts:", counts)
            print("Current probabilities:", pcprobs, "\n")

        note_count += 1

    if print_ly:
        output_ly(sequence)

    return sequence

def output_ly(sequence):
    notes = []
    for pitch in sequence:
        duration = abjad.Duration(1, 4)
        note = abjad.Note(pitch, duration)
        notes.append(note)

    staff = abjad.Staff(notes)
    abjad.show(staff, pdf_file_path="dca_ps.pdf")
