import hashlib

block = """transaction_id:9
receiver_name:Jailer
receiver_key:1HGJuDsHPEXU9cFDPxyDn3Tn6US7Q3QyWT
sender_name:Nullcon9
sender_key:17cM7VAJWKvtN7WebxoKmvtdbHM2iv9rSD
transaction_amount:100
time_stamp:1536483609
transaction_signature:02487a9974eff50f5153c7511bc6331059e0e8f41926e0fe56680723125a675d
nonce:"""

i = 0
sig = None

while sig != "9999990b707d6d10d3121eadc054a21d1e9855f679fe1b096c05beb0273c591d":
    i = i + 1
    sig = hashlib.sha256(block + str(i)).hexdigest()

print "[+] Flag found: hackim18{{'{}'}}".format(i)
