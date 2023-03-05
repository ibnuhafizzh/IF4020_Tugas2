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
        # print(row, col)
        output_block[i] = S_BOX[row%4][col%4]
    return output_block

# # contoh penggunaan fungsi substitusi
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
    # print("this is input block", input_block)
    output_block = np.zeros_like(input_block)
    for i in range(16):
        # print(PERMUTATION_TABLE[i])
        output_block[i] = input_block[PERMUTATION_TABLE[i]]
    return output_block

# Fungsi putaran menggunakan jaringan substitusi-permutasi
def round_function(input_block, round_key):
    # print("input block" , input_block)
    # print("round key", round_key)
    output_block = substitution(input_block)
    output_block = permutation(output_block)
    output_block = xor_operation(output_block, round_key)
    return output_block

# Fungsi untuk menghasilkan kunci putaran
def generate_round_key(master_key, round_number):
    # round_key = master_key ^ round_number
    # round_key = round_key.to_bytes(16, byteorder='big')
    # round_key = np.frombuffer(round_key, dtype=np.uint8)
    
    round_number = [int(i) for i in list('{0:0b}'.format(round_number).zfill(len(master_key)))]
    
    # print("round number" , round_number)
    # print("master key", master_key)
    round_key = xor_operation(master_key,round_number)
    return round_key

def xor_operation(array1,array2):
    result = []
    for i in range(len(array1)):
        # print(array1[i], ' and', array2[i])
        result.append(array1[i] ^ array2[i])
    return result

# Fungsi jaringan Feistel
def feistel_cipher(input_block, master_key, num_rounds):
    left_block = input_block[:8]
    right_block = input_block[8:]
    for i in range(num_rounds):
        round_key = generate_round_key(master_key, i)
        # zfill buat nyamain xor aja
        new_right_block = xor_operation(left_block, round_function([int(i) for i in list(''.join(map(str, right_block)).zfill(len(round_key)))], round_key))
        left_block = right_block
        right_block = new_right_block
    output_block = np.concatenate((right_block, left_block))
    return output_block

# Fungsi enkripsi dan dekripsi pesan
def encrypt(input_message, master_key):
    BLOCK_SIZE = 16
    NUM_ROUNDS = 16
    input_message = [int(x) for x in input_message]
    master_key = [int(x) for x in master_key]
    num_blocks = len(input_message) // BLOCK_SIZE
    # print(len(input_message))
    output_message = []
    for i in range(num_blocks):
        input_block = np.array(input_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], dtype=np.uint8)
        output_block = feistel_cipher(input_block, master_key, NUM_ROUNDS)
        # print(i, " :" , output_block)
        output_message = np.concatenate((output_message, output_block))
    # print("enkripsi biner", output_message)
    output_message = output_message.astype(int)
    return output_message.tolist()

def decrypt(input_message, master_key):
    BLOCK_SIZE = 16
    NUM_ROUNDS = 16
    input_message = [int(x) for x in input_message]
    master_key = [int(x) for x in master_key]
    num_blocks = len(input_message) // BLOCK_SIZE
    output_message = []
    # print("ini oy", input_message)
    for i in range(num_blocks):
        input_block = np.array(input_message[i*BLOCK_SIZE:(i+1)*BLOCK_SIZE], dtype=np.uint8)
        left_block = input_block[:8]
        right_block = input_block[8:]
        round_keys = [generate_round_key(master_key, i) for i in range(NUM_ROUNDS)]
        for i in range(NUM_ROUNDS-1, -1, -1):
            new_right_block = left_block
            left_block = xor_operation(right_block, round_function([int(i) for i in list(''.join(map(str, left_block)).zfill(len(round_keys[i])))], round_keys[i]))
            right_block = new_right_block
        output_block = np.concatenate((left_block, right_block))
        # print("outblock nya", output_block)
        # print("ini output block", output_block)
        output_message = np.concatenate((output_message, output_block))
        output_message = output_message.astype(int)
    return output_message.tolist()

def binary_string_to_char(binary_str):
    # Split the binary string into 8-bit chunks
    chunks = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]

    # Convert each 8-bit chunk to a character
    chars = [chr(int(chunk, 2)) for chunk in chunks]

    # Join the characters into a string
    result = ''.join(chars)

    return result

# Tes program
message = 'assalamualaikumm'
print('\nmessage original: ' + message)
message = ''.join(format(ord(i), '08b') for i in message)
print('\nmessage binary: ' + message)
key = 'This is a key.iy'
print("key :", key)
key = ''.join(format(ord(i), '08b') for i in key)
# print("binary key", key))
encrypted_message = encrypt(message, key)
# print("panjang enkripted", len(encrypted_message), encrypted_message)

str_encrypted_message = ''.join(map(str, encrypted_message))

print("encrypted message in binary : ", str_encrypted_message)
print("encrypted char: ", binary_string_to_char(str_encrypted_message))
print()
print("=======")
print()
decrypted_message = decrypt(encrypted_message, key)

str_decrypted_message = ''.join(map(str, decrypted_message))

print("decrypted message in binary", str_decrypted_message)
print("decrypted char", binary_string_to_char(str_decrypted_message))
# print('\ndecrypted message: ' + decrypted_message.decode('utf-8'))