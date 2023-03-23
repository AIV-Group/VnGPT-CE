import os
import jwt
from dotenv import load_dotenv
load_dotenv('./.env')
import random
import string

def encode(type, key, secret_key):
  if type == "encode":
    encode = jwt.encode({"key": key}, secret_key, algorithm="HS256")
    return encode
  elif type == "decode":
    decode = jwt.decode(key, secret_key, algorithms="HS256")
    return decode["key"]
  else:
    pass



def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str