# Rought "notebook" from when I was working with ECB exploitation

import base64

token1 = "7z+Gu21W2Yi91LAZ1eB8zQ=="
token2 = "TnOY1nO3amROc5jWc7dqZE5zmNZzt2pkTnOY1nO3amROc5jWc7dqZAlrgRZJ9QdHTnOY1nO3amROc5jWc7dqZE5zmNZzt2pkTnOY1nO3amROc5jWc7dqZHF6B2HRRFYg"
token3 = "TnOY1nO3amROc5jWc7dqZE5zmNZzt2pkTnOY1nO3amROc5jWc7dqZD6CT4s+CkkATnOY1nO3amROc5jWc7dqZE5zmNZzt2pkTnOY1nO3amTGOnsxlTDmlTIknlbv8qFO"

d1Token = base64.b64decode(token1)
d2Token = base64.b64decode(token2)
d3Token = base64.b64decode(token3)

print(d1Token)
print(d2Token)
print(d3Token)
#  d2 token analysis
# Ns\x98\xd6s\xb7jd <-- repeats just like our "A" * 45
# Ns\x98\xd6s\xb7jd <-- 8 bytes in total i.e our block-size is of 8 bytes chunks
# Ns\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jd <-- first part (username||pass)
# \tk\x81\x16I\xf5\x07G <-- second part
# Ns\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jd <-- third part (password||user)
# qz\x07a\xd1DV <-- fourth part

# d3 token analysis
# >\x82O\x8b>\nI\x00Ns\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jd\xc6:{1\x950\xe6\x952$\x9eV\xef\xf2\xa1N

# [username][delimiter][password]
# 8 bytes    8 bytes    8 bytes

exx = "A" * 40 + "admin"
# print(exx)

# ECB -> [Message] == x bytes chunks ==> [msg1] + [msg2] + [msg3] + ... [msgN]
# then all these chunks are encrypted by a "key"

# we removed extra "A" from "A" * 40 + "admin" by looking at the pattern to only get "admin" as username in the first block
# This was by method of removal of information as an ECB attack
d3Modified = b">\x82O\x8b>\nI\x00Ns\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jdNs\x98\xd6s\xb7jd\xc6:{1\x950\xe6\x952$\x9eV\xef\xf2\xa1N"
# print(base64.b64encode(d3Modified))

# By the method of swapping blocks
# we figured out that our delimiter is of 1 byte
# [username][delimiter][password]
# 8 bytes    8 bytes     8 bytes ( since block mode is of 8 bytes as figured earlier)
# username="password" -> 8 bytes
# delimiter is of 1 byte
# password="admin" -> 5 bytes
# we want our username (when swapped) to be "admin   " with 3 spaces (3 bytes) (assuming sql issue in the app)

token4 = "wY0hY1GwdbHrvmiLk8NRUQgFu0hUEA/9"
d4Token = base64.b64decode(token4)
print(d4Token)

# \x08\x05\xbbHT\x10\x0f\xfd <-- our "admin   "
# \xc1\x8d!cQ\xb0u\xb1 <-- password with 7 spaces + 1 left for delimiter
# total 8,8,8 block chunks or 24 bytes

swapToken = b"\x08\x05\xbbHT\x10\x0f\xfd\xeb\xbeh\x8b\x93\xc3QQ\xc1\x8d!cQ\xb0u\xb1"
print(base64.b64encode(swapToken))
