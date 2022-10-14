import requests

ss = requests.session()
ss.proxies = {'http': 'socks5h://localhost:9050'}

hdr={
    "Host":"xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "http://xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion/",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "81",
    "Origin": "http://xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion",
    "Authorization": "Basic YWRtaW46aGFtbWVydGltZQ==",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1"
}

secret = bytes.fromhex('ad8bb176da1f40a98385ad0ae9777c3208b78ae57a7fec84092b2cbbaf2ab1c0')

keepers = []
inters = []

flag=-1
for j in range(15,-1,-1):

    if flag ==-1 and j < 15:
        print(keepers)
        print(inters) 
        quit()

    # starting with 0
    plain = 15 - j 

    fillers = '!'*j
    prefix = str.encode(fillers)
    if flag != -1:
        keepers.append(flag)
        inter = flag ^ plain
        inters.append(inter)
        for i in range(plain):
            keepers[i] = inters[i] ^ (plain + 1)

    flag = -1
    for i in range(0,256):
        
        if flag != -1:
            break
        
        modified = prefix + i.to_bytes(1, 'little') 
        for jj in range(plain):
            modified = modified + keepers[len(keepers)-jj-1].to_bytes(1, 'little')

        modified = modified + secret[16:]
        trythese= modified.hex()
        print(i, trythese)
        while(1):
            try:
                ss = ss.post("http://xtfbiszfeilgi672ted7hmuq5v7v3zbitdrzvveg2qvtz4ar5jndnxad.onion/check_secret.html", headers=hdr, data={"secret": trythese}, timeout=10)
            except Exception as e:
                if "wrong" in str(e):
                    print(i, "is correctly padded")
                    print('\n')
                    flag = i
                if "timed out" not in str(e) and "Connection refused" not in str(e) and "closed connection" not in str(e):
                    break

# last intermediate
keepers.append(flag)
inter = flag ^ 16
inters.append(inter)

print(inters)

# what we get here
# inters = [51, 1, 15, 198, 126, 200, 230, 230, 218, 111, 100, 231, 49, 240, 199, 235]

# and to get the plaintext
res = ""
for i in range(0,16, 1):
    r = inters[15-i] ^ secret[i] 
    res += chr(r)

print(res)
# FLAG={/secet/x}