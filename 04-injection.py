import hashlib
import base64

target = "0DPiKuNIrrVmD8IUCuw1hQxNqZc="

def brute_force_sha1(target_base64):
    with open('password-wordlist.txt') as f:
        for p in f:
            password=p.strip()
            print(f'trying password: {password}')
            sha1_hash = hashlib.sha1(password.encode()).digest()
            base64_hash = base64.b64encode(sha1_hash).decode()

            if base64_hash == target_base64:
                print(f'password found for hash {target}: {password}')
                return password  

    return None  

if __name__ == '__main__':
    brute_force_sha1(target)