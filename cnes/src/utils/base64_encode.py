import base64

def base64_encode(n):
    byte_data = n.to_bytes((n.bit_length() + 7) // 8, 'big')
    base64_data = base64.b64encode(byte_data)
    base64_string = base64_data.decode('utf-8')
    return base64_string