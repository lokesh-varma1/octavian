def find_key(plaintext, ciphertext):
    """
    Derive the key based on the known plaintext and ciphertext.
    The key represents the column order used in the transposition cipher.
    """
    if len(plaintext) != len(ciphertext):
        raise ValueError("Plaintext and ciphertext must have the same length.")

    # Create a mapping of ciphertext letters to the indices in the plaintext
    mapping = sorted(range(len(ciphertext)), key=lambda i: ciphertext[i])
    
    # The key will be the order of columns in the transposition
    key = sorted(range(len(mapping)), key=lambda i: mapping[i])

    return key

def decrypt_with_key(ciphertext, key):
    """
    Decrypt a given ciphertext using the derived key.
    """
    # Calculate the number of columns based on the key length
    num_columns = len(key)
    
    # Split ciphertext into columns based on the length of the key
    rows, extra = divmod(len(ciphertext), num_columns)
    
    # Create a grid to store the transposed columns
    grid = [''] * num_columns
    k = 0
    
    for col in key:
        # Determine how many characters each column will have
        col_length = rows + 1 if col < extra else rows
        grid[col] = ciphertext[k:k + col_length]
        k += col_length
    
    # Read the rows in the grid to form the decrypted plaintext
    decrypted_text = ''.join([grid[col][i] for i in range(rows + 1) for col in range(num_columns) if i < len(grid[col])])

    return decrypted_text

# Example usage
plaintext = "WarmMorning"
ciphertext = "IRRMNMOWAGN"
ciphertext_to_decrypt = "SENNOYPFUNR"

# Step 1: Find the key based on the known plaintext and ciphertext
key = find_key(plaintext, ciphertext)
print("Derived Key:", key)

# Step 2: Decrypt another ciphertext using the derived key
decrypted_text = decrypt_with_key(ciphertext_to_decrypt, key)
print("Decrypted Text:", decrypted_text)
