import binascii
import Crypto.Random

def get_random_number(bits):
    return int(binascii.hexlify(Crypto.Random.get_random_bytes(bits)), 16)
