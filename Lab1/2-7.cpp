#include <iostream>
#include <string>
#include <cctype>
using namespace std;

const int M = 26;


int gcd(int a, int b) {
    return b == 0 ? a : gcd(b, a % b);
}

bool isValidA(int a) {
    return gcd(a, M) == 1;
}

int modInverse(int a, int m) {
    a = ((a % m) + m) % m;
    for (int x = 1; x < m; x++) {
        if ((a * x) % m == 1)
            return x;
    }
    return -1;
}

string affineEncrypt(string text, int a, int b) {
    string result = "";
    for (char ch : text) {
        if (isalpha(ch)) {
            bool isUpper = isupper(ch);
            int x = tolower(ch) - 'a';
            int enc = (a * x + b) % M;
            char c = enc + 'a';
            result += isUpper ? toupper(c) : c;
        } else {
            result += ch;
        }
    }
    return result;
}

string affineDecrypt(string text, int a, int b) {
    int aInv = modInverse(a, M);
    string result = "";
    for (char ch : text) {
        if (isalpha(ch)) {
            bool isUpper = isupper(ch);
            int y = tolower(ch) - 'a';
            int dec = (aInv * ((y - b + M) % M)) % M;
            char c = dec + 'a';
            result += isUpper ? toupper(c) : c;
        } else {
            result += ch;
        }
    }
    return result;
}

int main() {
    int choice, a, b;
    string text;

    cout << "===== Affine Cipher =====\n";
    cout << "1. Ma hoa\n";
    cout << "2. Giai ma\n";
    cout << "Chon: ";
    cin >> choice;
    cin.ignore();

    if ((choice != 1) && (choice != 2))
        cout << "Lua chon khong hop le. Vui long nhap lai!\n";

    do {
        cout << "Nhap he so a: ";
        cin >> a;
        if (!isValidA(a)) {
            cout << "a khong hop le. Vui long nhap lai!\n";
        }
    } while (!isValidA(a));

    cout << "Nhap he so b: ";
    cin >> b;
    cin.ignore();

    cout << "Nhap van ban:\n";
    getline(cin, text);

    string output;
    if (choice == 1) {
        output = affineEncrypt(text, a, b);
        cout << "\nVan ban da ma hoa:\n" << output << endl;
    } else if (choice == 2) {
        output = affineDecrypt(text, a, b);
        cout << "\nVan ban da giai ma:\n" << output << endl;
    }

    return 0;
}
