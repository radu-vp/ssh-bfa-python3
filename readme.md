# SSH Brute-Force - Python3 Script

## Description

This python project is a small CLI utility that attempts to perform a brute-force attack on a SSH server, given a hostname/port, username and a possible password list.

## Installation Guide

```bash
pip3 install -r requirements.txt
```

## Features

* More password attacks by specifying the number of subprocesses (3 by default, maximum of 10)
* Successful login credentials saved in the same folder as `cracked.txt`
* Custom user-supplied wordlist
* Default wordlist powered by *10-million-password-list-top-100000.txt*. Source:
	* https://gitlab.com/kalilinux/packages/seclists/-/blob/kali/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt

## Usage

```bash
python3 main.py -p PORT -u USER [-t THREADS] [-w WORDLIST] host
```

Example:

```bash
python3 main.py 127.0.0.1 -p 22 -u admin -w wordlist.txt -t 10
```

## Help:

```bash
python3 main.py -h

usage: SSH Brute force utility [-h] -p PORT -u USER [-t THREADS] [-w WORDLIST] host

Program that attempts to find the right SSH password given a wordlist file.

positional arguments:
  host                  Target host with active SSH service

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port where the SSH service is running
  -u USER, --user USER  Known username for SSH service
  -t THREADS, --threads THREADS
                        Specify number of subprocesses for task - default is 3
  -w WORDLIST, --wordlist WORDLIST
                        File that contains potential passwords; one item per line

Do not use on machines you do not own or without explicit permission.
```

## References

1. Argparse - Docs available at: https://docs.python.org/3/library/argparse.html
2. Multiprocessing - Docs available at: https://docs.python.org/3/library/multiprocessing.html
2. Paramiko - Docs available at: https://www.paramiko.org/