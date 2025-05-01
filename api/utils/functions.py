import binascii
import os
#import secrets

def generateAPIKey():
    """
        Function that generates a random APIKey 

        param: None
        return: string => random APIKey 
    """
    #return secrets.token_hex(20)
    return binascii.hexlify(os.urandom(20)).decode()