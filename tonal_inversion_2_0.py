import re
import shutil

notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


scales = {
    # --- Pentatonic and other small scales ---
    "major pentatonic": [0, 2, 4, 7, 9],
    "minor pentatonic": [0, 3, 5, 7, 10],
    "dominant pentatonic": [0, 2, 4, 7, 10],
    "minor six pentatonic": [0, 3, 5, 7, 9],
    "egyptian": [0, 2, 5, 7, 10],
    "man gong": [0, 3, 5, 8, 10],
    "hirajoshi": [0, 2, 3, 7, 8],
    "in sen": [0, 1, 5, 7, 10],
    "iwato": [0, 1, 5, 6, 10],
    "yo": [0, 2, 5, 7, 9],
    "kumoi": [0, 2, 3, 7, 9],
    "ryukyu": [0, 4, 5, 7, 11],
    "blues": [0, 3, 5, 6, 7, 10],
    "major blues": [0, 2, 3, 4, 7, 9],

    # --- Symmetric / hexatonic ---
    "whole tone": [0, 2, 4, 6, 8, 10],
    "augmented": [0, 3, 4, 7, 8, 11],
    "tritone": [0, 1, 4, 6, 7, 10],
    "two semitone tritone": [0, 1, 2, 6, 7, 8],
    "prometheus": [0, 2, 4, 6, 9, 10],
    "prometheus neapolitan": [0, 1, 4, 6, 9, 10],

    # --- Harmonic minor and its modes ---
    "harmonic minor": [0, 2, 3, 5, 7, 8, 11],
    "locrian natural 6": [0, 1, 3, 5, 6, 9, 10],
    "ionian #5": [0, 2, 4, 5, 8, 9, 11],
    "dorian #4": [0, 2, 3, 6, 7, 9, 10],
    "phrygian dominant": [0, 1, 4, 5, 7, 8, 10],
    "lydian #2": [0, 3, 4, 6, 7, 9, 11],
    "ultralocrian": [0, 1, 3, 4, 6, 8, 9],

    # --- Melodic minor (ascending) and its modes ---
    "melodic minor": [0, 2, 3, 5, 7, 9, 11],
    "dorian b2": [0, 1, 3, 5, 7, 9, 10],
    "lydian augmented": [0, 2, 4, 6, 8, 9, 11],
    "lydian dominant": [0, 2, 4, 6, 7, 9, 10],
    "mixolydian b6": [0, 2, 4, 5, 7, 8, 10],
    "locrian #2": [0, 2, 3, 5, 6, 8, 10],
    "altered": [0, 1, 3, 4, 6, 8, 10],

    # --- Other heptatonic scales ---
    "harmonic major": [0, 2, 4, 5, 7, 8, 11],
    "double harmonic major": [0, 1, 4, 5, 7, 8, 11],
    "hungarian minor": [0, 2, 3, 6, 7, 8, 11],
    "hungarian major": [0, 3, 4, 6, 7, 9, 10],
    "neapolitan minor": [0, 1, 3, 5, 7, 8, 11],
    "neapolitan major": [0, 1, 3, 5, 7, 9, 11],
    "persian": [0, 1, 4, 5, 6, 8, 11],
    "enigmatic": [0, 1, 4, 6, 8, 10, 11],
    "leading whole tone": [0, 2, 4, 6, 8, 10, 11],
    "major locrian": [0, 2, 4, 5, 6, 8, 10],
    "lydian minor": [0, 2, 4, 6, 7, 8, 10],
    "lydian diminished": [0, 2, 3, 6, 7, 9, 11],

    # --- Octatonic and bebop ---
    "whole half diminished": [0, 2, 3, 5, 6, 8, 9, 11],
    "half whole diminished": [0, 1, 3, 4, 6, 7, 9, 10],
    "bebop dominant": [0, 2, 4, 5, 7, 9, 10, 11],
    "bebop major": [0, 2, 4, 5, 7, 8, 9, 11],
    "bebop dorian": [0, 2, 3, 4, 5, 7, 9, 10],

    # --- Messiaen modes of limited transposition (1 = whole tone, 2 = diminished) ---
    "messiaen 3": [0, 2, 3, 4, 6, 7, 8, 10, 11],
    "messiaen 4": [0, 1, 2, 5, 6, 7, 8, 11],
    "messiaen 5": [0, 1, 5, 6, 7, 11],
    "messiaen 6": [0, 2, 4, 5, 6, 8, 10, 11],
    "messiaen 7": [0, 1, 2, 3, 5, 6, 7, 8, 9, 11],

    # --- Yours, kept as you had them ---
    "algerian": [0, 2, 3, 6, 7, 8, 11, 12, 14, 15, 17],
    "chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}


aliases = {
    "aeolian": "minor",
    "ionian": "major",
    "acoustic": "lydian dominant",
    "acoustic scale": "lydian dominant",
    "overtone": "lydian dominant",
    "super locrian": "altered",
    "ukrainian dorian": "dorian #4",
    "romanian minor": "dorian #4",
    "freygish": "phrygian dominant",
    "hindu": "mixolydian b6",
    "aeolian dominant": "mixolydian b6",
    "half diminished": "locrian #2",
    "aeolian b5": "locrian #2",
    "phrygian natural 6": "dorian b2",
    "double harmonic": "double harmonic major",
    "byzantine": "double harmonic major",
    "gypsy minor": "hungarian minor",
    "double harmonic minor": "hungarian minor",
    "dominant diminished": "half whole diminished",
}


LETTER_ORDER = "CDEFGAB"
MAJOR = [0, 2, 4, 5, 7, 9, 11]
mode_names = ["major", "dorian", "phrygian", "lydian", "mixolydian", "minor", "locrian"]


def mode_offsets(k):
    """Offsets of the k-th mode of the major scale, rooted on 0."""
    rotated = MAJOR[k:] + MAJOR[:k]
    return [(o - rotated[0]) % 12 for o in rotated]


scales.update({name: mode_offsets(k) for k, name in enumerate(mode_names)})


NOTE = r"[A-G](?:[#b])?"
CHORD_RE = re.compile(rf"{NOTE}(?:\s*,?\s*{NOTE})*")
LETTERS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
ACCIDENTALS = {"": 0, "#": 1, "b": -1}


def pc(note):
    """Pitch class 0-11, so A# == Bb and E# == F."""
    return (LETTERS[note[0]] + ACCIDENTALS[note[1:]]) % 12


def ask_note(prompt):
    while True:
        raw = input(prompt).strip()
        raw = raw[:1].upper() + raw[1:]  # 'bb' -> 'Bb'
        if re.fullmatch(NOTE, raw):
            return raw
        print("ValueError: Please enter exactly one note, e.g. C, F#, Bb.")


def print_columns(title, names):
    names = sorted(names)
    width = max(len(n) for n in names) + 3
    term_width = shutil.get_terminal_size().columns
    n_cols = max(1, term_width // width)
    n_rows = -(-len(names) // n_cols)  # ceiling division
    print(f"\n{title}")
    for r in range(n_rows):
        print("".join(n.ljust(width) for n in names[r::n_rows]).rstrip())
    print()


def print_scale_list():
    print_columns("Modes", mode_names)
    print_columns("Scales", [s for s in scales if s not in mode_names])
    print_columns("Alternate names", [f"{a} -> {t}" for a, t in aliases.items()])


def ask_scale():
    while True:
        name = " ".join(input("Scale/mode: ").lower().replace("-", " ").split())
        if name in ("list", "?"):
            print_scale_list()
            continue
        name = aliases.get(name, name)
        if name in scales:
            return name
        print("ValueError: Unknown scale. Type 'list' to see the options.")


def spell(root, offsets):
    """One letter per degree. Returns None if it needs a double sharp/flat."""
    if len(offsets) != 7:
        return None
    start = LETTER_ORDER.index(root[0])
    out = []
    for i, off in enumerate(offsets):
        letter = LETTER_ORDER[(start + i) % 7]
        diff = ((pc(root) + off) - LETTERS[letter] + 6) % 12 - 6
        if abs(diff) > 1:
            return None
        out.append(letter + {-1: "b", 0: "", 1: "#"}[diff])
    return out


def alt_spellings(root):
    """Enharmonic spellings of the root, e.g. G# -> Ab."""
    return [
        l + a
        for l in LETTER_ORDER
        for a in ("", "#", "b")
        if pc(l + a) == pc(root) and l + a != root
    ]


def build_tonality(root, scale):
    offsets = sorted({i % 12 for i in scales[scale]})  # dedupe + sort
    for r in [root] + alt_spellings(root):
        spelled = spell(r, offsets)
        if spelled:
            return spelled
    return [notes[(pc(root) + i) % 12] for i in offsets]  # sharps fallback


def ask_axis(tonality):
    pcs = [pc(n) for n in tonality]
    while True:
        axis = ask_note("Axis: ")
        if pc(axis) in pcs:
            return axis
        print(f"ValueError: Axis must be in the scale ({', '.join(tonality)}).")


def ask_chord(tonality):
    pcs = [pc(n) for n in tonality]
    while True:
        raw = input("Chord/notes: ").strip()
        if not CHORD_RE.fullmatch(raw):
            print("ValueError: Invalid notes or must capitalize notes.")
            continue
        chord = re.findall(NOTE, raw)
        outside = [n for n in chord if pc(n) not in pcs]
        if outside:
            print(f"ValueError: Not in the scale: {', '.join(outside)}")
            continue
        return chord


def tonal_inversion(tonality, axis, chord):
    pcs = [pc(n) for n in tonality]
    i = pcs.index(pc(axis))
    rotated = tonality[i:] + tonality[:i]
    rotated_pcs = pcs[i:] + pcs[:i]
    # degree k above the axis maps to degree k below it (index -k wraps)
    return [rotated[-rotated_pcs.index(pc(n))] for n in chord]


def main():
    root = ask_note("Root: ")
    scale = ask_scale()
    tonality = build_tonality(root, scale)
    print(f"Chosen tonality: {', '.join(tonality)}")
    axis = ask_axis(tonality)
    chord = ask_chord(tonality)
    print(", ".join(tonal_inversion(tonality, axis, chord)))


if __name__ == "__main__":
    main()