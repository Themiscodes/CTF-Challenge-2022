# CTF Computer Security Challenge 2022

The purpose of this competition was to learn the basic techniques of vulnerability assessment, cryptography and exploitation in six security challenges of increasing difficulty. Among the methods used were file forensics, breaking encryption schemes such as RSA, AES and Shamir's Secret Sharing and binary exploitation through buffer overflow attacks.

The code of each solution can be found in the corresponding folder and a detailed report can be found below. This was a team challenge introduced as an assignment for the YS13 Computer Security course of Spring 2022 and was completed in collaboration with [Giannis Dravilas](https://github.com/giannisdravilas).
 
 ![encryption](https://user-images.githubusercontent.com/73662635/195792353-355df31b-7b88-409c-8dfa-8bb3d348d99b.png)
 
## Writeup

### 1. Where is George?

- Initially, inspecting the web source of the onion page that was given, we found a link to a blog. Among other things it mentioned that the server-info page should be hidden. By connecting on the page we found another link, where using the information in the server-info (i.e. that it is in phps format) we added the extension `/access.phps`.

- On this page there was a simple problem that we solved in [riddle1.py]() and the output was: 1337. This, however, was not accepted, so we converted it to 0001337 since it should be of length 7 characters. On the url we also added to bypass the password check a simple array so that in that way `strcmp()` would return 0.

- This way, we succesfully connected and the next part was revealed, namely the directory: `/blogposts7589109238`. Among the links in that page there was a diary with the following message: `Giorgos Komninos winner visitor# 834472`.

- Going back to the home page we noticed that the visitor number did not change per session, so it would depend on the cookie of each user. Using **cyberchef** we decoded from base 64 and saw that the first part showed 204 and the second a hash: `204:fc56dbc6d4652b315b86b71c8d688c1ccdea9c5f1fd07763d2659fde2e2fc49a`

- Running the second part through a hash analyzer we saw that it would either be of the md or sha family. So after testing with reverse decode we realized it was sha256 and that 204 hashes to it. Thus, to create George's cookie we did the corresponding format for 834472 in reverse and then in combination as was the format in base64.

- By changing the page cookie from the console we got the hint: `Check directory /sekritbackup7547`. So we were directed to this onion page and in the file `notes.txt` there was information about ropsten blockchain. Going in this site and changing the input data to UTF8 we got: `bigtent`. There was also a description of the passphrase used:
`key = SHA256(date in RFC3339 format> + "" + string>)`

- To find the date we wrote [riddle2.py](), where we tried all possible dates backwards, starting from 2023. Converting it to `sha256`, we tested with every time whether it is possible to decode to gpg. So in the end we managed to find the combination in [passphrase.key]() and using it we managed to decrypt gpg.

- In the `signal.txt` file there was a subtle hint that the information was a git commit. While in `firefox.log` there was the same link several times. Opening wikipedia and reading the contents we didn't find anything interesting. To find out if there was anything else in the `firefox.log` file besides this link, we wrote the bash script, [riddle3.sh](), which just reads each line and if there is anything aside from that it prints it. 

- After a while it printed another link, which we combined with the commit from the previous message to get a github repository. There, it was obvious from the description and variable names that the problem was referring to the RSA cryptosystem.

- So to reverse engineer it, in [riddle4.py]() we first found p and q and then phi. From there we were able to produce x and y, from which the corresponding Ex kai Ey were produced. By concatenating the link, we were directed to a page, where the first flag was displayed:

```
FLAG={GilmansPointKilimanjaro}
```

### 2. What did George find?

- On the page where we found the flag of the previous question there was a link at the end for an image `kilimanjarotimes4818.jpg`. Following the link, we found the excerpt from a newspaper, in the text of which it had comments about baseline and version control, which we understood to be some hint for the problem we had to solve. There was also the reference to a `tar.gz` file, which we added to the onion link to download it.

- Initially, trying to decompress it, we got the message that the file is corrupted. Changing it to `.txt` and doing cat we saw that at the beginning it had the message: `pleaseletmesleeep`. From this we concluded that the correct header was missing. So, looking at https://en.wikipedia.org/wiki/List_of_file_signatures for the magic bytes of `tar.gz` files, we saw that these are: `1F 8B`.

- Looking at the hex with the command `xdd` we saw that these bytes were in the 32nd and 33rd bytes of the file. So, with [riddle1.sh](), we managed to remove the "bad bytes" using `dd`. The file could then be decompressed normally and the `/sss` directory appeared.

- Inside there was a `.git` folder. Since it was a repository without files, we first tried to see the information it had in HEAD and logs and then objects. To see what all the objects contained, we wrote the script [riddle2.sh]() which recursively parses all the subfolders, and concatenates the folder name with the first 4 digits of the file, to get the commit.

- This way, we located the files `polywork.py` and `sss.py`, which we found useful in understanding that the cryptography is done with **Shamir's Secret Sharing** algorithm. We then adjusted the script with `grep` to see if the seed exists and found it in one of the files.

- Then, to find the shares we adjusted the script again with grep with the `shares` keyword and three files were located, which had three shares each. To generate the secret from them, we saw the code of `polywork.py` where it was a degree 2 polynomial and we noticed that only the first share was enough, since we could generate the coefficients through the seed.

- Thus, using the first share we wrote the first Lagrange equation, i.e. for x = 1, solving for the unknown share[0]. The code can be found in [riddle3.py](). This way, we got the two flags:

```
FLAG={RahulKhandelwal}
FLAG={TimeTravelPossible!!?}
```

### 3. What time is it on "Plan X"?

- In the second diary entry there was a form asking for a username and password to log in. First, we tried as username admin and for password the flags we had found before, without success. There was also a mention of a pico server, the code of which was in: https://github.com/chatziko/pico. 

- Downloading and following the instructions on how to set it up, we made the necessary changes on our system and installed the required libraries. When we tried to run make, although the compilation was successful, a warning appeared for the command `printf(auth_username);`, which made it vulnerable to a string format attack.

- Also, examining the code on the function `check_auth()` we saw that this can happen by keeping the password null. As is described in: https://ctf101.org/binary-exploitation/what-is-a-format-string-vulnerability in order to take advantage of this vulnerability, we only had to enter in the username as many `%x` as the number of stack values ​​that we want to be popped from the stack and by adding `%s` to the end, the result would be displayed as a string. So after attempting various combinations we succeeded and with `%x%x%x%x%x%x%s` we got the admin password: `0fba1b57781369f0dcfb5b55e61764fd`.

- This appeared in the web developer tools in the authenticate header, as we had also seen in the pico code. Since we knew that the code was hashed in md5, we reversed it online and found a string that matched: `hammertime`. By using this as a password we succesfully connected and got the answer to the third question and the third flag:

```
FLAG={Stop! Hammer Time}
```

### 4. Where are the "Plan X" files?

- After signing in as admin, there was a form that a secret was required. Entering something random in a new page it was displayed `invalid size`. With the location in hexadecimal format the message `secret ok` appeared and was accepted.
 
- Examining the pico code in the `check_secret` folder we saw that this was AES encryption and that the blocks were divided in blocks of 16 bytes. Converting the location that was in hexadecimal format to bytes, it had a length of 32, so it was clear there were two blocks. 

- The message `invalid padding` appeared when the padding was wrong and `wrong secret` when the secret was wrong, but there was correct padding. So we realised, we could use this to extract information to find the last 16 bytes of the plaintext.

- As is described in: https://robertheaton.com/2013/07/29/padding-oracle-attack to find each byte in position N of the block we must have N random bytes at the beginning, which we keep constant, then try the next byte we want to find with values from 0 to 255, then using the intermediate bytes and "XORing" them with the padding we are considering, that is (16-N), and finally the last 16 bytes of the ciphertext that was given.

- When `wrong secret` was displayed as a response, this would mean that we have found the intermediate byte in this position as it will have correct padding. So we stored it in intermediates to be used in later iterations by "XORing" it with the padding it was found with.

- Initially, we tested just to find the last byte, to make sure that the equations we wrote were correct and that there is indeed a byte that returns `wrong secret`. After finding the last byte this way, we wrote [riddle1.py](), which automated the process for all the bytes.

- We use the auxiliary array `inters` to store each byte we found and posting to the onion site with each cyphertext we were testing, we examined the response by handling the exception that was returned. This stopped after it has been found, and if it wasn't continued by increasing the byte. On the odd occasion, that there was an error due to refused connection or time out, then the program tried again with the same ciphertext.

- In [riddle2.py]() we generalised and automated the process for when there are more than two blocks for decryption. That is, it works in the same way, starting from the penultimate block, but continues until the blocks are exhausted. In [run.sh]() is the script that runs this.

- Finally, after finding all the bytes, by simply doing XOR with the bytes of the cyphertext, we managed to recover the plaintext which is also the flag of the question:

```
FLAG={/secet/x}
```

### 5. What are the results of "Plan Y"?

- From the flag of the previous question, we realised that we had to gain access to a file on the server. Firstly, we tried all previous links with the suffix `/secet/x`. This approach didn't work, so we figured we'd have to work using the pico code.

- The most straightforward way to exploit the buffer overflow vulnerability of `printf()` to retrieve files was with the cat command which belongs to system. So, we started setting up the attack locally, looking for a way to enter the command we wanted to execute in the return address of the program.

-  In `post_param()`, we realised we could overflow the buffer and by using gdb and turning on the `set follow-fork-mode child` flag to follow only child processes and placing a break point immediately after the buffer definition between lines 177 and 178 we tried to extract the necessary information about the structure of memory. 

- With the command `info frame` we got some initial information, such as the return address and the ebp address, while with a break on the line defining the buffer we found its first address. With the `x/20xw $esp` command, we were able to display the stack structure for a given time, with the bytes up to the return address of the function.

- We noticed that the stack consisted of 13 words, the buffer, 1 word, the canary (that ended in `00`), 2 words, the ebp and the return address. The aforementioned structure had to be replicated in our attack string, simply modifying it with the return address of the system call.

- Next step, was to manage to gain access to the return address through the vulnerability of `printf()`. Running the server on linux02 that was suggested in the initial page and using gdb we found the return address of `check_auth()` that we used in [test_localhost.py](). The script tries combinations of `%08x` until the return address is found in the bytes returned by the vulnerable `printf()`. This was achieved in the test in the 31st byte.

- We observed that the 30th byte was 136 bytes away from the ebp, while the 28th byte was 1685936 bytes away from the system address, while the 27th and 29th bytes contained the canary information. In this way, we repeated this process a few times to make sure that the offsets always remain constant. 

- Finally, we set up in [riddle1.py]() the attack, adding the appropriate offsets. The process was automated in [run.sh]() for other files as well. This way, we got the contents of `/secet/x`, which redirected us to `/secet/y` and we got the flag for this question:

```
FLAG={41.99299141232}
```

### 6. What is the code for "Plan Z"?

- In the `/secet/y` file of the previous question, there was the following sequence: `1. e4 c6 2. d4 d5 3. Nc3 dxe4...`, which we recognised as Chess moves. 

- By searching online we found in https://en-academic.com/dic.nsf/enwiki/780734 that they were the opening from Kasparov's historical game #6 against Deep Blue. The final winning move for deep blue was c4. So we used that in the first part of the flag, since it was stated that it would be of the form: `FLAG={<next move><public IP of this machine>}`.

- The second part of the flag was rather straightforward since we only needed to modify the code from the previous question to find the public IP of the machine. To achieve that we simply replaced the `cat` command with a `curl` and a url that returns the IP address. 

- So with `api.ipify.org` we were able to get `54.210.15.244` for the second part of the flag. The code for this is in: [riddle1.py]() and the script [run.sh]() automates the process. Finally, by concatenating the Chess move, along with the IP we were able to get the final flag:

```
FLAG={c454.210.15.244}
```

### Acknowledgements

This challenge was introduced as an assignment for the course YS13 Computer Security of Spring 2022 taught by [Kostas Chatzikokolakis](https://www.chatzi.org).
