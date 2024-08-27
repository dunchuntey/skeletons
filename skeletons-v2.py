import random
import argparse
import sys


notes = {
    0: ["C"],
    1: ["C#", "Db"],
    2: ["D"],
    3: ["D#", "Eb"],
    4: ["E"],
    5: ["F"],
    6: ["F#", "Gb"],
    7: ["G"],
    8: ["G#", "Ab"],
    9: ["A"],
    10: ["A#", "Bb"],
    11: ["B"],
    12: ["C"],
    13: ["C#", "Db"],
    14: ["D"],
    15: ["D#", "Eb"],
    16: ["E"],
    17: ["F"],
    18: ["F#", "Gb"],
    19: ["G"],
    20: ["G#", "Ab"],
    21: ["A"],
    22: ["A#", "Bb"],
    23: ["B"],
    24: ["C"],
    25: ["C#", "Db"],
    26: ["D"],
    27: ["D#", "Eb"],
    28: ["E"],
    29: ["F"],
    30: ["F#", "Gb"],
    31: ["G"],
    32: ["G#", "Ab"],
    33: ["A"],
    34: ["A#", "Bb"],
    35: ["B"],
    36: ["C"],
}


def main():
    """
    The skeleton comes to life.
    """

    tab_print, cipher, starting_notes, start_fret, string_grouping, skeleton = (
        skeleton_to_fretboard(*form_skeleton(*optional_arguments()[0:3]))
    )

    skel_notes = get_skel_notes(
        cipher, starting_notes, start_fret, string_grouping, optional_arguments()[3]
    )

    print(
        f"\n{tab_print}\n"

        f"\nSkeleton:\n{", ".join(map(str, skeleton))}"

        f"\nNotes:\n{", ".join(skel_notes)}"

        # f"\nStarting fret: {start_fret}"

        # f"\nString grouping: {string_grouping}"
    )


