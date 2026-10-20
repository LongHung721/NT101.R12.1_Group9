import re
import math
from collections import Counter, defaultdict


# ============================================================
# 1. CHUẨN HÓA CIPHERTEXT
# ============================================================

def normalize_text(text):
    return ''.join(
        c.lower()
        for c in text
        if c.isalpha() and c.isascii()
    )


# ============================================================
# 2. INDEX OF COINCIDENCE
# ============================================================

def index_of_coincidence(text):

    n = len(text)

    if n <= 1:
        return 0.0

    counter = Counter(text)

    numerator = sum(
        f * (f - 1)
        for f in counter.values()
    )

    denominator = n * (n - 1)

    return numerator / denominator


# ============================================================
# 3. IC TRUNG BÌNH CHO MỘT KEY LENGTH
# ============================================================

def average_ic(text, key_length):

    columns = []

    for i in range(key_length):
        column = text[i::key_length]
        columns.append(column)

    ic_values = [
        index_of_coincidence(column)
        for column in columns
    ]

    return sum(ic_values) / len(ic_values)


# ============================================================
# 4. TÌM KEY LENGTH BẰNG IC
# ============================================================

def find_key_lengths(text, max_key_length=20):
    results = []

    for key_length in range(1, max_key_length + 1):

        ic = average_ic(text, key_length)

        results.append(
            (key_length, ic)
        )

    # IC cao -> khả năng là key length tốt
    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results


# ============================================================
# 5. KASISKI EXAMINATION
# ============================================================

def kasiski_examination(text, min_length=3, max_length=5):

    distances = []

    for seq_length in range(
        min_length,
        max_length + 1
    ):

        positions = defaultdict(list)

        for i in range(
            len(text) - seq_length + 1
        ):

            sequence = text[
                i:i + seq_length
            ]

            positions[sequence].append(i)

        # Chỉ xét sequence xuất hiện >= 2 lần
        for sequence, pos_list in positions.items():

            if len(pos_list) < 2:
                continue

            for i in range(len(pos_list)):

                for j in range(
                    i + 1,
                    len(pos_list)
                ):

                    distance = (
                        pos_list[j] -
                        pos_list[i]
                    )

                    distances.append(
                        (sequence, distance)
                    )

    return distances


def kasiski_key_length_scores(
    text,
    max_key_length=20
):

    distances = kasiski_examination(text)

    scores = Counter()

    for sequence, distance in distances:

        for key_length in range(
            1,
            max_key_length + 1
        ):

            if distance % key_length == 0:
                scores[key_length] += 1

    return scores


# ============================================================
# 6. ENGLISH FREQUENCY
# ============================================================

ENGLISH_FREQUENCY = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074
}


# ============================================================
# 7. CHI-SQUARE
# ============================================================

def chi_square(column, shift):

    n = len(column)

    if n == 0:
        return float('inf')

    observed = [0] * 26

    for char in column:

        index = (
            ord(char) - ord('a') - shift
        ) % 26

        observed[index] += 1

    score = 0.0

    for i in range(26):

        letter = chr(
            ord('a') + i
        )

        expected = (
            ENGLISH_FREQUENCY[letter]
            * n
        )

        if expected > 0:

            score += (
                (observed[i] - expected) ** 2
                / expected
            )

    return score


# ============================================================
# 8. TÌM KÝ TỰ KHÓA
# ============================================================

def find_best_key_char(column):
    """
    Thử toàn bộ 26 khả năng của một ký tự khóa.
    """

    best_shift = 0
    best_score = float('inf')

    for shift in range(26):

        score = chi_square(
            column,
            shift
        )

        if score < best_score:

            best_score = score
            best_shift = shift

    return chr(
        ord('a') + best_shift
    )


# ============================================================
# 9. TÌM TOÀN BỘ KEY
# ============================================================

def find_key(ciphertext, key_length):

    key = ""

    for i in range(key_length):

        column = ciphertext[i::key_length]

        key_char = find_best_key_char(
            column
        )

        key += key_char

    return key


# ============================================================
# 10. GIẢI MÃ VIGENERE
# ============================================================

def decrypt_vigenere(
    ciphertext,
    key
):

    plaintext = []

    key_index = 0

    for char in ciphertext:

        if char.isalpha():

            c = (
                ord(char.lower())
                - ord('a')
            )

            k = (
                ord(
                    key[
                        key_index % len(key)
                    ]
                )
                - ord('a')
            )

            p = (
                c - k
            ) % 26

            plaintext.append(
                chr(
                    ord('a') + p
                )
            )

            key_index += 1

        else:

            plaintext.append(char)

    return ''.join(plaintext)


# ============================================================
# 11. ENGLISH PLAINTEXT SCORE
# ============================================================

COMMON_NGRAMS = {

    "the": 5,
    "and": 4,
    "ing": 4,
    "ion": 3,
    "that": 5,
    "this": 5,
    "with": 4,
    "from": 4,
    "have": 4,
    "were": 4,
    "they": 4,
    "which": 4,
    "tion": 4,
    "ment": 3,
    "crypt": 3,
    "data": 3,
    "computer": 6,
    "science": 6,
    "information": 6,
    "security": 5,
    "communication": 5,
    "algorithm": 5
}


