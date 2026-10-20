def normalize_text(text):
    return ''.join([char.upper() for char in text if char.isalpha()])

def vigenere_encrypt(plaintext, key):
    pt = normalize_text(plaintext)
    k = normalize_text(key)
    
    if not k:
        return "Lỗi: Khóa không được để trống hoặc thiếu ký tự alphabet."

    ciphertext = []
    for i, char in enumerate(pt):
        p_val = ord(char) - ord('A')
        k_val = ord(k[i % len(k)]) - ord('A')
        
        # C = (P + K) mod 26
        c_val = (p_val + k_val) % 26
        ciphertext.append(chr(c_val + ord('A')))
        
    return "".join(ciphertext)

def vigenere_decrypt(ciphertext, key):
    ct = normalize_text(ciphertext)
    k = normalize_text(key)
    
    if not k:
        return "Lỗi: Khóa không được để trống hoặc thiếu ký tự alphabet."

    plaintext = []
    for i, char in enumerate(ct):
        # Chuyển đổi ký tự thành giá trị 0-25
        c_val = ord(char) - ord('A')
        k_val = ord(k[i % len(k)]) - ord('A')
        
        # P = (C - K + 26) mod 26
        p_val = (c_val - k_val + 26) % 26
        plaintext.append(chr(p_val + ord('A')))
        
    return "".join(plaintext)

if __name__ == "__main__":
    print("--- CHƯƠNG TRÌNH MÃ HÓA/GIẢI MÃ VIGENÈRE ---")
    action = input("Bạn muốn Mã hóa (M) hay Giải mã (G)? ").strip().upper()
    
    if action == 'M':
        text = input("Nhập bản rõ (Plaintext): ")
        key = input("Nhập khóa (Key): ")
        print("\n[+] Bản rõ đã chuẩn hóa :", normalize_text(text))
        print("[+] Bản mã (Ciphertext):", vigenere_encrypt(text, key))
    elif action == 'G':
        text = input("Nhập bản mã (Ciphertext): ")
        key = input("Nhập khóa (Key): ")
        print("\n[+] Bản mã đã chuẩn hóa :", normalize_text(text))
        print("[+] Bản rõ (Plaintext)  :", vigenere_decrypt(text, key))
    else:
        print("Lựa chọn không hợp lệ.")