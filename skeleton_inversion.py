import re

import skeletons_rehash as sk
import tonal_inversion_2_0 as ti

POS = r"[EeAaDdGgBb]\d{1,2}"
ITEM = rf"(?:{POS}|{ti.NOTE})"
ITEM_LIST = re.compile(rf"{ITEM}(?:\s*,?\s*{ITEM})*")
TOKEN = re.compile(rf"({POS})|({ti.NOTE})")
POS_RE = re.compile(r"([EeAaDdGgBb])(\d{1,2})")

# 'E' is the low string and 'e' the high one. The other letters work in either case.
STRING_LOOKUP = {name: i for i, name in enumerate(sk.STRING_NAMES)}
for i, name in enumerate(sk.STRING_NAMES):
    if name not in "Ee":
        STRING_LOOKUP[name.upper()] = i
        STRING_LOOKUP[name.lower()] = i


def label(position):
    string, fret = position
    return f"{sk.STRING_NAMES[string]}{fret}"


def parse_position(text):
    """'A6' -> (1, 6). None if the text isn't a position."""
    m = POS_RE.fullmatch(text)
    return (STRING_LOOKUP[m.group(1)], int(m.group(2))) if m else None


def choose_position(note, candidates, positions):
    """Several positions share this note: ask which one is meant."""
    options = [positions[i] for i in candidates]
    menu = "  ".join(f"{n}) {label(p)}" for n, p in enumerate(options, 1))
    while True:
        answer = input(f"{note} is at {menu}. Which one? ").strip()
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return candidates[int(answer) - 1]
        position = parse_position(answer)
        if position in options:
            return candidates[options.index(position)]
        print("ValueError: Pick a number from the list or one of those positions.")


def ask_notes(prompt, positions, only_one=False):
    """Ask for notes by name (F#, Bb), or by position (E4, g6) to skip the
    follow-up question. Returns indices into `positions`."""
    pcs = [(sk.BASE_NOTES[s] + f) % 12 for s, f in positions]
    index = {pos: i for i, pos in enumerate(positions)}
    while True:
        raw = input(prompt).strip()
        if not ITEM_LIST.fullmatch(raw):
            print("ValueError: Enter notes (F#, Bb) or neck positions (E4, g6).")
            continue
        items = [pos or note for pos, note in TOKEN.findall(raw)]
        if only_one and len(items) != 1:
            print("ValueError: Exactly one note, please.")
            continue

        chosen = []
        for item in items:
            position = parse_position(item)
            if position is not None:
                if position not in index:
                    print(f"ValueError: {item} is not on the tab.")
                    break
                chosen.append(index[position])
            else:
                candidates = [i for i, p in enumerate(pcs) if p == ti.pc(item)]
                if not candidates:
                    print(f"ValueError: {item} is not on the tab.")
                    break
                if len(candidates) == 1:
                    chosen.append(candidates[0])
                else:
                    chosen.append(choose_position(item, candidates, positions))
        else:
            return chosen


def invert_indices(n, axis, chord):
    """Mirror positions about the axis in a cyclic sequence of n positions."""
    return [(2 * axis - k) % n for k in chord]


def frets_for(indices, positions):
    """Per-string fret lists (sorted, no repeats) for the given positions."""
    frets = [[] for _ in sk.BASE_NOTES]
    for i in indices:
        string, fret = positions[i]
        frets[string].append(fret)
    return [sorted(set(f)) for f in frets]


def side_by_side(left, right, gap=6):
    """Two equal-height text blocks, printed next to each other."""
    left, right = left.splitlines(), right.splitlines()
    width = max(len(line) for line in left)
    return "\n".join(f"{l:<{width + gap}}{r}".rstrip() for l, r in zip(left, right))


def main():
    start_fret, grouping, skeleton, frets, skel_notes = sk.build_skeleton(
        sk.parse_args()
    )
    sk.print_skeleton(start_fret, grouping, skeleton, frets, skel_notes)

    # Same order as skel_notes: low string to high, ascending along each string.
    positions = [
        (string, fret)
        for string, string_frets in enumerate(frets)
        for fret in string_frets
    ]

    print()
    axis = ask_notes("Axis: ", positions, only_one=True)[0]
    chord = ask_notes("Chord/notes: ", positions)

    result = invert_indices(len(positions), axis, chord)

    chord_tab = sk.tab_print(frets_for(chord, positions))
    inversion_tab = sk.tab_print(frets_for(result, positions))

    def summary(title, indices):
        notes = ", ".join(skel_notes[i] for i in indices)
        spots = ", ".join(label(positions[i]) for i in indices)
        return f"{title:<12}{notes} ({spots})"

    print(
        f"\n{side_by_side(f'Chord\n{chord_tab}', f'Inversion\n{inversion_tab}')}"
        f"\n\n{summary('Chord:', chord)}"
        f"\n{summary('Inversion:', result)}"
    )


if __name__ == "__main__":
    main()