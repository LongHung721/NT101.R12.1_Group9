import random
import secrets

# Tinh luy thua module
def modularExponentiation(b, e, n):
    res = 1
    b = b % n
    while (e > 0):
        if (e & 1):
            res = (res * b) % n
        e = e>>1;
        b = (b*b) % n
    return res

# Kiem tra Miller-Rabin
def MillerRabin (n, d):
    a = random.randint(2, n-2)

    x = modularExponentiation(a, d, n)

    if (x == 1) or (x == n-1):
        return True

    while (d != n-1):
        x = (x*x) % n
        d *= 2
        if (x == 1): 
            return False
        if (x == n-1):
            return True
    return False

# Kiem tra so nguyen to su dung giai thuat Miller-Rabin
def isPrime (n, k):
    if ((n & 1) == 0):
        return False;
    d = n-1
    while ((d & 1) == 0):
        d >>= 1
    for i in range(k):
        if (MillerRabin(n, d) == False):
            return False
    return True

# Tao so nguyen to ngau nhien
def generate_prime(bits):
    while True:
        p = secrets.randbits(bits)
        
        p |= (1 << (bits - 1)) | 1
        
        if (isPrime(p, 2)):
            return p

# In cac so nguyen to lon nhat nho hon so nguyen to Mersenne thu 10
def printPrime():
    mersenne_10 = (2**89) - 1
    primes = []
    current = mersenne_10 - 1
    if (current % 2 == 0):
        current -= 1

    while len(primes) < 10:
        if (isPrime(current, 2)):
            primes.append(current)
        current -= 2  
    
    for index, prime in enumerate(primes, 1):
        print(f"{index}. {prime}")

# Tim uoc chung lon nhat gcd cua hai bang giai thuat Euclid mo rong
def extended_gcd(a, b):
  if b == 0:
    return a, 1, 0
  else:
    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd

print("CHON TAC VU CAN THUC HIEN")

print("1.Tao so nguyen to ngau nhien\n"
"2.Liet ke 10 so nguyen to lon nhat nho hon so nguyen to Mersenne thu 10\n"
"3.Kiem tra so nguyen to ngau nhien\n"
"4.Tim uoc chung lon nhat cua 2 so\n"
"5.Tinh luy thua module\n"
"-------------------------------------\n")

print("Nhap lua chon (so tuong ung): ")

lua_chon = input()

match lua_chon:
    case 1:
        print("Nhap so bit: ")
        bits = input()
        print(generate_prime(bits))
    case 2:
        printPrime()
    case 3:
        print("Nhap so can kiem tra: ")
        p = input()
        isPrime(p, 2)
    case 4:
        print("Nhap 2 so: ")
        a = input()
        b = input()
        print(extended_gcd(a, b))
    case 5:
        print("Nhap cac so theo thu tu x^y mod z\n")
        print("Nhap a=x: ")
        x = input()
        print("Nhap y: ")
        y = input()
        print("Nhap z: ")
        z = input()
