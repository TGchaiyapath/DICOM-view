import base64

def text_to_binary(text):
    binary_str = ''.join(format(ord(char), '08b') for char in text)
    return binary_str

def split_binary_to_eight_bits(binary_str):
    eight_bit_chunks = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ' '.join(eight_bit_chunks)

def split_binary_to_six_bits(binary_str):
    six_bit_chunks = [binary_str[i:i+6] for i in range(0, len(binary_str), 6)]
    return ' '.join(six_bit_chunks)

def binary_to_base64(binary_str):
    binary_data = ''.join(binary_str.split())
    byte_data = int(binary_data, 2).to_bytes((len(binary_data) + 7) // 8, byteorder='big')
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str

def encode_text_to_base64(text):
    binary_str = text_to_binary(text)
    eight_bit_chunks = split_binary_to_eight_bits(binary_str)
    six_bit_chunks = split_binary_to_six_bits(binary_str)
    base64_str = binary_to_base64(binary_str)
    return eight_bit_chunks, six_bit_chunks, base64_str

# Example usage
text_input = "Phoofa"
eight_bit_chunks, six_bit_chunks, base64_output = encode_text_to_base64(text_input)

print(f"Original Text: {text_input}")
print(f"8-Bit Binary Chunks: {eight_bit_chunks}")
print(f"6-Bit Binary Chunks (for Base64): {six_bit_chunks}")
print(f"Base64 Output: {base64_output}")