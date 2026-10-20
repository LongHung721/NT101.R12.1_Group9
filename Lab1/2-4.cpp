#include <iostream>
#include <string>
using namespace std;

const int SIZE = 5;

struct BangKhoa {
    char o[SIZE][SIZE];
    int hang[26];
    int cot[26];
};

string chuanHoa(const string& s) {
    string ketQua;

    for (char c : s) {
        if (c >= 'a' && c <= 'z')
            c = c - 'a' + 'A';

        if (c < 'A' || c > 'Z')
            continue;

        ketQua += (c == 'J') ? 'I' : c;
    }

    return ketQua;
}

BangKhoa taoBang(const string& khoa) {
    BangKhoa bang = {};
    bool daDung[26] = {};
    string nguon = chuanHoa(khoa) + "ABCDEFGHIKLMNOPQRSTUVWXYZ";
    int viTri = 0;

    for (char c : nguon) {
        int chiSo = c - 'A';

        if (daDung[chiSo])
            continue;

        int h = viTri / SIZE;
        int k = viTri % SIZE;

        bang.o[h][k] = c;
        bang.hang[chiSo] = h;
        bang.cot[chiSo] = k;
        daDung[chiSo] = true;
        viTri++;
    }

    return bang;
}

void inBang(const BangKhoa& bang) {
    for (int h = 0; h < SIZE; h++) {
        for (int c = 0; c < SIZE; c++)
            cout << bang.o[h][c] << ' ';
        cout << '\n';
    }
}

string chuanBiBanRo(const string& banRo) {
    string s = chuanHoa(banRo);
    string ketQua;
    size_t i = 0;

    while (i < s.size()) {
        char a = s[i];
        char b = (a == 'X') ? 'Q' : 'X';

        if (i + 1 < s.size() && a != s[i + 1]) {
            b = s[i + 1];
            i += 2;
        }
        else {
            i++;
        }

        ketQua += a;
        ketQua += b;
    }

    return ketQua;
}

string bienDoi(const string& s, const BangKhoa& bang, int buoc) {
    string ketQua;

    for (size_t i = 0; i < s.size(); i += 2) {
        int a = s[i] - 'A';
        int b = s[i + 1] - 'A';
        int h1 = bang.hang[a], c1 = bang.cot[a];
        int h2 = bang.hang[b], c2 = bang.cot[b];

        if (h1 == h2) {
            c1 = (c1 + buoc) % SIZE;
            c2 = (c2 + buoc) % SIZE;
        }
        else if (c1 == c2) {
            h1 = (h1 + buoc) % SIZE;
            h2 = (h2 + buoc) % SIZE;
        }
        else {
            int tam = c1;
            c1 = c2;
            c2 = tam;
        }

        ketQua += bang.o[h1][c1];
        ketQua += bang.o[h2][c2];
    }

    return ketQua;
}

string maHoa(const string& banRo, const BangKhoa& bang) {
    return bienDoi(chuanBiBanRo(banRo), bang, 1);
}

bool giaiMa(const string& banMa, const BangKhoa& bang, string& ketQua) {
    string s = chuanHoa(banMa);
    ketQua.clear();

    if (s.size() % 2 != 0)
        return false;

    ketQua = bienDoi(s, bang, SIZE - 1);
    return true;
}

int main() {
    string khoa;
    cout << "Nhap khoa : ";
    if (!getline(cin, khoa))
        return 0;

    BangKhoa bang = taoBang(khoa);
    cout << "\nBang khoa:\n";
    inBang(bang);

    while (true) {
        string luaChon, noiDung;
        cout << "\n1. Ma hoa\n2. Giai ma\n0. Thoat\nChon: ";

        if (!getline(cin, luaChon) || luaChon == "0")
            break;

        if (luaChon != "1" && luaChon != "2") {
            cout << "Lua chon khong hop le.\n";
            continue;
        }

        cout << "Nhap noi dung (chu cai khong dau): ";
        if (!getline(cin, noiDung))
            break;

        if (luaChon == "1") {
            cout << "Ban ro da chuan bi: "
                << chuanBiBanRo(noiDung) << '\n';

            cout << "Ban ma: " << maHoa(noiDung, bang) << '\n';
        }
        else {
            string ketQua;

            if (giaiMa(noiDung, bang, ketQua))
                cout << "Ban giai ma (giu ky tu dem): "
                << ketQua << '\n';
            else
                cout << "Loi: Ban ma phai co so chu cai chan.\n";
        }
    }

    return 0;
}