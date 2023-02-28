import sys
import re
import time
import argparse
from multiprocessing.pool import ThreadPool
from src.bruteforce import *
from src.interface import *


if __name__ == "__main__":

	parser = argparse.ArgumentParser(
				prog = "SSH Brute force utility", 
				description = "Program that attempts to find the right SSH password given a wordlist file.", 
				epilog = "Do not use on machines you do not own or without explicit permission.")
	parser.add_argument(
						"host", 
						help = "Target host with active SSH service")
	parser.add_argument(
						"-p", 
						"--port", 
						help = "Port where the SSH service is running",
						required = True)
	parser.add_argument(
						"-u", 
						"--user", 
						help = "Known username for SSH service",
						required = True)
	parser.add_argument(
						"-t", 
						"--threads", 
						help = "Specify number of subprocesses for task - default is 3",
						required = False,
						type = int,
						default = 3)
	parser.add_argument(
						"-w", 
						"--wordlist", 
						help = "File that contains potential passwords; one item per line",
						required = False)

	args = parser.parse_args()
	host = args.host
	port = args.port
	user = args.user
	threads = args.threads
	wordlist = args.wordlist
	session = BruteForce(host, port, user)

	print(banner.graphics , "\n", banner.description, "\n")
	print(f"[~] Press CTRL+C twice to interrupt at any time...", "\n")

	if not re.search(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", host):
		print(colors.foreground.red, f"[!] Provided IP address is not a valid IPv4 address. Exiting...")
		sys.exit(1)
	
	if not threads <= 10:
		print(colors.foreground.red, 
		f"[!] Trying to open too many connections. Stopping...")
		sys.exit(1)

	try:
		with open(wordlist, "r") as f:
			wordlist = [line.rstrip() for line in f]

	except Exception as e:
		print(colors.foreground.yellow, 
			f"[!] Could not find a supplied wordlist...")
		print(colors.reset, 
			f"[#] Switching to default wordlist found in ~/data/wordlist.txt")
		with open("data/" + "wordlist.txt", mode = "r") as f:
			wordlist = [line.rstrip() for line in f]

	paramiko.util.log_to_file("/dev/null")

	try:
		with ThreadPool(threads) as pool:
			for result in pool.map(session.attack, wordlist):
				if result == False:
					pool.terminate()
					break

	except (KeyboardInterrupt, EOFError, SystemExit):
			sys.exit(1)

	finally:
		pool.close()
		pool.join()