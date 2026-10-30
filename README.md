# Python Network Security

A Hyperskill Python project that uses TCP sockets to demonstrate dictionary-based login attacks and timing side-channel attacks against passwords.

## Features

- Establish a TCP connection to an authentication server.
- Identify a valid login using a dictionary attack with uppercase and lowercase variations.
- Attempt a timing side-channel attack to find a valid password for the login.

## Getting Started

```bash
git clone https://github.com/AlbertZubovic/python-network-security.git
cd python-network-security
```

Make sure Python 3 is installed. No third-party packages are required.

The program requires a TCP authentication server compatible with the Hyperskill Password Hacker project.

## Usage

Run the program with the server's IP address and port:

```bash
python hack.py 127.0.0.1 9090
```

The program attempts to identify a valid login using a dictionary attack, then uses response timing to discover the password.

On success, it prints the discovered credentials in JSON format (example output):

```json
{
  "login": "example_user",
  "password": "example_password"
}
```

**Note:** This project was developed and tested using the Hyperskill testing environment. A compatible authentication server is required to run it independently.

## Acknowledgements

Developed as part of the Password Hacker project on JetBrains Academy / Hyperskill.