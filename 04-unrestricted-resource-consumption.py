from concurrent.futures.thread import ThreadPoolExecutor
import subprocess

NUMBER_OF_THREADS = 110


def execute_script(thread_id: int):
    print(f'Thread {thread_id} started')

    subprocess.run(["python", "01-broken-access-control.py"])


def execute():
    with ThreadPoolExecutor(max_workers=NUMBER_OF_THREADS) as executor:
        for i in range(NUMBER_OF_THREADS):
            executor.submit(execute_script, i)


if __name__ == '__main__':
    execute()
