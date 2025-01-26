import socket
import threading
import pickle
from Key_Management import KeyManagement
from Transaction_process import TransactionProcessing, BlockchainNetwork

class Server:
    def __init__(self, host, port, num_shards, threshold):
        self.host = host
        self.port = port
        self.num_shards = num_shards
        self.threshold = threshold
        self.clients = {}
        self.key_manager = KeyManagement(self.num_shards)
        self.shards = []
        self.lock = threading.Lock()
        self.team_closed = False  # Track whether the team is closed

    def handle_client(self, client_socket, client_address):
        try:
            while True:
                data = pickle.loads(client_socket.recv(4096))
                if data['action'] == 'join_team':
                    with self.lock:
                        if self.team_closed:
                            client_socket.send(pickle.dumps({'status': 'Team formation is closed.'}))
                        else:
                            self.clients[client_address] = client_socket
                            client_socket.send(pickle.dumps({'status': 'Team joined. Waiting for team closure...'}))
                            print(f"Client {client_address} joined the team.")
                elif data['action'] == 'initiate_transaction':
                    self.request_shards()
                elif data['action'] == 'share_shard':
                    shard = data['shard']
                    with self.lock:
                        self.shards.append(shard)
                        if len(self.shards) >= self.threshold:
                            self.reconstruct_and_initiate()
        except:
            print(f"Connection with {client_address} lost.")
            with self.lock:
                if client_address in self.clients:
                    del self.clients[client_address]

    # def close_team(self):
        # with self.lock:
        #     self.team_closed = True
        #     print("Team formation manually closed. Generating and distributing shards...")
        #     secret_key_hex = "ABD3410FE"  # Example secret key
        #     shards = self.key_manager.generate_key_shards(secret_key_hex)
        #     for i, client_address in enumerate(self.clients):
        #         client_socket = self.clients[client_address]
        #         shard = shards[i]
        #         client_socket.send(pickle.dumps({'action': 'receive_shard', 'shard': shard}))
        #     print("Shards distributed to all clients.")
    def close_team(self):
        with self.lock:
            self.team_closed = True
            print("Team formation manually closed. Generating and distributing shards...")
            secret_key_hex = "ABD3410FE"  # Example secret key
            shards = self.key_manager.generate_key_shards(secret_key_hex)
            for i, client_address in enumerate(self.clients):
                client_socket = self.clients[client_address]
                client_socket.send(pickle.dumps({'action': 'receive_shard', 'shard': shards[i]}))
            print("Shards distributed to all clients.")

    def request_shards(self):
        print("Requesting shards from all clients...")
        for client_address, client_socket in self.clients.items():
            client_socket.send(pickle.dumps({'action': 'request_shard'}))

    def reconstruct_and_initiate(self):
        reconstructed_key = self.key_manager.reconstruct_key(self.shards[:self.threshold])
        blockchain_network = BlockchainNetwork()
        transaction_processor = TransactionProcessing(blockchain_network)
        transaction_processor.initiate_transaction("Sample Transaction", reconstructed_key)
        print("Transaction successfully completed.")

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print("Server started, waiting for connections...")

        # Start a thread for handling manual team closure
        threading.Thread(target=self.manual_close_team, daemon=True).start()

        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address}")
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()

    def manual_close_team(self):
        while True:
            command = input("Type 'close' to close the team: ").strip().lower()
            if command == 'close':
                self.close_team()

if __name__ == "__main__":
    server = Server('127.0.0.1', 65432, num_shards=2, threshold=2)
    server.start()
