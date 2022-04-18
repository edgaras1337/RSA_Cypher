from database import Database
from rsa import *
from utils import to_int, to_string, to_num_array


def menu():
    run = True
    db = Database()

    while run:
        message = str(input("Enter a message you want to encrypt: "))

        p = to_int(input("\nPlease enter a PRIME number: "))
        while not is_prime(p):
            print("\nNot a prime number!")
            p = to_int(input("\nPlease enter a PRIME number: "))

        q = input("\nPlease enter another PRIME number: ")
        q = to_int(q)
        while p == q:
            print("Numbers must differ!")
            q = to_int(input("\nPlease enter a PRIME number: "))
        while not is_prime(q):
            print("\nNot a prime number!")
            q = to_int(input("\nPlease enter a PRIME number: "))

        # generate public key (e, n) and encrypt the message
        e, n = generate_public_key(p, q)
        enc = to_string(encrypt(e, n, message))
        print(f"Encrypted message: {enc}")

        # save the cipher text to database, along with public key
        db.add_cipher_text_and_key(enc, e, n)

        # fetch the latest saved record from database
        # query returns cipher text and public key values - e, n
        result = db.select_latest_cipher()
        enc, e, n = result[0], int(result[1]), int(result[2])

        print(f"Encrypted message from Database: {enc}")

        # calculate the private key (d, n) and decrypt the message
        d, n = generate_private_key(e, n)
        dec = decrypt(d, n, to_num_array(enc))

        print(f"Decrypted message: {to_string(dec)}")

        while True:
            user_input = input("Do you want to encrypt another message? (Y/N) ")
            if user_input == 'n' or user_input == 'N':
                run = False
                break
            if user_input == 'y' or user_input == 'Y':
                break
            print("Wrong input!")


if __name__ == '__main__':
    menu()
