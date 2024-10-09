from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import urllib.parse

BLOCK_SIZE = 16

# Define the padding function
def pad_pkcs7(data, block_size):
    padding_size = block_size - len(data) % block_size  # number of padding bytes needed
    padding = bytes([padding_size]) * padding_size      # create padding bytes
    return data + padding

# Unpadding function
def unpad_pkcs7(padded_data):
    padding_size = padded_data[-1]
    return padded_data[:-padding_size]

# Generate a random AES key and IV
def generate_key_and_iv():
    key = get_random_bytes(16) 
    iv = get_random_bytes(16)  # random 16-byte IV for CBC mode
    return key, iv 

# Encrypt data using AES in CBC mode
def encrypt_cbc(data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(data)
    return ciphertext

# Function to submit data, encrypting it with AES CBC mode
def submit(user_input):
    prefix = "userid=456;userdata="
    suffix = ";session-id=31337"
    
    # URL-encode the user input
    user_input_encoded = urllib.parse.quote(user_input)
    
    # Construct the final message
    message = (prefix + user_input_encoded + suffix).encode('utf-8')
    
    # Pad the message using PKCS7 padding
    padded_message = pad_pkcs7(message, BLOCK_SIZE)
    
    # Encrypt using AES-128-CBC
    ciphertext = encrypt_cbc(padded_message, key, iv)
    return ciphertext

# Function to verify if ";admin=true;" exists in the decrypted message
def verify(ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    
    # Unpad the plaintext
    plaintext = unpad_pkcs7(plaintext_padded).decode('utf-8', errors='ignore')
    
    # Print the decrypted message for debugging purposes
    print(f"Decrypted message: {plaintext}")
    
    # Check if the decrypted data contains ";admin=true;"
    return ";admin=true;" in plaintext

# XOR function for modifying blocks (bit-flipping)
def flip_bits(ciphertext, block_index, bit_index):
    modified_ciphertext = bytearray(ciphertext)
    modified_ciphertext[block_index * BLOCK_SIZE + bit_index // 8] ^= (1 << (bit_index % 8))
    return bytes(modified_ciphertext)

# Bit-flipping attack function
def bit_flipping_attack():
    # Controlled input to manipulate blocks
    user_input = "A" * BLOCK_SIZE * 3
    ciphertext = submit(user_input)
    
    # Convert ciphertext to a byte array for modification
    ciphertext = bytearray(ciphertext)

    # Target plaintext to appear in the decrypted result
    target_plaintext = b";admin=true;" + b"A" * (BLOCK_SIZE - len(";admin=true;"))
    
    # Block to modify (modifying the second ciphertext block)
    block_to_modify = 1

    # Original plaintext for the block (block of 'A's)
    original_plaintext = b"A" * BLOCK_SIZE
    
    # XOR the original plaintext with the target plaintext to get the XOR delta
    xor_delta = bytes([a ^ b for a, b in zip(original_plaintext, target_plaintext)])
    
    # Apply the XOR delta to the second ciphertext block (to affect the third plaintext block)
    for i in range(len(xor_delta)):
        ciphertext[block_to_modify * BLOCK_SIZE + i] ^= xor_delta[i]
    
    # Verify if the attack was successful and print decrypted message
    return verify(bytes(ciphertext))

if __name__ == "__main__":
    # Generate key and IV
    key, iv = generate_key_and_iv()
    
    # Run the bit-flipping attack
    result = bit_flipping_attack()
    print(f"Bit-flipping attack successful: {result}")



