import hashlib

def verify_youtube_certificate(modulus_hex, exponent_int, signature_hex, body_bin_path):
    print("=" * 60)
    print("  XÁC MINH CHỮ KÝ SỐ X.509 TRANG CHỦ YOUTUBE.COM (RSA)")
    print("=" * 60)

    # 1. Chuyển đổi dữ liệu chuỗi Hex sang số nguyên (Integer)
    n = int(modulus_hex, 16)
    e = exponent_int
    S = int(signature_hex, 16)

    # 2. Giải mã chữ ký RSA theo công thức: EM = S^e mod n
    print("\n[*] Đang thực hiện tính toán RSA: EM = S^e mod n ...")
    EM_int = pow(S, e, n)

    # Chuyển số nguyên EM về mảng Byte theo độ dài của Modulus n
    key_len_bytes = (n.bit_length() + 7) // 8
    EM_bytes = EM_int.to_bytes(key_len_bytes, byteorder='big')

    print(f"[+] Encoded Message (EM) dạng Hex:\n{EM_bytes.hex()}\n")

    # 3. Trích xuất SHA-256 Hash từ cấu trúc PKCS#1 v1.5 Padding
    # SHA-256 Digest chiếm 32 bytes cuối cùng của khối EM
    extracted_hash = EM_bytes[-32:].hex()
    print(f"[*] Hash trích xuất từ chữ ký (Decrypted Hash): {extracted_hash}")

    # 4. Tính toán SHA-256 Hash trực tiếp từ phần thân c0_body.bin
    with open(body_bin_path, 'rb') as f:
        body_data = f.read()
    computed_hash = hashlib.sha256(body_data).hexdigest()
    print(f"[*] Hash tính toán từ c0_body.bin (Computed Hash):  {computed_hash}")

    # 5. Đánh giá và hiển thị kết quả xác minh
    print("\n" + "=" * 25 + " KẾT QUẢ " + "=" * 26)
    if extracted_hash.lower() == computed_hash.lower():
        print(" SUCCESS: Chữ ký HỢP LỆ! Chứng chỉ YouTube toàn vẹn và chính xác.")
    else:
        print(" FAILED: Chữ ký KHÔNG HỢP LỆ! Giá trị băm không trùng khớp.")
    print("=" * 60)

if __name__ == "__main__":

    CA_MODULUS_HEX = "A9FF9C7F451E70A8539FCAD9E50DDE4657577DBC8F9A5AAC46F1849ABB91DBC9FB2F01FB920900165EA01CF8C1ABF9782F4ACCD885A2D8593C0ED318FBB1F5240D26EEB65B64767C14C72F7ACEA84CB7F4D908FCDF87233520A8E269E28C4E3FB159FA60A21EB3C920531982CA36536D604DE90091FC768D5C080F0AC2DCF1736BC5136E0A4F7AC2F2021C2EB46383DA31F62D7530B2FBABC26EDBA9C00EB9F967D4C3255774EB05B4E98EB5DE28CDCC7A14E47103CB4D612E6157C519A90B98841AE87929D9B28D2FFF576A66E0CEAB95A82996637012671E3AE1DBB02171D77C9EFDAA176EFE2BFB381714D166A7AF9AB570CCC863813A8CC02AA97637CEE3"

    CA_EXPONENT = 65537

    CERT_SIGNATURE_HEX = "0494e7faf05b23713b3aa28ab6436089b37d55ef2efa941593a59ab22a720e665a38c8f0ae30c3735feeb1b8873959438be351fdade035788bbee2ddf2b16a466adb61857110c8acf27a34a73f22c81b74e7283ab7df9d61d052658bc2bce373cf3a231238fedc8e085b716330087bff7ca701d2dd5eae379327b9714aad8d60d335ccdf12129834f80adf02418b3114b1d6becb5729ddd2edb13e76aaab87c14dfd7da886870bf8b0c70f75777dddc89cef1e5f724b4caa029ecb2a890c25fa1b6ac3d4ba7ecb0752a00e502cfee4cb97325d8795cc63572c55aa3d0c70132026f80b85af7e0fdf1066e66bf5233faf063707ed834747bf76b043d2193ef051"

    BODY_FILE_PATH = r"D:\c0_body.bin"

    verify_youtube_certificate(CA_MODULUS_HEX, CA_EXPONENT, CERT_SIGNATURE_HEX, BODY_FILE_PATH)