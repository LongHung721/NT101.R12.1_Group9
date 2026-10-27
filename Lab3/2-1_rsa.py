import base64
import binascii
import re
from math import gcd


# RSA
def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y


def modinv(e, phi):
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("e va phi(n) khong nguyen to cung nhau")
    return x % phi


def keygen(p, q, e):
    if p == q:
        raise ValueError("p va q phai phan biet")
    n = p * q
    phi = (p - 1) * (q - 1)
    if not (1 < e < phi):
        raise ValueError("can 1 < e < phi(n)")
    if gcd(e, phi) != 1:
        raise ValueError("gcd(e, phi(n)) != 1")
    d = modinv(e, phi)
    return {"p": p, "q": q, "n": n, "phi": phi, "PU": (e, n), "PR": (d, n)}


def rsa_op(m, key):                        
    k, n = key
    return pow(m, k, n)


# ma hoa / giai ma van ban
def block_sizes(n):
    plain = max(1, (n.bit_length() - 1) // 8)
    cipher = (n.bit_length() + 7) // 8
    return plain, cipher


def encrypt_text(text, key):
    n = key[1]
    pb, cb = block_sizes(n)
    data = text.encode()
    out = b""
    for i in range(0, len(data), pb):
        m = int.from_bytes(data[i:i + pb], "little")
        out += rsa_op(m, key).to_bytes(cb, "little")
    return out


def decrypt_bytes(cipher, key):
    n = key[1]
    _, cb = block_sizes(n)
    out = b""
    for i in range(0, len(cipher), cb):
        c = int.from_bytes(cipher[i:i + cb], "little")
        m = rsa_op(c, key)
        out += m.to_bytes((m.bit_length() + 7) // 8, "little")
    return out


def printable(b):
    return len(b) > 0 and all(32 <= x < 127 for x in b)


def bits_to_bytes(s):
    return bytes(int(s[i:i + 8], 2) for i in range(0, len(s) - len(s) % 8, 8))


def parse_cipher(s):
    """Tu nhan dang dinh dang: tra ve (ten_dinh_dang, [cac ung vien bytes])."""
    s = re.sub(r"\s+", "", s)
    if re.fullmatch(r"[01]+", s):
        if len(s) % 8 == 0:
            return "nhi phan", [bits_to_bytes(s)]
        # chuoi nhi phan sai do dai -> thu bo tung bit thua / thieu
        cands = [bits_to_bytes(s[:p] + s[p + 1:]) for p in range(len(s))] \
            if len(s) % 8 == 1 else [bits_to_bytes(s)]
        return "nhi phan (do dai khong chia het cho 8, thu bo 1 bit)", cands
    if re.fullmatch(r"[0-9A-Fa-f]+", s) and len(s) % 2 == 0:
        return "hex", [bytes.fromhex(s)]
    try:
        return "base64", [base64.b64decode(s, validate=True)]
    except (binascii.Error, ValueError):
        raise ValueError("khong nhan dang duoc dinh dang ban ma (Base64/Hex/Nhi phan)")


# nhap/xuat
def read_int(prompt, base):
    while True:
        s = input(prompt).strip().replace(" ", "")
        if s.lower().startswith("0x"):
            s, b = s[2:], 16
        else:
            b = base
        try:
            return int(s, b)
        except ValueError:
            print("  Gia tri khong hop le, nhap lai.")


def read_base():
    while True:
        s = input("He so cua p, q, e (10 = thap phan, 16 = thap luc phan) [10]: ").strip()
        if s in ("", "10"):
            return 10
        if s == "16":
            return 16
        print("  Chi nhan 10 hoac 16.")


def show_key(name, k):
    print(f"\n--- {name} ---")
    print(f"  p      = {k['p']}")
    print(f"  q      = {k['q']}")
    print(f"  n      = {k['n']}  (hex {k['n']:X}) [{k['n'].bit_length()} bit]")
    print(f"  phi(n) = {k['phi']}")
    print(f"  PU = (e, n) = ({k['PU'][0]}, {k['PU'][1]})")
    print(f"  PR = (d, n) = ({k['PR'][0]}, {k['PR'][1]})")
    print(f"  e (hex) = {k['PU'][0]:X}   d (hex) = {k['PR'][0]:X}")


def choose_key(keys):
    if not keys:
        print("Chua co khoa nao. Hay dung muc 1 de nhap khoa.")
        return None
    names = list(keys)
    for i, nm in enumerate(names, 1):
        print(f"  [{i}] {nm}")
    while True:
        s = input(f"Chon khoa (1-{len(names)}) [{len(names)}]: ").strip()
        if s == "":
            return keys[names[-1]]
        if s.isdigit() and 1 <= int(s) <= len(names):
            return keys[names[int(s) - 1]]
        print("  Lua chon khong hop le.")


# menu
def action_enter_key(keys):
    base = read_base()
    p = read_int("p = ", base)
    q = read_int("q = ", base)
    e = read_int("e = ", base)
    try:
        k = keygen(p, q, e)
    except ValueError as ex:
        print("Loi:", ex)
        return
    name = f"Khoa {len(keys) + 1}"
    keys[name] = k
    show_key(name, k)


def action_test_number(keys):
    k = choose_key(keys)
    if not k:
        return
    s = input("Ban ro M (so nguyen, 0 <= M < n): ").strip()
    try:
        m = int(s)
    except ValueError:
        print("M khong hop le.")
        return
    if not 0 <= m < k["n"]:
        print("M phai nam trong [0, n-1].")
        return
    PU, PR = k["PU"], k["PR"]
    c = rsa_op(m, PU)
    print(f"Bao mat  : C = M^e mod n = {c}")
    print(f"           M = C^d mod n = {rsa_op(c, PR)}")
    c = rsa_op(m, PR)
    print(f"Xac thuc : C = M^d mod n = {c}")
    print(f"           M = C^e mod n = {rsa_op(c, PU)}")


def action_encrypt_text(keys):
    k = choose_key(keys)
    if not k:
        return
    text = input("Thong diep can ma hoa: ")
    try:
        c = encrypt_text(text, k["PU"])
    except UnicodeError:
        print("Loi ma hoa van ban.")
        return
    print("Ban ma (Base64):", base64.b64encode(c).decode())
    print("Ban ma (Hex)   :", c.hex().upper())
    assert decrypt_bytes(c, k["PR"]).decode() == text


def action_decrypt(keys):
    if not keys:
        print("Chua co khoa nao. Hay dung muc 1 de nhap khoa.")
        return
    s = input("Ban ma (Base64 / Hex / chuoi nhi phan): ")
    try:
        fmt, cands = parse_cipher(s)
    except ValueError as ex:
        print("Loi:", ex)
        return
    print("Dinh dang nhan dang:", fmt)
    for c in cands:
        for name, k in keys.items():
            try:
                pt = decrypt_bytes(c, k["PR"])
            except Exception:
                continue
            if printable(pt) and len(pt) >= 4:
                print(f"Giai ma thanh cong bang {name}:")
                print(f'  Ban ro: "{pt.decode()}"')
                return
    print("Khong giai ma ra van ban doc duoc voi cac khoa hien co.")


MENU = """
================ RSA - Nhiem vu 2.1 ================
 1. Nhap khoa moi (p, q, e) -> tinh n, phi(n), PU, PR
 2. Thu ma hoa/giai ma so M (bao mat + xac thuc)
 3. Ma hoa thong diep van ban -> Base64
 4. Giai ma ban ma (Base64 / Hex / nhi phan)
 5. Xem cac khoa hien co
 0. Thoat
"""


def main():
    keys = {}
    actions = {"1": action_enter_key, "2": action_test_number,
               "3": action_encrypt_text, "4": action_decrypt}
    while True:
        print(MENU)
        try:
            ch = input("Chon: ").strip()
        except EOFError:
            break
        if ch == "0":
            break
        try:
            if ch == "5":
                if not keys:
                    print("Chua co khoa nao.")
                for nm, k in keys.items():
                    show_key(nm, k)
            elif ch in actions:
                actions[ch](keys)
            else:
                print("Lua chon khong hop le.")
        except EOFError:
            break


if __name__ == "__main__":
    main()