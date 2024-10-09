from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import urllib.parse
from urllib.parse import unquote

key, iv = get_random_bytes(16), get_random_bytes(16)

def pad_pkcs7(data, block_size):
    padding_size = block_size - len(data) % block_size
    padding = bytes([padding_size]) * padding_size
    return data + padding

def submit(user_input, modified_iv):
    data = f"userid=456;userdata={user_input};session-id=31337"
    data = urllib.parse.quote(data)
    padded_data = pad_pkcs7(data.encode('utf-8'), 16)

    # Modify the last bit of the IV
    modified_iv[-1] ^= 1

    cipher = AES.new(key, AES.MODE_CBC, modified_iv)
    ciphertext = cipher.encrypt(padded_data)

    print("Modified Ciphertext:", ciphertext.hex())
    return ciphertext




def verify(ciphertext, modified_iv):
    cipher = AES.new(key, AES.MODE_CBC, modified_iv)
    decrypted_data = cipher.decrypt(ciphertext)

    # Flip the bit in the decrypted data
    decrypted_data = bytearray(decrypted_data)
    decrypted_data[-1] ^= 1  # Modify the first byte of the second block

    try:
        padding_size = decrypted_data[-1]
        if padding_size > 0 and decrypted_data[-padding_size:] == bytes([padding_size] * padding_size):
            print("Decrypted Data (Hex):", decrypted_data.hex())

            # Check for admin=true
            if b';admin=true;' in decrypted_data:
                return True
            else:
                return False
        else:
            return False
    except UnicodeDecodeError as e:
        print("Error decoding:", e)
        return False
    
def flip_bits(ciphertext, block_index, bit_index):
    if bit_index < 0 or bit_index >= 128:
        raise ValueError("Invalid bit index. It should be in the range [0, 127].")

    modified_ciphertext = bytearray(ciphertext)

    # Flip the bit in the original ciphertext block
    modified_ciphertext[block_index * 16 + bit_index // 8] ^= (1 << (bit_index % 8))

    return bytes(modified_ciphertext)



# Example
user_input = "You're the man now, dog"
modified_iv = bytearray(iv)
modified_iv[15] ^= 1

original_ciphertext = submit(user_input, modified_iv)
flipped_ciphertext = flip_bits(original_ciphertext[16:], 2, 3)
result = verify(flipped_ciphertext, modified_iv)
print("Verification Result:", result)
