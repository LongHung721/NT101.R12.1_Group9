#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <cctype>
#include <algorithm>

using namespace std;

string encryptCaesar(const string& text, int shift) {
    string result = text;

    shift = ((shift % 26) + 26) % 26;

    for (char& c : result) {
        if (c >= 'A' && c <= 'Z') {
            c = char((c - 'A' + shift) % 26 + 'A');
        }
        else if (c >= 'a' && c <= 'z') {
            c = char((c - 'a' + shift) % 26 + 'a');
        }
    }

    return result;
}

string decryptCaesar(const string& text, int shift) {
    return encryptCaesar(text, -shift);
}

double calculateScore(const string& text) {

    vector<string> commonWords = {
        "the", "and", "that", "this", "with",
        "from", "have", "for", "not", "are",
        "was", "were", "you", "your", "they",
        "their", "what", "which", "when", "where",
        "will", "would", "there", "about", "could",
        "should", "into", "more", "than", "then",
        "them", "some", "these", "people", "time",
        "only", "very", "just", "know", "like",
        "good", "because", "make", "also", "can"
    };

    const double frequency[26] = {
        8.167, 1.492, 2.782, 4.253, 12.702,
        2.228, 2.015, 6.094, 6.966, 0.153,
        0.772, 4.025, 2.406, 6.749, 7.507,
        1.929, 0.095, 5.987, 6.327, 9.056,
        2.758, 0.978, 2.360, 0.150, 1.974,
        0.074
    };

    double score = 0.0;

    string lowerText;

    for (char c : text) {
        lowerText += tolower(static_cast<unsigned char>(c));
    }

    stringstream ss(lowerText);
    string word;

    while (ss >> word) {

        string cleanWord;

        for (char c : word) {
            if (isalpha(static_cast<unsigned char>(c))) {
                cleanWord += c;
            }
        }

        for (const string& common : commonWords) {
            if (cleanWord == common) {
                score += 10.0;
            }
        }
    }

    int letterCount[26] = {0};
    int totalLetters = 0;

    for (char c : text) {

        if (isalpha(static_cast<unsigned char>(c))) {

            c = tolower(static_cast<unsigned char>(c));

            letterCount[c - 'a']++;
            totalLetters++;
        }
    }

    if (totalLetters > 0) {

        for (int i = 0; i < 26; i++) {

            double actualFrequency =
                (double)letterCount[i] / totalLetters * 100.0;

            double difference =
                actualFrequency - frequency[i];

            score -= difference * difference * 0.01;
        }
    }

    vector<string> commonPairs = {
        "th", "he", "in", "er", "an",
        "re", "on", "at", "en", "nd",
        "ti", "es", "or", "te", "of",
        "ed", "is", "it", "al", "ar"
    };

    for (const string& pair : commonPairs) {

        size_t position = 0;

        while ((position = lowerText.find(pair, position))
               != string::npos) {

            score += 1.0;
            position += 1;
        }
    }

    return score;
}

void bruteForce(const string& ciphertext) {

    int bestShift = 0;
    double bestScore = -1e9;
    string bestPlaintext;

    for (int shift = 0; shift < 26; shift++) {

        string plaintext = decryptCaesar(ciphertext, shift);

        double score = calculateScore(plaintext);

        if (score > bestScore) {

            bestScore = score;
            bestShift = shift;
            bestPlaintext = plaintext;
        }
    }

    cout << "Plaintext co diem cao nhat: " << endl;

    cout << "Khoa : " << bestShift << endl;
    cout << "Diem : " << bestScore << endl;

    cout << "Van ban: " << endl;
    cout << bestPlaintext << endl;
}


int main() {

    string paragraph;
    int shift;

    cout << "Nhap van ban ro: " << endl;
    getline(cin, paragraph);

    cout << "Nhap khoa (0-25): ";
    cin >> shift;

    shift = ((shift % 26) + 26) % 26;

    string ciphertext =
        encryptCaesar(paragraph, shift);

    cout << "Van ban da ma hoa: " << endl;

    cout << "Khoa: " << shift << endl;

    cout << ciphertext << endl;

    string cipherparagraph;

    cout << "Nhap ciphertext: " << endl;
    cin.ignore();
    getline(cin, cipherparagraph);

    bruteForce(cipherparagraph);

    return 0;
}
