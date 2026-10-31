import argparse
import random

SHARPS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLATS = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

BASE_NOTES = [4, 9, 2, 7, 11, 4]  # E A D G B E as pitch classes
FOURTH = 5                        # the spacing the skeleton's windows assume

# grouping -> (min length, max length). Ceiling is 5 * grouping - 1 (4, 9, 14).
LENGTH_RANGES = {1: (2, 4), 2: (2, 8), 3: (3, 12)}

NUM_FRETS = 21
MAX_FRET = NUM_FRETS - 4          # highest starting fret
STRING_NAMES = ["E", "A", "D", "g", "b", "e"]  # low to high, matching BASE_NOTES


def ceiling_for(grouping):
    return 5 * grouping - 1


def unearth_skeleton(length, ceiling):
    """Sorted unique offsets that always include 0 and stay within the ceiling."""
    if length < 2:
        raise ValueError("Length must be at least 2.")
    if length - 1 > ceiling:
        raise ValueError("Length can be at most ceiling + 1.")
    return [0] + sorted(random.sample(range(1, ceiling + 1), k=length - 1))


def has_chromatic_run(skeleton, run=4):
    """True if `run` consecutive semitones occur, e.g. [0, 1, 2, 3]."""
    return any(
        skeleton[i + run - 1] - skeleton[i] == run - 1
        for i in range(len(skeleton) - run + 1)
    )


def has_cluster_at_both_ends(skeleton, ceiling):
    """Starts with 0, 1 and ends with ceiling-2, ceiling-1, ceiling."""
    return skeleton[1] == 1 and skeleton[-3:] == [ceiling - 2, ceiling - 1, ceiling]


def form_skeleton(length, grouping, start_fret):
    """Generate skeletons until one passes curation."""
    ceiling = ceiling_for(grouping)
    while True:
        skeleton = unearth_skeleton(length, ceiling)
        frets = place_skeleton(skeleton, grouping, start_fret)
        if (
            all(frets)  # no empty strings
            and is_playable(frets)
            and not has_chromatic_run(skeleton)
            and not has_cluster_at_both_ends(skeleton, ceiling)
        ):
            return skeleton


def place_skeleton(skeleton, grouping, start_fret):
    """Fret numbers for each string (low to high), as six lists.

    Each skeleton note is played on one string of its group: offsets 0-4 on the
    first, 5-9 on the second, 10-14 on the third. A skeleton no longer than the
    grouping puts one note on each string. The same shape is used on every
    group, so the upper strings of the G-B-e group sound a semitone lower,
    as in the original.
    """
    frets = []
    for string in range(len(BASE_NOTES)):
        k = string % grouping
        frets.append(
            [
                start_fret + offset - FOURTH * k
                for i, offset in enumerate(skeleton)
                if (i if len(skeleton) <= grouping else offset // FOURTH) == k
            ]
        )
    return frets


def is_playable(frets_by_string):
    """Frets on the neck, and fretted notes within a four-fret stretch."""
    frets = [f for string in frets_by_string for f in string]
    fretted = [f for f in frets if f > 0]
    return (
        min(frets) >= 0
        and max(frets) <= NUM_FRETS
        and (not fretted or max(fretted) - min(fretted) <= 4)
    )


def tab_print(frets_by_string, pad=2):
    lines = [
        f"{name:<{pad}}| {'--'.join(map(str, frets))}"
        for name, frets in zip(STRING_NAMES, frets_by_string)
    ]
    return "\n".join(reversed(lines))  # high string on top


def int_or_random(value, name):
    """None means random."""
    if value in ("r", ""):
        return None
    if value.isdigit():
        return int(value)
    raise SystemExit(f"{name}: a number or 'r' for random.")


def choose_settings(grouping, length):
    """Resolve random (None) choices into a valid (grouping, length) pair."""
    if grouping is None:
        options = [
            g
            for g, (lo, hi) in LENGTH_RANGES.items()
            if length is None or lo <= length <= hi
        ]
        if not options:
            raise SystemExit("Length must be between 2 and 12.")
        grouping = random.choice(options)
    elif grouping not in LENGTH_RANGES:
        raise SystemExit("Grouping: 1 to 3 or 'r' for random.")

    lo, hi = LENGTH_RANGES[grouping]
    if length is None:
        length = random.randint(lo, hi)
    elif not lo <= length <= hi:
        raise SystemExit(
            f"Length for a grouping of {grouping} must be between {lo} and {hi}."
        )
    return grouping, length


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--fret", default="r",
        help="Starting fret: a number or 'r' for random (default). "
        f"Highest allowed fret is {MAX_FRET}.",
    )
    parser.add_argument(
        "-l", "--length", default="r",
        help="Skeleton length: a number or 'r' for random (default). "
        "Allowed range depends on grouping: 2-4, 2-8, 3-12 for groupings 1, 2, 3.",
    )
    parser.add_argument(
        "-g", "--grouping", default="r",
        help="Grouping size, 1 to 3, or 'r' for random (default).",
    )
    parser.add_argument(
        "-#", "--shflat", choices=["#", "b"], default="#",
        help="Show sharps ('#') or flats ('b'). Defaults to sharps.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    grouping, length = choose_settings(
        int_or_random(args.grouping, "Grouping"),
        int_or_random(args.length, "Length"),
    )
    start_fret = int_or_random(args.fret, "Fret")
    if start_fret is None:
        start_fret = random.randint(0, MAX_FRET)
    elif start_fret > MAX_FRET:
        raise SystemExit(f"Starting fret too high: the maximum is {MAX_FRET}.")


    skeleton = form_skeleton(length, grouping, start_fret)
    frets = place_skeleton(skeleton, grouping, start_fret)
    names = SHARPS if args.shflat == "#" else FLATS
    skel_notes = [
        names[(open_string + fret) % 12]
        for open_string, string_frets in zip(BASE_NOTES, frets)
        for fret in string_frets
    ]

    print(
        f"\n{tab_print(frets)}\n"
        f"\nSkeleton:\n{', '.join(map(str, skeleton))}"
        f"\n\nNotes:\n{', '.join(skel_notes)}"
        f"\n\nStarting fret: {start_fret}"
        f"\nString grouping: {grouping}"
    )


if __name__ == "__main__":
    main()