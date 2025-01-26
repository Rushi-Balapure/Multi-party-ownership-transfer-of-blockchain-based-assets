import socket
import pickle
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.shard = None

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print("Connected to server")

    def join_team(self):
        try:
            # Send join request
            self.client_socket.send(pickle.dumps({'action': 'join_team'}))

            # Wait for the server's response
            # response = pickle.loads(self.client_socket.recv(4096))
            # print("Response:", response)

            # Wait for team closure and shard distribution
            while True:
                try:
                    data = pickle.loads(self.client_socket.recv(4096))
                    if data.get('action') == 'receive_shard':
                        self.shard = data['shard']
                        print(f"Shard received and stored: {self.shard}")
                        break  # Exit the loop after receiving the shard
                except EOFError:
                    print("Error receiving shard from server.")
                    break
        except Exception as e:
            print(f"Error during team joining: {e}")
            self.client_socket.close()

    def handle_server_messages(self):
        while True:
            try:
                data = pickle.loads(self.client_socket.recv(4096))
                if data.get('action') == 'request_shard':
                    self.decide_sharing()
                elif data.get('action') == 'waiting_for_shards':
                    print("Waiting for shards from all clients...")
                elif data.get('action') == 'rejected_shard':
                    print(f"Client {data['client']} rejected sharing their shard.")
            except Exception as e:
                print(f"Disconnected from server. Error: {e}")
                break

    def decide_sharing(self):
        choice = input("Server is requesting your shard. Do you want to share it? (yes/no): ")
        if choice.lower() == "yes" and self.shard:
            self.client_socket.send(pickle.dumps({'action': 'share_shard', 'shard': self.shard}))
            print("Shard sent to server.")
        elif choice.lower() == "no":
            self.client_socket.send(pickle.dumps({'action': 'reject_shard'}))
            print("Shard not shared.")
        else:
            print("Invalid choice. Please respond with 'yes' or 'no'.")

    def initiate_transaction(self):
        try:
            self.client_socket.send(pickle.dumps({'action': 'initiate_transaction'}))
            print("Transaction initiation requested.")
        except Exception as e:
            print(f"Error initiating transaction: {e}")

    def menu(self):
        threading.Thread(target=self.handle_server_messages, daemon=True).start()
        while True:
            print("\n--- Client Menu ---")
            print("1. Join Team")
            print("2. Initiate Transaction")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.join_team()
            elif choice == "2":
                self.initiate_transaction()
            elif choice == "3":
                print("Exiting...")
                self.client_socket.close()
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    client = Client('127.0.0.1', 65432)
    client.connect()
    client.menu()
