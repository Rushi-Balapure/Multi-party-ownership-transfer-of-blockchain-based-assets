from secretsharing import SecretSharer

class KeyManagement:
    def __init__(self, num_shards=5, threshold=3):
        self.num_shards = num_shards  # Total number of shards to generate
        self.threshold = threshold  # Minimum shards required to reconstruct the key
        self.shards = []

    def generate_key_shards(self, secret_key):
        # Split the secret key into multiple shards
        self.shards = SecretSharer.split_secret(secret_key, self.threshold, self.num_shards)
        print(f"Key split into {self.num_shards} shards with threshold {self.threshold}.")
        return self.shards

    def reconstruct_key(self, selected_shards):
        # Reconstruct the key from selected shards
        if len(selected_shards) < self.threshold:
            raise ValueError("Insufficient shards to reconstruct the key.")
        secret_key = SecretSharer.recover_secret(selected_shards)
        print("Key successfully reconstructed.")
        return secret_key

    def destroy_key(self):
        # Securely destroy the key by clearing the shards
        self.shards = []
        print("Key shards securely destroyed.")
# Initialize Key Management with 5 shards and threshold of 3
key_management = KeyManagement(num_shards=5, threshold=3)
secret_key = "super_secret_key_value"  # This would be a cryptographic key in a real implementation

# Generate shards
shards = key_management.generate_key_shards(secret_key)
print("Generated Shards:", shards)

# Select any 3 shards for reconstruction
selected_shards = shards[:3]  # For demonstration, we select the first 3 shards
reconstructed_key = key_management.reconstruct_key(selected_shards)
print("Reconstructed Key:", reconstructed_key)

# Destroy the key securely
key_management.destroy_key()
