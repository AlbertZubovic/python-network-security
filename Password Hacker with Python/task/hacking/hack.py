from itertools import product
from socket import socket
from argparse import ArgumentParser
from typing import Iterator
from string import ascii_lowercase, ascii_uppercase, digits


type CharacterRange = tuple[str, str]
type CharacterRanges = tuple[CharacterRange] | tuple[CharacterRange, CharacterRange] | tuple[CharacterRange, CharacterRange, CharacterRange]


def main():
    """Connect to a TCP Server and find its password through brute force."""
    parser: ArgumentParser = ArgumentParser(description="Connect to a TCP Server, send a message and display the result.")


    # Add command line arguments
    parser.add_argument("ip_address")
    parser.add_argument("port", type=int)

    args = parser.parse_args()
    ip_address: str = args.ip_address
    port: int = args.port

    # Establish a socket connection
    with socket() as client_socket:
        address: tuple[str, int] = (ip_address, port)

        client_socket.connect(address)

        for candidate in generate_candidates((("a", "z"), ("0", "9"))):
            client_socket.sendall(candidate.encode())

            if client_socket.recv(1024).decode() == "Connection success!":
                print(candidate)
                break


def generate_candidates(character_ranges: CharacterRanges = (("A", "Z"), ("a", "z"), ("0", "9"))) -> Iterator[str]:
    """
    Lazily generates password candidates using the specified character ranges.

    Candidates are generated in increasing order of length, starting at one
    character and continuing up to the configured maximum length.

    Args:
        fields -- A tuple of character ranges, each represented by a pair of inclusive bounds.
    Yields:
        str: The next password candidate.
    """

    upper = []
    lower = []
    digit = []
    groups = []

    def parse_char_list(char_range: CharacterRange) -> tuple[str, list[str]]:
        """Classify a character range and return its category and characters."""


        match char_range:
            case (str(start), str(end)) if start.isupper() and end.isupper():
                return "upper", [char for char in ascii_uppercase if start <= char <= end]
            case (str(start), str(end)) if start.islower() and end.islower():
                return "lower", [char for char in ascii_lowercase if start <= char <= end]
            case (str(start), str(end)) if start.isdigit() and end.isdigit():
                return "digit", [char for char in digits if start <= char <= end]
            case _:
                raise ValueError("Expected string fields")

    # Perform checks on parameters and assign variables for each range
    try:

        if not 1 <= len(character_ranges) <= 3:
            raise ValueError("Expected between 1 and 3 ranges")

        for field in character_ranges:
            if len(field) != 2 or any(len(i) != 1 for i in field) or field[0] > field[1]:
                raise ValueError("Each range must contain exactly two single characters in ascending order.")

            kind, chars = parse_char_list(field)

            match kind:
                case "upper":
                    upper.extend(chars)
                case "lower":
                    lower.extend(chars)
                case "digit":
                    digit.extend(chars)

        chars = upper + lower + digit

        for i in range(1, 6):
            yield from ("".join(p) for p in product(chars, repeat=i))

    except ValueError as e:
        print(f"Invalid Input: {e}")
        return





if __name__ == "__main__":
    main()