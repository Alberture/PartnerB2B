import binascii
import os

"""
    Function that generates a random APIKey 

    param: None
    return: string => random APIKey 
"""
def generateAPIKey():
    return binascii.hexlify(os.urandom(20)).decode()