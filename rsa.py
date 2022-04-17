import random
import sys
import math


def is_prime(n):
    low_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97,
                  101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197,
                  199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
                  317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                  443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
                  577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
                  701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829,
                  839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977,
                  983, 991, 997]

    if n in low_primes:
        return True

    prime_flag = 0
    if n > 1:
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                prime_flag = 1
                break
        if prime_flag == 0:
            return True
        else:
            return False
    else:
        return False


def is_co_prime(p, q):
    return gcd(p, q) == 1


def gcd(p, q):
    while q:
        p, q = q, p % q

    return p


def egcd(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    _gcd, x1, y1 = egcd(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return _gcd, x, y


def modular_inv(a, b):
    _gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x


def prime_factors(n):
    org = n
    primes = []
    while n % 2 == 0:
        primes.append(2)
        n = n / 2

    # n must be odd at this point
    # so a skip of 2 ( i = i + 2) can be used
    for i in range(3, int(math.sqrt(n)) + 1, 2):

        # while i divides n , print i and divide n
        while n % i == 0:
            primes.append(int(i))
            n = n / i

    # Condition if n is a prime
    # number greater than 2
    if n > 2:
        primes.append(int(n))

    for num in primes:
        for temp_num in primes:
            if num * temp_num == org:
                return num, temp_num
    print("P AND Q CANNOT BE FOUND")
    exit(-1)


def generate_public_key(p, q):
    n = p * q  # RSA Modulus
    phi_n = (p - 1) * (q - 1)  # totient

    # (e, n) - public key
    e = 2
    while e < phi_n:
        if is_co_prime(e, phi_n):
            break
        else:
            e += 1

    return e, n


def generate_private_key(e, n):
    p, q = prime_factors(n)

    phi_n = (p - 1) * (q - 1)

    d = modular_inv(e, phi_n)

    return d, n


def encrypt(e, n, msg):
    cipher = []

    for c in msg:
        m = ord(c)
        cipher.append(pow(m, e, n))

    return cipher


def decrypt(d, n, cipher):
    decipher = []

    for c in cipher:
        decipher.append(pow(c, d, n))

    return decipher
