import random
from functools import reduce
from cryptography.hazmat.primitives import hashes

class KeyManagement:
    def __init__(self, num_shards=5, threshold=3):
        self.num_shards = num_shards
        self.threshold = threshold
        self.shards = []

    def generate_key_shards(self, secret_key):
        secret_int = int.from_bytes(secret_key.encode(), 'big')
        coeffs = [secret_int] + [random.SystemRandom().randint(0, 2**128) for _ in range(self.threshold - 1)]
        self.shards = [(i, self._evaluate_polynomial(coeffs, i)) for i in range(1, self.num_shards + 1)]
        print(f"Generated {len(self.shards)} shards with threshold {self.threshold}.")
        return self.shards

    def reconstruct_key(self, selected_shards):
        if len(selected_shards) < self.threshold:
            raise ValueError("Insufficient shards to reconstruct the key.")
        secret_int = self._lagrange_interpolation(0, selected_shards)
        secret_key = secret_int.to_bytes((secret_int.bit_length() + 7) // 8, 'big').decode()
        print("Key successfully reconstructed.")
        return secret_key

    def destroy_key(self):
        self.shards = []
        print("Key shards securely destroyed.")

    def _evaluate_polynomial(self, coeffs, x):
        return sum([c * (x ** i) for i, c in enumerate(coeffs)])

    def _lagrange_interpolation(self, x, points):
        def basis(j):
            return reduce(lambda acc, m: acc * (x - points[m][0]) / (points[j][0] - points[m][0]),[m for m in range(len(points)) if m != j], 1)
        return round(sum(points[j][1] * basis(j) for j in range(len(points))))
    

# Initialize Key Management with 5 shards and threshold of 3
threshold =3
num_shards=5
key_management = KeyManagement(num_shards, threshold)
secret_key = "super_secret_key_value"  # This would be a cryptographic key in a real implementation

# Generate shards
shards = key_management.generate_key_shards(secret_key)
print("Generated Shards:", shards)

# Select any 3 shards for reconstruction
selected_shards = shards[:threshold]  # For demonstration, we select the first 3 shards
reconstructed_key = key_management.reconstruct_key(selected_shards)
print("Reconstructed Key:", reconstructed_key)

# Destroy the key securely
key_management.destroy_key()
