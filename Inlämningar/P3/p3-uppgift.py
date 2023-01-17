# TDP015 Programming Assignment 3
# Number Theory
# Skeleton Code

import random

# In this assignment you are asked to implement a simple version of
# the RSA cryptosystem.
#
# https://en.wikipedia.org/wiki/RSA_(cryptosystem)

# ## Problem 1
#
# At its core, the RSA cryptosystem deals with integers. In order to
# encrypt and decrypt strings, we first need to convert them into
# numbers. To do that we first encode each string into a byte array,
# and then convert each byte into an integer. Here is an example:
#
# String: 'foo'
# Byte array: b'foo'
# Integers: [102, 111, 111]
#
# In real implementations of RSA, a single integer corresponds to a
# block of bytes. Here is an example where we encode blocks of 2 bytes
# instead of single bytes. In order for this to work, we need to pad
# the original byte string with a zero byte:
#
# String: 'foo'
# Byte array: b'foo'
# Byte array, padded: b'foo\x00'
# Integers: [26223, 28416]
#
# To encode a string into a byte array, use
# https://docs.python.org/3/library/stdtypes.html#str.encode
#
# To decode a byte array into a string, use
# https://docs.python.org/3/library/stdtypes.html#str.decode
#
# To convert a byte array to an integer, use
# https://docs.python.org/3/library/stdtypes.html#int.from_bytes
#
# To convert an integer into a byte array, use
# https://docs.python.org/3/library/stdtypes.html#int.to_bytes


def text2ints(text, m):
    """Encode a string into a list of integers.

    Args:
        text: A string.
        m: The size of a block in bytes.

    Returns:
        A list of integers.

    """
    string = text.encode()
    while(len(string) % m != 0):
        string += '\x00'.encode()
    string_list = [string[i:i+m] for i in range(0, len(string), m)]
    array_finished = []
    for strs in string_list:
        array_finished.append(int.from_bytes(strs, byteorder='big'))
    return array_finished


def ints2text(ints, m):
    """Decode a list of integers into a string.

    Args:
        ints: A list of integers.
        m: The size of a block in bytes.

    Returns:
        A string.

    """
    array_int = ints
    array_byt = []
    array_str = []
    for p in array_int:
        array_byt.append(p.to_bytes(m, byteorder= 'big'))
    for bytes in array_byt:
        array_str.append(bytes.decode())

    strs = "".join(array_str)
    return strs.replace('\x00', '')


# ## Problem 2
#
# Your next task is to implement the Euclidean algorithm for computing
# the greatest common divisor (gcd) of two integers `a` and `b`. You
# will actually start by implementing an extended version of this
# algorithm that computes not only the gcd but also a pair of
# so-called Bezout coefficients. These are integers `x` and `y`
# satisfying the equation
#
# ax + by = gcd(a, b)
#
# The extended Euclidean algorithm is described here:
# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
#
# Once you have implemented the extended Euclidean algorithm,
# implementing the standard algorithm is trivial.


def xgcd(a, b):
    """Computes the greatest common divisor (gcd) and a pair of Bezout
    coefficients for the specified integers.

    Args:
        a: An integer.
        b: An integer.

    Returns:
        A triple `(g, x, y)` where `g = gcd(a, b)` and `x`, `y` are
        Bezout coefficients for `a` and `b`.

    """
    g = 0
    x = 0
    y = 1
    pr_x = 1
    pr_y = 0

    while b != 0:
        g = a // b
        a, b = b, (a % b)
        x, pr_x = (pr_x - g * x), x
        y, pr_y = (pr_y - g * y), y
    return a, pr_x, pr_y


def gcd(a, b):
    """Computes the greatest common divisor (gcd) of the specified
    integers.

    Args:
        a: An integer.
        b: An integer.

    Returns:
        The greatest common divisor of the specified integers.

    """
    while b != 0:
        a, b = b, (a % b)
    return a


# ## Problem 3
#
# Your next task is to implement a function that generates an RSA key
# pair from a pair of two prime numbers, `p` and `q`. A key pair
# consists of a public key `(e, n)` (`e` stands for "encrypt") and a
# private key `(d, n)` (`d` stands for "decrypt").  Use the following
# recipe (which is slightly simplified from the real RSA cryptosystem):
#
# 1. Compute n = p * q
# 2. Compute phi = (p-1) * (q-1)
# 3. Choose 1 < e < phi such that e and phi are coprime.
# 4. Determine d as the modular multiplicative inverse of e modulo phi.
#
# For step 3, use a random number generator and the Euclidean
# algorithm from Problem 2 to generate numbers in the relevant range
# until you find a number that satisfies the criterion.
#
# For step 4, note that the modular multiplicative inverse of e modulo
# phi is simply the Bezout coefficient for e, modulo phi. This means
# that you can use the extended Euclidean algorithm from Problem 2.


