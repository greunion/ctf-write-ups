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
