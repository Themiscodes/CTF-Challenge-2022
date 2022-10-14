import hashlib
import os
import datetime

# starting from 2023 onwards
start=datetime.date(2023,1,1) 
for i in range(1000):
    
    # in RFC3339 format
    key= start.strftime('%Y-%m-%d')+" bigtent"

    # in SHA-256
    passphrase = hashlib.sha256(key.encode())

    # write in the file the passphrase
    f = open("passphrase.key", "w")
    f.write(passphrase.hexdigest())
    f.close()

    # $ gpg --symmetric --passphrase-file passphrase.key --batch plaintext.txt
    trythis = "gpg --passphrase-file passphrase.key --decrypt --batch firefox.log.gz.gpg"
    os.system(trythis)

    # get the one that succeeded
    print(passphrase.hexdigest())

    # use timedelta to reduce by a day
    start-= datetime.timedelta(days=1)