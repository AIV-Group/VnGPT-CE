import os
import jwt
from dotenv import load_dotenv
load_dotenv('./.env')

def encode(type, key, secret_key):
  if type == "encode":
    encode = jwt.encode({"key": key}, secret_key, algorithm="HS256")
    return encode
  elif type == "decode":
    decode = jwt.decode(key, secret_key, algorithms="HS256")
    return decode["key"]
  else:
    pass
