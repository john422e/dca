from random import choice, randrange
from IPython.display import Image, display
from numpy.random import choice as npchoice
import abjad
import convert_image

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

def make_dca_spaced_pitch_sequence(offset, weights_option, length, pitch_range_slider, pitches=None, show_data=False, print_ly=False):
    if not pitches:
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

    if show_data:
        print("Weights:", weights, "\n")

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
        output_sequence_ly(sequence)

    return sequence

def output_sequence_ly(sequence):
    notes = []
    for pitch in sequence:
        duration = abjad.Duration(1, 4)
        note = abjad.Note(pitch, duration)
        notes.append(note)

    staff = abjad.Staff(notes)
    score = abjad.Score([staff])
    lilypond_file = abjad.LilyPondFile.new(score, global_staff_size=20,
                                        default_paper_size=('letter', 'portrait'))
    lilypond_file.header_block.title = abjad.Markup("Dissonant Counterpoint Pitch Sequence")
    #abjad.show(staff, pdf_file_path="dca_ps.pdf")

    pdf_file = "imgs/dca_ps.pdf"
    png_file = "imgs/dca_ps.png"
    abjad.persist(score).as_pdf(pdf_file)
    convert_image.get_abjad_output(pdf_file, png_file)
    display(Image(png_file))

def make_clang(offset, deviation, weights_option, undeviated_length, length, pitch_range_slider, pitches=None, show_data=False, print_ly=False):
    # length = average length +/- deviation range
    deviated_length = undeviated_length + randrange(deviation*-1, deviation)
    length.value = int(deviated_length)
    sequence = make_dca_spaced_pitch_sequence(offset, weights_option, length, pitch_range_slider, pitches=pitches, show_data=show_data, print_ly=print_ly)
    sequence.append("rest") # end every clang with a rest
    return sequence

def output_clangs_ly(clangs):
    notes = []
    for clang in clangs:
        for pitch in clang:
            if pitch == "rest":
                notes.append(abjad.Rest('r8'))
            else:
                duration = abjad.Duration(1, 8)
                note = abjad.Note(pitch, duration)
                notes.append(note)

    staff = abjad.Staff(notes)

    score = abjad.Score([staff])
    lilypond_file = abjad.LilyPondFile.new(score, global_staff_size=20,
                                        default_paper_size=('letter', 'portrait'))
    lilypond_file.header_block.title = abjad.Markup("Dissonant Counterpoint Example Piece")
    #abjad.show(staff, pdf_file_path="dca_ps.pdf")

    pdf_file = "imgs/dca_piece.pdf"
    png_file = "imgs/dca_piece.png"
    png_stem = png_file[:-4]
    abjad.persist(score).as_pdf(pdf_file)
    total_pngs = convert_image.get_abjad_output(pdf_file, png_file, multiple_pages=True)
    for i in range(total_pngs):
        png_file = png_stem + str(i) + ".png"
        print(png_file)
        display(Image(png_file))