def optional_arguments():
    """Optional command-line skeleton customisation.

    Returns:
        tuple: Values for the form_skeleton() function's start_fret, length, and string_grouping parameters.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f", "--fret",
        help="Starting fret: number or 'r' for random (no argument defaults to random). "
        "Highest allowed fret is 17.",
        default=""
    )

    parser.add_argument(
        "-l",
        "--length",
        help=(
            "Skeleton length: number or 'r' for random (no argument defaults to random). "
            "Minimum and maximum length dictated by string grouping: "
            "2-4, 2-8, and 3-12 for string groupings 1, 2, and 3 respectively."
        ),
        default=""
    )

    parser.add_argument(
        "-g",
        "--grouping",
        help="String grouping size. 1 to 3 or 'r' for random (no argument defaults to random).",
        default=""
    )

    parser.add_argument(
        "-#",
        "--shflat",
        help="'#' or 'b'. Display sharps or flats for letter notation output. Defaults to sharps.",
        default="#")

    args = parser.parse_args()

    if args.fret and args.fret.isdigit():
        args.fret = int(args.fret)
    elif args.fret == "r":
        args.fret = "r"

    if args.length and args.length.isdigit():
        args.length = int(args.length)
    elif args.length == "r":
        args.length = "r"

    if args.grouping and args.grouping.isdigit():
        args.grouping = int(args.grouping)
    elif args.grouping == "r":
        args.grouping = "r"

    if args.shflat in ["#", "b"]:
        args.shflat = args.shflat

    return args.fret, args.length, args.grouping, args.shflat


def form_skeleton(
    start_fret: int | str = "r", length: int | str = "r", string_grouping: int = "r"
):
    """Skeleton generator and gatekeeper. Conformity with curation criteria is checked here.
    If necessary, new skeletons are unearthed (i.e. generated).

    Args:
        start_fret (int | str, optional): Set starting fret for skeletons.
        The instrument's number of frets (-4) determines the maximum allowed fret.
        Defaults to "r" for random.

        length (int | str, optional): Set skeleton length.
        Upper and lower limits depend on string grouping.
        Defaults to "r" for random.

        string_grouping (int, optional): Sets string group size (between 1 and 3). Defaults to 3.

    Raises:
        ValueError: If string_grouping == 1 and length not between 2 and 4.
        ValueError: If string_grouping == 2 and length not between 2 and 8.
        ValueError: If string_grouping == 3 and length not between 3 and 12.
        ValueError: If string_grouping not "r" or between 1 and 3.

    Returns:
        skeleton [list]: Curated skeleton ready for fretboard formatting.
        Represents the raw interval values of the skeleton.

        string_grouping [int].

        start_fret [int].
    """

    start_fret = set_start_fret(start_fret)
    if string_grouping in ["r", ""]:
        string_grouping = random.choice(range(1, 4))
    match string_grouping:

        case 1:
            ceiling = 4
            if length in ["r", ""]:
                length = random.choice(range(2, 5))
            elif isinstance(length, str):
                raise ValueError("See help (-h or --help) for rules regarding length.")
            elif 2 <= length <= 4:
                pass
            else:
                # Handling length being set by user in command line and string_grouping being random.
                length = random.choice(range(2, 5))
                print(
                    "\nWARNING! ValueError: Length for a string grouping of 1 can be between 2 and 4"
                )
            while True:
                skeleton = unearth_skeleton(length, ceiling)
                for i in range(3, len(skeleton)):
                    a = skeleton[i - 3]
                    b = skeleton[i - 2]
                    c = skeleton[i - 1]
                    d = skeleton[i]
                    if b == a + 1 and c == b + 1 and d == c + 1:
                        break
                else:
                    return skeleton, string_grouping, start_fret

        case 2:
            ceiling = 9
            if length in ["r", ""]:
                length = random.choice(range(2, 9))
            elif isinstance(length, str):
                raise ValueError("See help (-h or --help) for rules regarding length.")
            elif 2 <= length <= 8:
                pass
            else:
                # Handling length being set by user in command line and string_grouping being random.
                length = random.choice(range(2, 9))
                print(
                    "\nWARNING! ValueError: Length for a string grouping of 2 can be between 2 and 8"
                )
            while True:
                skeleton = unearth_skeleton(length, ceiling)
                # Potentially optional avoidance of severe chromatic slop at start and end of skeleton.
                if skeleton[-3:-1] == [7,8] and skeleton[-1] == 9 and skeleton[1] == 1:
                    continue
                # Ensuring no skeletons over 2 in length have major 6th as second note.
                elif len(skeleton) > 2 and skeleton[1] == 9:
                    continue
                # Ensuring valid skeletons of 2 in length.
                elif (
                    (len(skeleton) == 2 and start_fret == 0 and skeleton[1] < 5)
                    or (len(skeleton) == 2 and start_fret == 1 and skeleton[1] < 4)
                    or (len(skeleton) == 2 and start_fret == 2 and skeleton[1] < 3)
                    or (len(skeleton) == 2 and start_fret == 3 and skeleton[1] < 2)
                ):
                    continue
                # Ensuring valid skeletons of 3 in length.
                elif (
                    (len(skeleton) == 3 and start_fret == 0 and skeleton[2] < 5)
                    or (len(skeleton) == 3 and start_fret == 1 and skeleton[2] < 4)
                    or (len(skeleton) == 3 and start_fret == 2 and skeleton[2] < 3)
                ):
                    continue

                # Ensuring valid skeletons of 4 and over in length.
                elif len(skeleton) == 4 and start_fret == 0 and skeleton[-1] < 5:
                    continue
                for i in range(3, len(skeleton)):
                    a = skeleton[i - 3]
                    b = skeleton[i - 2]
                    c = skeleton[i - 1]
                    d = skeleton[i]
                    if b == a + 1 and c == b + 1 and d == c + 1:
                        break
                else:
                    return skeleton, string_grouping, start_fret

        case 3:
            ceiling = 14
            if length in ["r", ""]:
                # Limiting max skel lengths to avoid chromatic slop.
                length = random.choice(range(3, 12))
            elif isinstance(length, str):
                raise ValueError("See help (-h or --help) for rules regarding length.")
            elif 3 <= length <= 12:
                pass
            else:
                # Handling length being set by user in command line and string_grouping being random.
                length = random.choice(range(3, 12))
                print(
                    "\nWARNING! ValueError: Length for a string grouping of 3 can be between 3 and 12."
                )
            while True:
                skeleton = unearth_skeleton(length, ceiling)
                # Potentially optional avoidance of severe chromatic slop at start and end of skeleton.
                if skeleton[-3:-1] == [12,13] and skeleton[-1] == 14 and skeleton[1] == 1:
                    continue
                if skeleton[1] > 9:
                    continue
                if start_fret == 0:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and (skeleton[1] < 5 or skeleton[2] < 10):
                        continue
                    # Ensuring valid skeletons of 4 in length.
                    if len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                            # Ensuring valid skeletons of 6 in length.
                            or (
                                len(skeleton) == 6
                                and (skeleton[-3] < 5 and skeleton[-2] > 9)
                            )
                            # Ensuring valid skeletons of 7 in length.
                            or (
                                len(skeleton) == 7
                                and skeleton[-4] < 5
                                and skeleton[-3] > 9
                            )
                            # Ensuring valid skeletons of 8 in length.
                            or (
                                len(skeleton) == 8
                                and skeleton[-5] < 5
                                and skeleton[-4] > 9
                            )
                        ):
                            continue

                if start_fret == 1:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and (skeleton[1] < 4 or skeleton[2] < 9):
                        continue

                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                if start_fret == 2:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and (skeleton[1] < 3 or skeleton[2] < 8):
                        continue
                    # Avoiding FRETTED distances of over 4 frets (i.e. major third)
                    if skeleton[1] == 4 and skeleton[2] > 13:
                        continue
                    # Subtract based on allowable notes (1 per fret?)
                    # Ensuring valid skeletons of 4 in length.
                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                elif start_fret == 3:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and (skeleton[1] < 2 or skeleton[2] < 7):
                        continue
                    # Avoiding FRETTED distances of over 4 frets (i.e. major third)
                    elif skeleton[1] == 3 and skeleton[2] > 12:
                        continue
                    elif skeleton[1] == 4 and skeleton[2] > 13:
                        continue
                    # Subtract based on allowable notes (1 per fret?)
                    # Ensuring valid skeletons of 4 in length.
                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                elif start_fret == 4:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and skeleton[-1] < 6:
                        continue
                    # Avoiding FRETTED distances of over 4 frets (i.e. major third)
                    elif skeleton[1] == 2 and skeleton[2] > 11:
                        continue
                    elif skeleton[1] == 3 and skeleton[2] > 12:
                        continue
                    elif skeleton[1] == 4 and skeleton[2] > 13:
                        continue
                    # Subtract based on allowable notes (1 per fret?)
                    # Ensuring valid skeletons of 4 in length.
                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                elif start_fret == 5:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and skeleton[-1] < 5:
                        continue
                    elif skeleton[2] - skeleton[1] > 9:
                        continue
                    # Subtract based on allowable notes (1 per fret?)
                    # Ensuring valid skeletons of 4 in length.
                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                elif start_fret > 5:
                    # Ensuring valid skeletons of 3 in length.
                    if len(skeleton) == 3 and skeleton[-1] < 6:
                        continue
                    elif len(skeleton) == 3 and skeleton[2] - skeleton[1] > 9:
                        continue
                    # Subtract based on allowable notes (1 per fret?)
                    # Ensuring valid skeletons of 4 in length.
                    elif len(skeleton) == 4:
                        if (
                            (skeleton[-1] < 10)
                            or (skeleton[1] < 5 and skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[1] < 5 and skeleton[2] > 9 and skeleton[3] > 9)
                        ):
                            continue
                    # Ensuring valid skeletons of 5 (and above) in length.
                    elif len(skeleton) >= 5:
                        if (
                            (skeleton[1] < 5 and skeleton[2] > 9)
                            or (skeleton[2] < 5 and skeleton[3] > 9)
                            or (skeleton[3] < 5 and skeleton[4] > 9)
                            or (skeleton[-1] < 10)
                            or (skeleton[-2] < 5 and skeleton[-1] > 10)
                        ):
                            continue

                    elif (
                        # Ensuring valid skeletons of 6 in length.
                        (len(skeleton) == 6 and skeleton[-3] < 5 and skeleton[-2] > 9)
                        # Ensuring valid skeletons of 7 in length.
                        or (
                            len(skeleton) == 7 and skeleton[-4] < 5 and skeleton[-3] > 9
                        )
                        # Ensuring valid skeletons of 8 in length.
                        or (
                            len(skeleton) == 8 and skeleton[-5] < 5 and skeleton[-4] > 9
                        )
                    ):
                        continue

                for i in range(3, len(skeleton)):
                    a = skeleton[i - 3]
                    b = skeleton[i - 2]
                    c = skeleton[i - 1]
                    d = skeleton[i]
                    if b == a + 1 and c == b + 1 and d == c + 1:
                        break
                else:
                    return skeleton, string_grouping, start_fret


        case _:
            sys.exit(
                "Error. String grouping: 1 to 3 or 'r' for random (no argument defaults to random)."
            )


def set_start_fret(fret: int | str) -> int:
    """Sets starting fret for skeleton and validates optional_arguments().
    For use within form_skeleton() only.

    Args:
        fret (int | str, optional): The instrument's number of frets
        determines the highest possible starting fret
        to allow adequate room for skeletons
        (the ceiling is frets - 4). Defaults to "r" for random choice.

    Returns:
        int | str: Chosen int or random int.
    """
    if isinstance(fret, int):
        if fret < 0:
            raise ValueError(
                "Starting fret: number or 'r' for random (defaults to random)."
            )
        if fret > 21 - 4:
            sys.exit(
                "ValueError: Starting fret too high — you'll run out of frets!"
            )
        return fret
    elif isinstance(fret, str):
        if fret in ("r", ""):
            return random.choice(range(0, 21 - 4))
        else:
            raise ValueError(
                "Starting fret: number or 'r' for random (defaults to random)."
            )


def unearth_skeleton(length: int, ceiling: int) -> list[int]:
    """Generates list of unique integers for validation within form_skeleton().

    Args:
        length (int): Skeleton length.
        ceiling (int): Maximum allowed interval (i.e. relative note).
        Valid values vary based on string_grouping set by form_skeleton().

    Returns:
        list[int]: List of unique integers.
    """

    # Following if and elifs only pertinent when function used outside of module.
    if isinstance(length, str) or isinstance(ceiling, str):
        raise TypeError("Integers for length and ceiling, please.")
    elif length == 0:
        raise ValueError(
            "'0' is, hopefully, an obviously inappropriate, "
            "though somewhat philosophically intriguing, value for length."
            )
    elif length == ceiling + 2:
        raise ValueError("Ceiling must be at least length - 1")


    skeleton = sorted(random.sample(range(1, ceiling + 1), k=length-1))
    skeleton.extend([0])
    skeleton = sorted(skeleton)
    if len(skeleton) == 1:
        raise ValueError("Can we really call '1' a length?")
    return skeleton


def skeleton_to_fretboard(
    skeleton: list, string_grouping: int, start_fret: int
):
    """Skeleton interpreter. Provides output in pseudo-tablature.

    Args:
        skeleton (list): Pattern whose constituent indices will
        be assigned to frets or open strings.

        string_grouping (int): String group size (between 1 and 3).

        start_fret (int): Starting fret for skeleton.

    Raises:
        ValueError: If start_fret is a negative number.

    Returns:
        tuple[str, list, list, int, int, list]:

        tab_print [str]: Ready-to-print pseudo-tab).

        cipher [list]: Somewhat cryptic lists of integers representing fret numbers
        to be put in the correct order and applied to appropriate strings.

        starting_notes [list]: Put simply: open string + starting fret.

        start_fret [int]: Skeleton's starting fret.

        string_grouping [int]: String group size.

        skeleton [list]: Pattern of the raw interval values of the skeleton.
    """

    if start_fret < 0:
        raise ValueError("Starting fret: number or 'r' for random (defaults to random).")
    starting_notes = [
        (open_string + start_fret - 1) % 12 + 1
        
        # For each string in indices of notes in E standard
        for open_string in [4, 9, 2, 7, 11, 4]
    ]

    string_one, string_two, string_three = (
        starting_notes[0:3]
    )

    strings_one_three_five = starting_notes[0:5:2]
    strings_two_four_six = starting_notes[1:6:2]

    strings_one_four = starting_notes[0:5:3]
    strings_two_five = starting_notes[1:6:3]
    strings_three_six = starting_notes[2:6:3]

    cipher = []
    pad = 2 # Padding for tab_print

    match string_grouping:

        case 1:
            for _ in starting_notes:
                cipher.append([start_fret + i for i in skeleton])

        case 2:
            if len(skeleton) == 2:
                for _ in strings_one_three_five:
                    cipher.append([start_fret + skeleton[0]])
                for _ in strings_two_four_six:
                    if string_two < string_one:
                        cipher.append(
                            [
                                start_fret
                                - (((string_two + 12) % 24) - string_one)
                                + skeleton[1]
                            ]
                        )
                    else:
                        cipher.append(
                            [
                                start_fret
                                - ((string_two) - string_one)
                                + skeleton[1]
                            ]
                        )

            elif len(skeleton) == 3:
                if start_fret == 0:
                    for _ in strings_one_three_five:
                        cipher.append([start_fret + i for i in skeleton if i < 5])
                    for _ in strings_two_four_six:
                        if string_two < string_one:
                            cipher.append(
                                [
                                    start_fret
                                    - (
                                        ((string_two + 12) % 24)
                                        - string_one
                                    )
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )
                        else:
                            cipher.append(
                                [
                                    start_fret
                                    - ((string_two) - string_one)
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )

                elif start_fret == 1:
                    for _ in strings_one_three_five:
                        cipher.append([start_fret + i for i in skeleton if i < 4])
                    for _ in strings_two_four_six:
                        if string_two < string_one:
                            cipher.append(
                                [
                                    start_fret
                                    - (
                                        ((string_two + 12) % 24)
                                        - string_one
                                    )
                                    + i
                                    for i in skeleton
                                    if i >= 4
                                ]
                            )
                        else:
                            cipher.append(
                                [
                                    start_fret
                                    - ((string_two) - string_one)
                                    + i
                                    for i in skeleton
                                    if i >= 4
                                ]
                            )

                elif start_fret == 2:
                    if skeleton[2] == 9:
                        for _ in strings_one_three_five:
                            cipher.append(
                                [start_fret + i for i in skeleton if i <= 4 and i != 3]
                            )
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 3
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 3
                                    ]
                                )
                    else:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 3])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )

                elif start_fret == 3:
                    if skeleton[2] == 9:
                        for _ in strings_one_three_five:
                            cipher.append(
                                [start_fret + i for i in skeleton if i <= 4 and i != 2]
                            )
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 2
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 2
                                    ]
                                )
                    else:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 2])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 2
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 2
                                    ]
                                )

                elif start_fret == 4:
                    if skeleton[2] == 9:
                        for _ in strings_one_three_five:
                            cipher.append(
                                [start_fret + i for i in skeleton if i <= 4 and i != 1]
                            )
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 1
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 4 or i == 1
                                    ]
                                )

                    elif (
                        (skeleton[1] == 1 and skeleton[2] == 2)
                        or (skeleton[1] == 1 and skeleton[2] == 3)
                        or (skeleton[1] == 2 and skeleton[2] == 3)
                    ):
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + skeleton[0]])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 0
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 0
                                    ]
                                )

                    else:
                        for _ in strings_one_three_five:
                            cipher.append(
                                [start_fret + i for i in skeleton if i < 4 and i != 1]
                            )
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 4 or i == 1
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - ((string_two) - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 4 or i == 1
                                    ]
                                )

                elif skeleton[1] <= 4 and skeleton[2] <= 4:  # start_fret above 4
                    for _ in strings_one_three_five:
                        cipher.append(
                            [start_fret + skeleton[0], start_fret + skeleton[1]]
                        )
                    for _ in strings_two_four_six:
                        if string_two < string_one:
                            cipher.append(
                                [
                                    start_fret
                                    - (
                                        ((string_two + 12) % 24)
                                        - string_one
                                    )
                                    + skeleton[2]
                                ]
                            )
                        else:
                            cipher.append(
                                [
                                    start_fret
                                    - ((string_two) - string_one)
                                    + skeleton[2]
                                ]
                            )

                else:
                    for _ in strings_one_three_five:
                        cipher.append([start_fret + i for i in skeleton if i <= 4])
                    for _ in strings_two_four_six:
                        if string_two < string_one:
                            cipher.append(
                                [
                                    start_fret
                                    - (
                                        ((string_two + 12) % 24)
                                        - string_one
                                    )
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )
                        else:
                            cipher.append(
                                [
                                    start_fret
                                    - ((string_two) - string_one)
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )

            elif len(skeleton) >= 4:
                if start_fret == 0:
                    for _ in strings_one_three_five:
                        cipher.append([start_fret + i for i in skeleton if i < 5])
                    for _ in strings_two_four_six:
                        if string_two < string_one:

                            cipher.append(
                                [
                                    start_fret
                                    - (
                                        ((string_two + 12) % 24)
                                        + string_one
                                    )
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )
                        else:
                            cipher.append(
                                [
                                    start_fret
                                    - (string_two - string_one)
                                    + i
                                    for i in skeleton
                                    if i >= 5
                                ]
                            )

                elif start_fret == 1:
                    if skeleton[-1] == 4:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 4])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i == 4
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i == 4
                                    ]
                                )
                    else:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 5])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 5
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 5
                                    ]
                                )

                elif start_fret == 2:
                    if skeleton[-1] == 4:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 3])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )

                    elif skeleton[-1] == 9:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i <= 4])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 4
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 4
                                    ]
                                )

                    else:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 3])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )

                else:  # start_fret higher than 3
                    if skeleton[-1] == 4:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 3])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 3
                                    ]
                                )

                    elif skeleton[2] == 9:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i <= 4])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i > 4
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i > 4
                                    ]
                                )

                    else:
                        for _ in strings_one_three_five:
                            cipher.append([start_fret + i for i in skeleton if i < 5])
                        for _ in strings_two_four_six:
                            if string_two < string_one:
                                cipher.append(
                                    [
                                        start_fret
                                        - (
                                            ((string_two + 12) % 24)
                                            - string_one
                                        )
                                        + i
                                        for i in skeleton
                                        if i >= 5
                                    ]
                                )
                            else:
                                cipher.append(
                                    [
                                        start_fret
                                        - (string_two - string_one)
                                        + i
                                        for i in skeleton
                                        if i >= 5
                                    ]
                                )

        case 3:

            if len(skeleton) == 3:

                for _ in strings_one_four:
                    cipher.append([start_fret])
                for _ in strings_two_five:
                    if string_two < string_one:
                        cipher.append(
                            [
                                start_fret
                                - (((string_two + 12) % 24) - string_one)
                                + skeleton[1]
                            ]
                        )
                    else:
                        cipher.append(
                            [
                                start_fret
                                - ((string_two) - string_one)
                                + skeleton[1]
                            ]
                        )
                for _ in strings_three_six:
                    if string_three < string_one:
                        cipher.append(
                            [
                                start_fret
                                - (((string_three + 12) % 24) - string_one)
                                + skeleton[2]
                            ]
                        )
                    else:
                        cipher.append(
                            [
                                start_fret
                                - ((string_three) - string_one)
                                + skeleton[2]
                            ]
                        )

            elif len(skeleton) > 3:
                for _ in strings_one_four:
                    cipher.append([start_fret + i for i in skeleton if i < 5])
                for _ in strings_two_five:
                    if string_two < string_one:
                        cipher.append(
                            [
                                start_fret
                                - (((string_two + 12) % 24) - string_one)
                                + i
                                for i in skeleton
                                if 5 <= i <= 9
                            ]
                        )
                    else:
                        cipher.append(
                            [
                                start_fret
                                - ((string_two) - string_one)
                                + i
                                for i in skeleton
                                if 5 <= i <= 9
                            ]
                        )
                for _ in strings_three_six:
                    if string_three < string_one:
                        cipher.append(
                            [
                                start_fret
                                - (((string_three + 12) % 24) - string_one)
                                + i
                                for i in skeleton
                                if i >= 10
                            ]
                        )
                    else:
                        cipher.append(
                            [
                                start_fret
                                - ((string_three) - string_one)
                                + i
                                for i in skeleton
                                if i >= 10
                            ]
                        )

            tab_print = (
                f"{"e":<{pad}}"
                f"| {"--".join(map(str, cipher[5]))}\n"

                f"{"b":<{pad}}"
                f"| {"--".join(map(str, cipher[2]))}\n"

                f"{"g":<{pad}}"
                f"| {"--".join(map(str, cipher[4]))}\n"

                f"{"D":<{pad}}"
                f"| {"--".join(map(str, cipher[1]))}\n"

                f"{"A":<{pad}}"
                f"| {"--".join(map(str, cipher[3]))}\n"

                f"{"E":<{pad}}"
                f"| {"--".join(map(str, cipher[0]))}"
            )

            return tab_print, cipher, starting_notes, start_fret, string_grouping, skeleton

    tab_print = (
        f"{"e":<{pad}}"
        f"| {"--".join(map(str, cipher[5]))}\n"

        f"{"b":<{pad}}"
        f"| {"--".join(map(str, cipher[2]))}\n"

        f"{"g":<{pad}}"
        f"| {"--".join(map(str, cipher[4]))}\n"

        f"{"D":<{pad}}"
        f"| {"--".join(map(str, cipher[1]))}\n"

        f"{"A":<{pad}}"
        f"| {"--".join(map(str, cipher[3]))}\n"

        f"{"E":<{pad}}"
        f"| {"--".join(map(str, cipher[0]))}"
    )

    return tab_print, cipher, starting_notes, start_fret, string_grouping, skeleton


def get_skel_notes(
    cipher: list,
    starting_notes: list,
    start_fret: int,
    string_grouping: int,
    shflat: str = "#",
):
    """Provides all notes of a given skeleton.

    Args:
        cipher (list): Somewhat cryptic lists of integers representing fret numbers
        to be put in the correct order and applied to appropriate strings.
        Returned by skeleton_to_fretboard().

        starting_notes (list): Indices of the notes resulting from the transposition of all open strings to the starting fret,
        i.e. open string + starting fret, bearing in mind that C = 0.
        As returned by skeleton_to_fretboard().

        string_grouping (int): As returned by form_skeleton().

        start_fret (int): As returned by form_skeleton().

        shflat (str, optional): Whether to display sharps or flats.
        "#" for sharps, "b" for flats. Defaults to "#".

    Returns:
        list: All notes of the Skeleton after being
        appropriately applied to every string.
    """

    notes_dict = notes
    all_idx = []
    skel_notes = []
    match string_grouping:

        case 1:
            for starting_note in starting_notes:
                all_idx.append([starting_note - start_fret + i for i in cipher[0]])
            # Flatten the list of lists of indices...
            all_idx = [i for idx in all_idx for i in idx]

        case 2:
            for starting_note in starting_notes[0:5:2]:
                all_idx.append([starting_note - start_fret + i for i in cipher[0]])
            for starting_note in starting_notes[1:6:2]:
                all_idx.append([starting_note - start_fret + i for i in cipher[3]])
            all_idx = (
                all_idx[0]
                + all_idx[3]
                + all_idx[1]
                + all_idx[4]
                + all_idx[2]
                + all_idx[5]
            )

        case 3:
            for starting_note in starting_notes[0:5:3]:
                all_idx.append([starting_note - start_fret + i for i in cipher[0]])
            for starting_note in starting_notes[1:6:3]:
                all_idx.append([starting_note - start_fret + i for i in cipher[2]])
            for starting_note in starting_notes[2:6:3]:
                all_idx.append([starting_note - start_fret + i for i in cipher[4]])

            all_idx = (
                all_idx[0]
                + all_idx[2]
                + all_idx[4]
                + all_idx[1]
                + all_idx[3]
                + all_idx[5]
            )

    for idx in all_idx:
        for pos, note in notes_dict.items():
            if idx == pos:
                if len(note) == 2 and shflat == "#":
                    skel_notes.append(note[0])
                    break
                elif len(note) == 2 and shflat == "b":
                    skel_notes.append(note[1])
                    break
                else:
                    skel_notes.append(note[0])
                    break

    return skel_notes


if __name__ == "__main__":
    main()
