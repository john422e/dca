from random import choice, randrange
from numpy.random import choice as npchoice
import abjad

pitches = range(12)
counts = [0] * 12 # counts since that index of pitches was chosen
pcprob = [1] * 12
weights = [1] * 12

offset = 0 #int(input("Pitch Offset: ")) # 0 = C4
length = 100 # number of notes, for now

# growth function which acts on count values to update the relative selection probabilities
# i.e. growth_function(counts[x]) = selection probability
# weight on each element = w[i]

""""
for timestep:
    -probabilities:
    weight[i] * function[count[i]] / w*f sum of all elements
    -randomly choose j from set
    -update counts
    -store j in output list
"""

def growth_function(n):
    return 2**n

def get_probs(weights, counts):
    probs = []
    total = 0
    for i in range(len(weights)):
        total += weights[i] * growth_function(counts[i])

    for i in range(len(weights)):
        prob = weights[i] * growth_function(counts[i]) / total
        probs.append(prob)

    return probs

def make_random_pitch_sequence(pitches, offset, length):
    sequence = []
    for note in range(length):
        note = random.choice(pitches)
        sequence.append(note + offset)
    return sequence

def make_dca_spaced_pitch_sequence(pitches, offset, weights, length, show_data=False):
    counts = [0] * len(pitches)
    pcprobs = get_probs(weights, counts)

    sequence = []
    for note in range(length):
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
            print("\nRandom index choice:", note_choice)
            print("Current counts:", counts)
            print("Current probabilities:", pcprobs)

    return sequence



#weights = range(1, 13)

sequence = make_dca_spaced_pitch_sequence(pitches, offset, weights, length)

for pitch in pitches:
    print(sequence.count(pitch))

print()
print(sequence)

def output_ly(sequence):
    notes = []
    for pitch in sequence:
        duration = abjad.Duration(1, 4)
        note = abjad.Note(pitch, duration)
        notes.append(note)

    staff = abjad.Staff(notes)
    abjad.show(staff)

#output_ly(sequence)


def make_clang(pitches, weights, length, deviation, offset=0):
    # length = average length +/- deviation range
    length = length + randrange(deviation*-1, deviation)
    sequence = make_dca_spaced_pitch_sequence(pitches, offset, weights, length)
    sequence.append("rest") # end every clang with a rest
    return sequence

# build clangs
total_clangs = 72

# weight by proximity to pitch center
increasing = [ 1 * i for i in range(1, 7) ]
decreasing = list(reversed(increasing))
weights = increasing + decreasing

peak = int(total_clangs * (2/3))

length = 5
length_deviation = int(length * 0.5)

offset = -12
pitch_center = 6
clangs = []

for clang in range(total_clangs):
    pitches = [*range(int(pitch_center) - 6, int(pitch_center+6))]
    #print(pitches)

    sequence = make_clang(pitches, weights, length, length_deviation, offset=offset)
    clangs.append(sequence)

    if clang < peak:
        pitch_center += 0.6
        length += 1
    else:
        pitch_center -= 1.25
        length -= 2
    length_deviation = int(length * 0.5)

for clang in clangs:
    print(clang)

def output_clangs(clangs):
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
    abjad.show(staff)
    abjad.play(staff)

output_clangs(clangs)
