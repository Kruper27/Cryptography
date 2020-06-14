import random


def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def randomNumber(bits: int):
    x = random.randrange(0, 1 << bits - 1)
    return (1 << bits) + x


def randomBytes(n):
    res = [random.randrange(0, 255) for _ in range(n)]
    return bytes(res)


def millerTest(d, n):
    a = 2 + random.randint(1, n - 4)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True

    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False


def isPrime(n, k):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True

    for el in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
        if n % el == 0:
            return n == el
    d = n - 1
    while d % 2 == 0:
        d //= 2

    for i in range(k):
        if not millerTest(d, n):
            return False
    return True


def randomPrime(bits: int):
    n = randomNumber(bits)
    if n & 1 == 0:
        n += 1

    while not isPrime(n, bits):
        n += 2
    return n


class RSA:

    def __init__(self, e, n, d, p, q):
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        self.n = n

    @classmethod
    def generate(cls, bits, e=65537):
        p = randomPrime(bits)
        q = randomPrime(bits)
        n = p * q
        d = cls.inv(e, (p - 1) * (q - 1))
        return cls(e, n, d, p, q)

    @staticmethod
    def inv(number, base):
        g, res, _ = gcdExtended(number, base)
        if g != 1:
            raise ValueError('Error')
        return res % base


def encrypt(message: int, key: RSA) -> int:
    return pow(message, key.e, key.n)


def decrypt(ciphertext: int, key: RSA) -> int:
    return pow(ciphertext, key.d, key.n)


if __name__ == '__main__':

    plaintext = b'London is the capital of Great Britain '
    intPT = int(plaintext.hex(), 16)
    key = RSA.generate(bits=512)
    print(plaintext)

    ct = encrypt(intPT, key)
    print(ct)

    pt = decrypt(ct, key)
    print(bytes.fromhex(hex(pt)[2:]))