def english_score(text):

    text = text.lower()

    score = 0

    for ngram, weight in COMMON_NGRAMS.items():

        count = text.count(ngram)

        score += count * weight

    return score


# ============================================================
# 12. RÚT GỌN KEY NẾU KEY BỊ LẶP
# ============================================================

def reduce_repeated_key(key):

    n = len(key)

    for length in range(
        1,
        n + 1
    ):

        if n % length != 0:
            continue

        candidate = key[:length]

        repeated = (
            candidate *
            (n // length)
        )

        if repeated == key:

            return candidate

    return key


# ============================================================
# 13. CHỌN KEY TỐT NHẤT
# ============================================================

def crack_vigenere(
    ciphertext,
    max_key_length=20,
    top_n=8
):

    print("\n[+] Phân tích IC...\n")

    ic_results = find_key_lengths(
        ciphertext,
        max_key_length
    )

    print(
        f"{'Length':<10}"
        f"{'Average IC':<15}"
    )

    print("-" * 25)

    for length, ic in ic_results:

        print(
            f"{length:<10}"
            f"{ic:.5f}"
        )

    candidate_lengths = [
        length
        for length, ic
        in ic_results[:top_n]
    ]

    print(
        "\n[+] Các độ dài khóa được thử:",
        candidate_lengths
    )

    candidates = []

    for key_length in candidate_lengths:

        key = find_key(
            ciphertext,
            key_length
        )

        plaintext = decrypt_vigenere(
            ciphertext,
            key
        )

        score = english_score(
            plaintext
        )

        candidates.append(
            (
                score,
                key_length,
                key,
                plaintext
            )
        )

    candidates.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return candidates


# ============================================================
# 14. INPUT TỪ FILE
# ============================================================

def read_file(filename):

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# 15. MAIN
# ============================================================

def main():

    print("=" * 60)
    print("          VIGENERE CIPHER CRACKER")
    print("=" * 60)

    print("\n1. Nhập ciphertext")
    print("2. Đọc ciphertext từ file")

    choice = input(
        "\nLựa chọn: "
    )

    if choice == "1":

        print(
            "\nNhập ciphertext."
        )

        print(
            "Nhấn Enter 2 lần để kết thúc:"
        )

        lines = []

        while True:

            line = input()

            if line == "":
                break

            lines.append(line)

        original_text = "\n".join(
            lines
        )

    elif choice == "2":

        filename = input(
            "\nTên file: "
        )

        original_text = read_file(
            filename
        )

    else:

        print(
            "Lựa chọn không hợp lệ!"
        )

        return

    # --------------------------------------------------------
    # Normalize
    # --------------------------------------------------------

    ciphertext = normalize_text(
        original_text
    )

    print(
        "\n[+] Ciphertext sau khi chuẩn hóa:"
    )

    print(
        ciphertext[:100] + "..."
    )

    print(
        f"\n[+] Số ký tự: "
        f"{len(ciphertext)}"
    )

    # --------------------------------------------------------
    # Kasiski
    # --------------------------------------------------------

    print(
        "\n[+] Thực hiện Kasiski Examination..."
    )

    kasiski_scores = (
        kasiski_key_length_scores(
            ciphertext
        )
    )

    print(
        "\nCác key length có điểm Kasiski cao:"
    )

    for length, score in sorted(
        kasiski_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]:

        print(
            f"Length {length:2d}"
            f" -> {score} hits"
        )

    # --------------------------------------------------------
    # Crack
    # --------------------------------------------------------

    candidates = crack_vigenere(
        ciphertext,
        max_key_length=20,
        top_n=8
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    print(
        "\n" + "=" * 60
    )

    print(
        "                 KẾT QUẢ"
    )

    print(
        "=" * 60
    )

    for i, candidate in enumerate(
        candidates[:5],
        start=1
    ):

        score, key_length, key, plaintext = candidate

        reduced_key = (
            reduce_repeated_key(key)
        )

        if reduced_key != key:

            plaintext = decrypt_vigenere(
                original_text,
                reduced_key
            )

        print(
            f"\n--- Candidate {i} ---"
        )

        print(
            f"Key length : {key_length}"
        )

        print(
            f"Key        : {reduced_key.upper()}"
        )

        print(
            f"Score      : {score}"
        )

        print(
            f"Plaintext  :\n"
            f"{plaintext[:500]}"
        )

    # --------------------------------------------------------
    # Best result
    # --------------------------------------------------------

    best = candidates[0]

    score, key_length, key, plaintext = best

    key = reduce_repeated_key(key)

    plaintext = decrypt_vigenere(
        original_text,
        key
    )

    print(
        "\n" + "=" * 60
    )

    print(
        "              BEST RESULT"
    )

    print(
        "=" * 60
    )

    print(
        f"\nKhóa          : {key.upper()}"
    )

    print(
        f"Độ dài khóa   : {len(key)}"
    )

    print(
        f"Score         : {score}"
    )

    print(
        "\nBẢN RÕ:\n"
    )

    print(plaintext)

    print(
        "\n" + "=" * 60
    )


if __name__ == "__main__":
    main()