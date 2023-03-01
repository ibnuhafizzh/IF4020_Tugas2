import numpy as np

# Fungsi substitusi menggunakan tabel S-box
def substitution(input_block):
    S_BOX = np.array([
        [0x9, 0x4, 0xA, 0xB],
        [0xD, 0x1, 0x8, 0x5],
        [0x6, 0x2, 0x0, 0x3],
        [0xC, 0xE, 0xF, 0x7]
    ])
    output_block = np.zeros_like(input_block)
    for i in range(4):
        row = input_block[i] >> 4
        col = input_block[i] & 0x0F
        output_block[i] = S_BOX[row][col]
    return output_block

# Fungsi permutasi menggunakan tabel permutasi
def permutation(input_block):
    PERMUTATION_TABLE = np.array([
        0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15
    ])
    output_block = np.zeros_like(input_block)
    for i in range(16):
        output_block[i] = input_block[PERMUTATION_TABLE[i]]
    return output_block

# Fungsi putaran menggunakan jaringan substitusi-permutasi
def round_function(input_block, round_key):
    output_block = substitution(input_block)
    output_block = permutation(output_block)
    output_block = np.bitwise_xor(output_block, round_key)
    return output_block

# Fungsi untuk menghasilkan kunci putaran
def generate_round_key(master_key, round_number):
    round_key = master_key ^ round_number
    round_key = round_key.to_bytes(16, byteorder='big')
    round_key = np.frombuffer(round_key, dtype=np.uint8)
    return round_key

# Fungsi enkripsi dan dekripsi menggunakan jaringan Feistel
def feistel_cipher(input_block, master_key, num_rounds):
    left_block = input_block[:8]
    right_block = input_block[8:]
    for i in range(num_rounds):
        round_key = generate_round_key(master_key, i)
        new_right_block = np.bitwise_xor(left_block, round_function(right_block, round_key))
        left_block = right_block
        right_block = new_right_block
    output_block = np.concatenate((right_block, left_block))
    return output_block

# Fungsi utama untuk enkripsi dan dekripsi pesan
def encrypt(input_message, master_key):
    BLOCK_SIZE = 16
    NUM_ROUNDS = 16
    num_blocks = len(input_message) // BLOCK_SIZE
    output_message = bytearray()
    for i in range(num_blocks):
        input_block = np.frombuffer(input_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], dtype=np.uint8)
        output_block = feistel_cipher(input_block, master_key, NUM_ROUNDS)
        output_message += bytes(output_block)
    return output_message

# Tes program
message = b'This is a secret message!'
key = int.from_bytes(b'This is a key.', byteorder='big')
encrypted_message = encrypt(message, key)
print('Encrypted message: ' + encrypted_message)