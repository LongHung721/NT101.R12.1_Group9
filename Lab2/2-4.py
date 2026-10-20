
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Buoc 1: Tao du lieu 1000 byte
plaintext = get_random_bytes(1000)

print("Do dai du lieu ban dau:", len(plaintext), "bytes")

# Tao khoa AES-128 (128 bit = 16 bytes)
key = get_random_bytes(16)

# Tao IV cho cac che do can IV
iv = get_random_bytes(16)

# Buoc 2: Ma hoa du lieu bang AES-128

# ECB: AES yeu cau du lieu chia het cho 16 byte
# Nen can them padding cho 1000 byte
from Crypto.Util.Padding import pad

cipher_ecb = AES.new(key, AES.MODE_ECB)
ciphertext_ecb = cipher_ecb.encrypt(pad(plaintext, AES.block_size))

# CBC: can IV va padding
cipher_cbc = AES.new(key, AES.MODE_CBC, iv=iv)
ciphertext_cbc = cipher_cbc.encrypt(pad(plaintext, AES.block_size))

# CFB: khong can padding
cipher_cfb = AES.new(key, AES.MODE_CFB, iv=iv, segment_size=128)
ciphertext_cfb = cipher_cfb.encrypt(plaintext)

# OFB: khong can padding
cipher_ofb = AES.new(key, AES.MODE_OFB, iv=iv)
ciphertext_ofb = cipher_ofb.encrypt(plaintext)

print("Do dai ban ma ECB:", len(ciphertext_ecb), "bytes")
print("Do dai ban ma CBC:", len(ciphertext_cbc), "bytes")
print("Do dai ban ma CFB:", len(ciphertext_cfb), "bytes")
print("Do dai ban ma OFB:", len(ciphertext_ofb), "bytes")
# Buoc 3: Dao 1 bit tai byte thu 26 cua moi ban ma

def dao_bit_byte_26(ciphertext):
    ban_ma_loi = bytearray(ciphertext)
    ban_ma_loi[25] ^= 0x01

    return bytes(ban_ma_loi)


ciphertext_ecb_loi = dao_bit_byte_26(ciphertext_ecb)
ciphertext_cbc_loi = dao_bit_byte_26(ciphertext_cbc)
ciphertext_cfb_loi = dao_bit_byte_26(ciphertext_cfb)
ciphertext_ofb_loi = dao_bit_byte_26(ciphertext_ofb)


# Buoc 4: Giai ma ban ma loi va dem cac khoi ban ro bi hong

from Crypto.Util.Padding import unpad

# Tao doi tuong giai ma moi, dung dung key va IV ban dau.

# ECB: giai ma va loai bo padding
decrypt_ecb = AES.new(key, AES.MODE_ECB)
plaintext_ecb_loi = unpad(
    decrypt_ecb.decrypt(ciphertext_ecb_loi),
    AES.block_size
)

# CBC: giai ma va loai bo padding
decrypt_cbc = AES.new(key, AES.MODE_CBC, iv=iv)
plaintext_cbc_loi = unpad(
    decrypt_cbc.decrypt(ciphertext_cbc_loi),
    AES.block_size
)

# CFB: giu segment_size=128 nhu khi ma hoa
decrypt_cfb = AES.new(
    key, AES.MODE_CFB, iv=iv, segment_size=128
)
plaintext_cfb_loi = decrypt_cfb.decrypt(ciphertext_cfb_loi)

# OFB: khong can loai bo padding
decrypt_ofb = AES.new(key, AES.MODE_OFB, iv=iv)
plaintext_ofb_loi = decrypt_ofb.decrypt(ciphertext_ofb_loi)


def thong_ke_loi(ten_che_do, ban_ro_loi):
    khoi_loi = []
    vi_tri_byte_loi = []
    so_bit_loi = 0

    # So sanh tung khoi 16 byte voi ban ro goc.
    for i in range(0, len(plaintext), AES.block_size):
        khoi_goc = plaintext[i:i + AES.block_size]
        khoi_giai_ma = ban_ro_loi[i:i + AES.block_size]

        if khoi_goc != khoi_giai_ma:
            khoi_loi.append(i // AES.block_size + 1)

    # Dem so byte va so bit khac nhau.
    for i in range(len(plaintext)):
        if plaintext[i] != ban_ro_loi[i]:
            vi_tri_byte_loi.append(i + 1)

        so_bit_loi += bin(
            plaintext[i] ^ ban_ro_loi[i]
        ).count("1")

    print("\nChe do:", ten_che_do)
    print("So khoi bi loi:", len(khoi_loi))
    print("Cac khoi bi loi:", khoi_loi)
    print("So byte bi loi:", len(vi_tri_byte_loi))
    print("Vi tri byte bi loi (dem tu 1):", vi_tri_byte_loi)
    print("So bit bi loi:", so_bit_loi)


thong_ke_loi("ECB", plaintext_ecb_loi)
thong_ke_loi("CBC", plaintext_cbc_loi)
thong_ke_loi("CFB-128", plaintext_cfb_loi)
thong_ke_loi("OFB", plaintext_ofb_loi)