def generate_keypair(p, q):
    """Generate an RSA key pair.

    An RSA key pair consists of a public key `(e, n)` and a private
    key `(d, n)`.

    Args:
        p: A prime number.
        q: A prime number, distinct from `p`.

    Returns:
        An RSA keypair.

    """
    n = p * q
    phi = (p-1) * (q-1)
    r = random.randrange(1, phi)
    g = gcd(r, phi)
    while g != 1:
        r = random.randrange(1, phi)
        g = gcd(r, phi)

    d = xgcd(r, phi)[1]
    if r*d % phi == 1:
        return ((r, n), (d, n)) if d > 0 else generate_keypair(p, q)
    else:
        return "Whoaaa!"


# ## Problem 4
#
# Implement functions for encryption and decryption. The encryption
# and decryption of a single integer i is very simple:
#
# Encryption: i^e % n
# Decryption: i^d % n
#
# (You can implement this efficiently using the `pow()` function.)
#
# How to choose the block size? On the one hand, it should be as large
# as possible. On the other hand, both encryption and decryption are
# modulo n, so one cannot use block sizes that yield integers larger
# than that value. Therefore, as the block size we should choose the
# largest number of bytes b such that 2^(8*b)-1 < n. To give a
# concrete example, if n >= 256 then any integer with 1 byte (maximal
# value 255) will fit into n, but if n < 65536 then not every integer
# with 2 bytes (maximal value 65535) will fit into n -- so for n
# within this range, the block size should be 1.


def encrypt(pubkey, plaintext):
    """Encrypt a plaintext message using a public key.

    Args:
        pubkey: A key.
        plaintext: A plaintext message (a string).

    Returns:
        A ciphertext message (a list of integers).

    """
    e, n = pubkey
    b = 0
    while pow(2, 8*(b+1))-1 < pubkey[1]: ## HÄR STOD 'seckey' ISTÄLLET FÖR 'pubkey'. 
        b += 1
    p = text2ints(plaintext, b)
    cipher = [pow(char, e, n) for char in p]
    return cipher


def decrypt(seckey, ciphertext):
    """Decrypt a ciphertext message using a secret key.

    Args:
        seckey: A key.
        ciphertext: A ciphertext message (a list of integers).

    Returns:
        A plaintext message (a string).

    """
    p, q = seckey
    b = 0
    while pow(2, 8*(b+1))-1 < seckey[1]:
        b += 1

    array_ints = []
    for ch in ciphertext:
        array_ints.append(pow(ch, p, q))
    return ints2text(array_ints, b)


# To test your implementation, you can use the following code, which
# will allow you to generate a key pair and encrypt messages.

if __name__ == "__main__":
    #try:
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))
    print("Generating keypair")
    pubkey, seckey = generate_keypair(p, q)
    print("The public key is", pubkey, "and the private key is", seckey)
    message = input("Enter a message to encrypt with the public key: ")
    encrypted_msg = encrypt(pubkey, message)
    print("The encrypted message is: ", end="")
    print(" ".join(map(lambda x: str(x), encrypted_msg))) 
    print("The decrypted message is: ", end="")
    print(decrypt(seckey, encrypted_msg))
    #except ZeroDivisionError as oe:
    #print("After the zero divsion error", oe)

# AV NÅGON ANLEDNING JAG FÅR 'overflow error' NÄR JAG KÖR FÖR HÖGA PRIMTAL VILKET ÄR KONSTIGT, ANNAR FUNGERAR PROGRAMMET SOM DET SKA.
# UPPDATERING: JAG ÄNDRADE RAD 257 DÅ HADE JAG EXPONENTEN UPP TILL 32 ISTÄLLET FÖR 8.
# 
# UPPDATERING: NU HAR JAG FIXAT PROBLEMET I ENCRYPT VILKET JAG SJÄLV BLEV FÖRVÅNAD ATT 
# ## VARFÖR DET STOD 'seckey' ISTÄLLET FÖR 'pubkey'.  

# As a further test, we have generated a ciphertext for you. With a
# working implementation, you should be able to decode that ciphertext
# using the secret key (91307, 268483).
#
# 259114 14038 13667 74062 148955 50062 36907 18603 93303 170481 7991
