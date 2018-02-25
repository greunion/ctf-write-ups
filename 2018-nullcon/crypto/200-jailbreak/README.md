## Jailbreak (Crypto, 200pt)

> Find Jail_id
>
> [Jailbreak.pdf](Jailbreak.pdf)

We are given an AES-128-CBC encoded message. We know the encryption key (`jailbreak123 `) and we are looking for the IV, which is an id repeated two times (`Jail_idJail_id`). We also know that the format of the cleartext message is `name_of_inmate;prison_term=2yrs;about=some useful information of the inmate`

Since it uses [CBC mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_(CBC)) the IV only affects the first block of the decrypted message.

![](CBC_decryption.png)

So we can decrypt the rest of the blocks, using the password and an empty IV.


```bash
echo "U2FsdGVkX1+1KcLc+WlP8rcjdSP8DnOx/W1h+lww6rGCUVH4ghAuhSs+Xs9ShwJNEFlJ4IWDoG00T4LnAqIMrsY9EODHGc7Jv/Rn1lC/h7k=" \
| base64 -D | openssl aes-128-cbc -d -pass pass:jailbreak123 -iv "" | xxd

00000000: f310 0f31 7577 4b3b 7072 6973 6f6e 5f74  ...1uwK;prison_t
00000010: 6572 6d3d 3379 7273 3b61 626f 7574 3d73  erm=3yrs;about=s
00000020: 7065 616b 6572 2061 7420 6e75 6c6c 636f  peaker at nullco
00000030: 6e20 3230 3138 3b0a                      n 2018;.
```

From this we can deduce that the name of the inmate is 7 characters long and that the IV must be 14 hex digits long, since it affects only the name part of the first block. We are also given a hint that the inmate is a speaker at nullcon 2018.

The plan is to get the first names of the conference speakers, keep the ones with 7 characters, xor them with the first 7 decrypted bytes and check if the first half of the IV is equal to the second.

```python
import requests
from bs4 import BeautifulSoup

possible_inmates = []

# Get speakers
response = requests.get('https://nullcon.net/website/goa-2018/about-speakers.php')
soup = BeautifulSoup(response.text, 'html.parser')
speakers = soup.find_all('h4')

for speaker in speakers:
    name = speaker.text.replace('Dr.', '')
    for each in name.split('&'):
        first_name = each.strip().split()[0]
        if len(first_name) == 7:
            possible_inmates.append(first_name.lower())

# Test names
for name in possible_inmates:
    decoded = "f3100f3175774b"
    xor = int(name.encode('hex'), 16) ^ int(decoded, 16)
    hex = format(xor, 'x')
    if hex[:7] == hex[7:]:
        print "[+] Flag found: hackim18{{'{}'}}".format(hex[:7])
```

```bash
$ python solve.py
[+] Flag found: hackim18{'8071625'}
```
