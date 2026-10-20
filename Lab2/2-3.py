from Crypto.Cipher import DES

def bytes_to_bin_str(data):
    return bin(int.from_bytes(data, 'big'))[2:].zfill(64)

def avalanche_test(key):
    p1 = b'STAYHOME'
    p2 = b'STAYHOMA'
    
    # TODO: Thực hiện mã hóa p1, p2 bằng DES-ECB
    cipher = DES.new(key, DES.MODE_ECB)
    c1 = cipher.encrypt(p1)
    c2 = cipher.encrypt(p2)
    
    # Chuyển bản mã sang chuỗi nhị phân
    bin_c1 = bytes_to_bin_str(c1)
    bin_c2 = bytes_to_bin_str(c2)
    
    # TODO: Đếm số bit khác nhau giữa hai bản mã thu được
    hamming_distance = sum(b1 != b2 for b1, b2 in zip(bin_c1, bin_c2))
    
    # TODO: Tính tỷ lệ % bit bị thay đổi
    total_bits = len(bin_c1)
    percentage = (hamming_distance / total_bits) * 100
    
    # In kết quả
    print(f"Key được sử dụng    : {key}")
    print(f"Bản mã 1 (nhị phân) : {bin_c1}")
    print(f"Bản mã 2 (nhị phân) : {bin_c2}")
    print(f"Hamming Distance    : {hamming_distance} bits")
    print(f"Tỷ lệ thay đổi      : {percentage:.2f}%\n")
    print("-" * 60 + "\n")

if __name__ == "__main__":
    p1_bin = bytes_to_bin_str(b'STAYHOME')
    p2_bin = bytes_to_bin_str(b'STAYHOMA')
    print(f"Bản rõ 1 (p1)       : {p1_bin}")
    print(f"Bản rõ 2 (p2)       : {p2_bin}")
    print("=" * 60 + "\n")

    mssv_keys = [
        b'24521454',
        b'24520611',
        b'24520055'
    ]
    
    for mssv in mssv_keys:
        avalanche_test(mssv)