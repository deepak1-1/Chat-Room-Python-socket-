

from socket import *
from threading import Thread
from time import sleep


class Client:

	def __init__(self):

		self.FORMAT = 'utf-8'
		self.BYTE_LEN = 2048
		self.username = ""
		self.client_socket = socket(AF_INET, SOCK_STREAM)
		self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	

	def connect_(self):

		try:
			self.client_socket.connect( ('127.0.0.1', 9000) )
		except:
			print('SERVER is not started yet!')
			return False

		return True

	
	def calculate_byte_len(self, message):
		return len(message.encode(self.FORMAT))


	def add_bytes( self, message_byte_len ):
		
		actual_len = len(str(message_byte_len).encode(self.FORMAT))
		byte_to_be_added = self.BYTE_LEN - actual_len
		to_send_byte_len = b""*byte_to_be_added + str(message_byte_len).encode(self.FORMAT)

		return to_send_byte_len


	def register_username(self):

		while True:

			username = input('[USERNAME]:>')
			if username.strip() == "":
				print('[NOT VALID]')
				continue

			username_byte_len = self.calculate_byte_len(username)
			self.client_socket.send( self.add_bytes(username_byte_len) )
			self.client_socket.send( username.encode(self.FORMAT) )

			server_message_byte_len = int( self.client_socket.recv(self.BYTE_LEN).decode(self.FORMAT) )
			server_message = self.client_socket.recv( server_message_byte_len ).decode(self.FORMAT)

			if(server_message == 'True'):
				self.username = username
				break

			print(f"!![USERNAME]: {username} already exists")


	def message_receiver( self ):

		while True:

			try:
				message_byte_len = int( self.client_socket.recv(self.BYTE_LEN).decode(self.FORMAT) )
				message_from_server = self.client_socket.recv( message_byte_len ).decode(self.FORMAT)
				print(message_from_server)

			except Exception as e:
				print('Unable to receive Message from server [PLEASE RECONNECT]')
				print(e)
				break


	def message_sender( self ):

		while True:

			try:
				message = input(f"[{self.username.upper()}]:>")
				message_byte_len = self.calculate_byte_len(message)
				self.client_socket.send( self.add_bytes(message_byte_len) )
				self.client_socket.send( message.encode(self.FORMAT) )

			except Exception as e:
				print('Unable to send Messages to server [PLEASE RECONNECT]')
				print(e)
				break



if __name__ == "__main__":

	client = Client()

	if client.connect_():
		client.register_username()
		Thread(target=client.message_receiver).start()
		client.message_sender()
