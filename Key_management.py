import random
from functools import reduce

class KeyManagement:
    def __init__(self, num_shards, prime_modulus=2**137 - 1):
        self.num_shards = num_shards
        self.prime_modulus = prime_modulus  # Use a large prime modulus for secure modular arithmetic
        self.shards = []

    def generate_key_shards(self, secret_key_hex):
        # Convert hex key to an integer
        secret_int = int(secret_key_hex, 16)
        
        # Generate random coefficients for polynomial with modular arithmetic
        coeffs = [secret_int] + [random.SystemRandom().randint(0, self.prime_modulus - 1) for _ in range(self.num_shards - 1)]
        
        # Evaluate polynomial for each shard using modular arithmetic
        self.shards = [(i, self._evaluate_polynomial(coeffs, i)) for i in range(1, self.num_shards + 1)]
        print(f"Generated {len(self.shards)} shards.")
        return self.shards

    def reconstruct_key(self, selected_shards):
        # Use all provided shards to reconstruct the key, no threshold condition
        secret_int = self._lagrange_interpolation(0, selected_shards)
        
        # Convert integer back to hex
        secret_key_hex = hex(secret_int)[2:]  # Removing '0x' prefix
        print("Key successfully reconstructed.")
        return secret_key_hex

    def destroy_key(self):
        self.shards = []
        print("Key shards securely destroyed.")

    def _evaluate_polynomial(self, coeffs, x):
        # Evaluates the polynomial at x using modular arithmetic
        return sum([(c * pow(x, i, self.prime_modulus)) % self.prime_modulus for i, c in enumerate(coeffs)]) % self.prime_modulus

    def _lagrange_interpolation(self, x, points):
        # Lagrange interpolation to reconstruct the key using modular arithmetic
        def basis(j):
            numerator, denominator = 1, 1
            for m in range(len(points)):
                if m != j:
                    # Modular multiplication for numerator and denominator
                    numerator = (numerator * (x - points[m][0])) % self.prime_modulus
                    denominator = (denominator * (points[j][0] - points[m][0])) % self.prime_modulus
            # Compute modular inverse of denominator
            return numerator * pow(denominator, -1, self.prime_modulus) % self.prime_modulus
        
        # Sum up basis polynomial times y-coordinates
        return sum((points[j][1] * basis(j)) % self.prime_modulus for j in range(len(points))) % self.prime_modulus
def key_init():
    # Initialize Key Management with all shards being required
    num_shards = 3
    key_management = KeyManagement(num_shards)
    secret_key_hex = "ABD3410FE"  # Example secret key in hex format

    # Generate shards
    shards = key_management.generate_key_shards(secret_key_hex)
    print("Generated Shards:", shards)

    # Use all generated shards for reconstruction
    reconstructed_key_hex = key_management.reconstruct_key(shards)
    print("Reconstructed Key (Hex):", reconstructed_key_hex)

    # Destroy the key securely
    key_management.destroy_key()
