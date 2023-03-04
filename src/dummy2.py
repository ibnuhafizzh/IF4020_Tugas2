input_array = [1, 0, 1]  # Example input array
n = 8  # Desired length of padded array

# Zero-pad input array to length n
padded_array = [int(i) for i in list(''.join(map(str, input_array)).zfill(n))]

print("Padded array: ", padded_array)
