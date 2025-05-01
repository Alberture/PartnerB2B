import binascii
import os

def generateAPIKey(partner):
    return binascii.hexlify(os.urandom(20)).decode()