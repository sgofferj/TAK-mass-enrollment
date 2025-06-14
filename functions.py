import secrets
import string
import csv


def createPW():
    alphabet = string.ascii_letters + string.digits + "[-_!@#$%^&*(){}[]+=~`|:;<>,./?]."
    password = ''.join(secrets.choice(alphabet) for i in range(20))  # for a 20-character password
    return password

def createURL(server,username,password):
    url = f"tak://com.atakmap.app/enroll?host={server}&username={username}&token={password}"
    return url

def readFile(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        next(reader)
        data = list(reader)
        return data
