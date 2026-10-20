from Crypto.Cipher import AES

key = b'1234567890123456'                      
plaintext = b"UIT_LAB_UIT_LAB_UIT_LAB_UIT_LAB_" 
iv = b'ABCDEFGHIJKLMNOP'                       

def split_blocks(ct):
    return [ct[i:i+16].hex() for i in range(0, len(ct), 16)]

results = {}

results["ECB"] = AES.new(key, AES.MODE_ECB).encrypt(plaintext)

results["CBC"] = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(plaintext)

results["CFB"] = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128).encrypt(plaintext)

results["OFB"] = AES.new(key, AES.MODE_OFB, iv=iv).encrypt(plaintext)

results["CTR"] = AES.new(key, AES.MODE_CTR, nonce=iv[:8]).encrypt(plaintext)

for name, ct in results.items():
    b1, b2 = split_blocks(ct)
    print(f"{name}: {ct.hex()}")
    print(f"   Khối 1: {b1}")
    print(f"   Khối 2: {b2}")
    print(f"   Khối 1 == Khối 2 ? {b1 == b2}\n")