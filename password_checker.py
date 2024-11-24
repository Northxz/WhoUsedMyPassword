import requests
import hashlib

def request_api_data(random_char):
    url = "https://api.pwnedpasswords.com/range/" + random_char
    result = requests.get(url)
    if result.status_code != 200:
        raise RuntimeError(f"Error fetching: {result.status_code}")
    return result

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    first5char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5char)
    return get_password_leaks_count(response, tail)

def main():
    password = input("Enter the password to check: ")
    count = pwned_api_check(password)
    if count:
        print(f"Your password: {password} has been used {count} times.")
    else:
        print(f"Your password: {password} has not been found in the database.")

if __name__ == "__main__":
    main()