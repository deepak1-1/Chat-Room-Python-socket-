
from socket import *
from threading import Thread



class Server:

	def __init__(self):

		self.BYTE_LEN = 10
		self.FORMAT = 'utf-8'
		self.client_conn_username = []
		self.messages_list = []

		self.soc_server = socket(AF_INET, SOCK_STREAM)
		self.soc_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.soc_server.bind( ("127.0.0.1", 9000) )
		self.soc_server.listen()
		print("Server is listening to [ADDR] [127.0.0.1:9000]")

	
	def calculate_byte_len( self, message ):
		return len(message.encode('utf-8'))


	def add_bytes( self, message_byte_len ):
		
		actual_len = len(str(message_byte_len).encode(self.FORMAT))
		byte_to_be_added = self.BYTE_LEN - actual_len
		to_send_byte_len = b" "*byte_to_be_added + str(message_byte_len).encode(self.FORMAT)

		return to_send_byte_len


	def message_sender( self ):
		
		while True:
			while self.messages_list:
				message_data = self.messages_list.pop()
				for user_data in self.client_conn_username:
					if message_data[0] != user_data[1]:

						pretty_message = f"\n[{message_data[2]}]:> {message_data[1].decode(self.FORMAT)}"
						pretty_message_byte_len = self.calculate_byte_len( pretty_message )
						add_byte_to_message_len = self.add_bytes( pretty_message_byte_len )

						user_data[1].send( add_byte_to_message_len )  
						user_data[1].send( pretty_message.encode(self.FORMAT) )
	
	def message_receiver( self, conn ):

		while True:

			message_byte_len = int( conn.recv(self.BYTE_LEN).decode(self.FORMAT) )
			message = conn.recv( message_byte_len )

			username = ""
			for i in self.client_conn_username:
				if i[1] == conn:
					username = i[0]

			self.messages_list.append([ conn, message, username])



	def handle_connection( self, conn, addr ):

		while True:

			byte_len = int( conn.recv(self.BYTE_LEN).decode(self.FORMAT) ) # grabbing byte len
			username = conn.recv(byte_len).decode(self.FORMAT) #grabbing username
			user_pass = False

			for i in self.client_conn_username:
				if i[0] != username:
					user_pass = True

			if not(self.client_conn_username):
				user_pass = True

			send_message_byte_len = self.calculate_byte_len(str(user_pass))

			conn.send( self.add_bytes( send_message_byte_len ) )
			conn.send( str(user_pass).encode(self.FORMAT) )
			
			if user_pass:
				break

		print(f"[New Connection] [{addr}]   [USERNAME]  [{username}]")
		self.client_conn_username.append([username, conn])

		Thread(target=self.message_receiver, args=(conn, )).start()
		Thread(target=self.message_sender).start()


	def accept_connections(self):

		while True:
			conn, addr = self.soc_server.accept()
			new_connection_thread = Thread( target=self.handle_connection, args=(conn, addr) )
			new_connection_thread.start() 
			



if __name__ == "__main__":

	server = Server()
	server.accept_connections()