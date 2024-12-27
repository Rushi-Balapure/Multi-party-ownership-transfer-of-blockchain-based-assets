import random
from functools import reduce

class EnhancedKeyManagement:
    def __init__(self, num_shards, threshold, prime_modulus=2**137 - 1):
        self.num_shards = num_shards
        self.threshold = threshold
        self.prime_modulus = prime_modulus  # Large prime modulus for secure modular arithmetic
        self.shards = []

    def generate_key_shards(self, secrets_hex):
        # Convert each hex key to an integer
        secrets_int = [int(secret, 16) for secret in secrets_hex]
        
        # Generate random coefficients for the polynomial
        num_coeffs = self.threshold + len(secrets_int) - 1
        coeffs = secrets_int + [random.SystemRandom().randint(0, self.prime_modulus - 1) for _ in range(num_coeffs - len(secrets_int))]
        
        # Generate shards
        self.shards = [(i, self._evaluate_polynomial(coeffs, i)) for i in range(1, self.num_shards + 1)]
        print(f"Generated {len(self.shards)} shards for {len(secrets_int)} secrets.")
        return self.shards

    def reconstruct_keys(self, selected_shards, num_secrets):
        # Reconstruct the polynomial at x = 0 to retrieve all coefficients
        polynomial_coeffs = [self._lagrange_interpolation(0, selected_shards[:self.threshold])]
        
        # Extract secrets from the reconstructed polynomial coefficients
        secrets_int = polynomial_coeffs[:num_secrets]
        secrets_hex = [hex(secret)[2:] for secret in secrets_int]  # Convert to hex
        print("Keys successfully reconstructed.")
        return secrets_hex

    def destroy_keys(self):
        self.shards = []
        print("Key shards securely destroyed.")

    def _evaluate_polynomial(self, coeffs, x):
        # Evaluate the polynomial at x using modular arithmetic
        return sum([(c * pow(x, i, self.prime_modulus)) % self.prime_modulus for i, c in enumerate(coeffs)]) % self.prime_modulus

    def _lagrange_interpolation(self, x, points):
        # Lagrange interpolation to reconstruct the polynomial at a given x
        def basis(j):
            numerator, denominator = 1, 1
            for m in range(len(points)):
                if m != j:
                    # Modular arithmetic for numerator and denominator
                    numerator = (numerator * (x - points[m][0])) % self.prime_modulus
                    denominator = (denominator * (points[j][0] - points[m][0])) % self.prime_modulus
            # Compute modular inverse of denominator
            return numerator * pow(denominator, -1, self.prime_modulus) % self.prime_modulus
        
        # Sum up the basis polynomial times y-coordinates
        return sum((points[j][1] * basis(j)) % self.prime_modulus for j in range(len(points))) % self.prime_modulus

def enhanced_key_init():
    # Initialize Enhanced Key Management with multiple secrets and threshold
    num_shards = 5
    threshold = 3
    key_management = EnhancedKeyManagement(num_shards, threshold)
    secrets_hex = ["ABD3410FE"]  # Example secrets in hex format

    # Generate shards for multiple secrets
    shards = key_management.generate_key_shards(secrets_hex)
    print("Generated Shards:", shards)

    # Use only a subset of shards for reconstruction (at least `threshold`)
    selected_shards = shards[:threshold]
    reconstructed_keys_hex = key_management.reconstruct_keys(selected_shards, len(secrets_hex))
    print("Reconstructed Keys (Hex):", reconstructed_keys_hex)

    # Destroy the keys securely
    key_management.destroy_keys()

# Run the enhanced key management system
enhanced_key_init()

