import pandas as pdb
from Crypto.Cipher import AES
import base64

secret_key = b'1234567890123456'
df = pdb.read_excel('SalesLead.xlsx')
cipher = AES.new(secret_key,AES.MODE_ECB) # never use ECB in strong systems obviously
def encrypt(x):
    pad_it = lambda s: bytes(s+(16 - len(s)%16)*chr(16 - len(s) % 16), encoding='utf8')
    base64.b64encode(cipher.encrypt(pad_it(x)))

def decrypt(x):
    unpad = lambda s : s[:-ord(s[len(s)-1:])]
    x = base64.b64decode(str(x))    
    return unpad(cipher.decrypt(x)).decode('utf8')
#encoded = base64.b64encode(cipher.encrypt(msg_text))

#decoded = cipher.decrypt(base64.b64decode(encoded))

df['Encoded_Column'] = df['Contact'].apply(lambda x: encrypt(str(x)))
df['Decoded_Column'] = df['Encoded_Column'].apply(lambda x: decrypt(x))
print(df)