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
        print(row, col)
        output_block[i] = S_BOX[row%4][col%4]
    return output_block

# contoh penggunaan fungsi substitusi
# input_block = np.array([0x22, 0x34, 0x56, 0x78])
# output_block = substitution(input_block)
# print("Input block: ", input_block)
# print("Output block:", output_block)

# Fungsi permutasi menggunakan tabel permutasi
def permutation(input_block):
    PERMUTATION_TABLE = np.array([
        0, 4, 8, 12,
        1, 5, 9, 13,
        2, 6, 10, 14,
        3, 7, 11, 15
    ])
    print("this is input block", input_block)
    output_block = np.zeros_like(input_block)
    for i in range(16):
        print(PERMUTATION_TABLE[i])
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

# Fungsi jaringan Feistel
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

# Fungsi enkripsi dan dekripsi pesan
def encrypt(input_message, master_key):
    BLOCK_SIZE = 16
    NUM_ROUNDS = 16
    input_message = [x for x in input_message]
    master_key = [x for x in master_key]
    num_blocks = len(input_message) // BLOCK_SIZE
    print(len(input_message))
    output_message = bytearray()
    for i in range(num_blocks):
        input_block = np.array(input_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], dtype=np.uint8)
        output_block = feistel_cipher(input_block, master_key, NUM_ROUNDS)
        output_message += bytes(output_block)
    return output_message

def decrypt(input_message, master_key):
    BLOCK_SIZE = 16
    NUM_ROUNDS = 16
    num_blocks = len(input_message) // BLOCK_SIZE
    output_message = bytearray()
    for i in range(num_blocks):
        input_block = np.frombuffer(input_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], dtype=np.uint8)
        print("ini input block", input_block)
        left_block = input_block[:8]
        right_block = input_block[8:]
        round_keys = [generate_round_key(master_key, i) for i in range(NUM_ROUNDS)]
        for i in range(NUM_ROUNDS-1, -1, -1):
            new_right_block = left_block
            left_block = np.bitwise_xor(right_block, round_function(left_block, round_keys[i]))
            right_block = new_right_block
        output_block = np.concatenate((left_block, right_block))
        output_message += bytes(output_block)
    return output_message

# Tes program
message = 'anjing ppppppppp'
print('\nmessage original: ' + message)
message = ''.join(format(ord(i), '08b') for i in message)
print('\nmessage binary: ' + message)
key = 'This is a key.iy'
print("key", key)
key = ''.join(format(ord(i), '08b') for i in key)
encrypted_message = encrypt(message, key)

print("after", key)
print('\nencrypted message: ' + (encrypted_message).decode('utf-8'))
decrypted_message = decrypt(encrypted_message, key)
print('\ndecrypted message: ' + decrypted_message.decode('utf-8'))