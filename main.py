from typing import Optional
import string
import hashlib
import os
import random
import base64
from fastapi import FastAPI
from pydantic import BaseModel


class RequestParams(BaseModel):
	salt_len: Optional[int] = 10
	pretty: Optional[bool] = False
	pin_len: Optional[int] = 4
	use_chars: Optional[bool] = False


app = FastAPI()


def create_salt(len : int):
	salt = base64.b64encode(os.urandom(15)) #Максимальная длина соли = 20
	return salt[:len]

def create_pin(len : int, use_chars : bool):
    digits = string.digits
    symbols = string.ascii_letters + string.digits
    if use_chars == False:
        return ''.join(random.choice(digits) for _ in range(len))
    else:
        return ''.join(random.choice(symbols) for _ in range(len))

def create_pretty_pin():
    half_pin = ''.join(random.choice(string.digits) for _ in range(2))
    pin_type = random.randint(0, 100)
    if pin_type < 20:
        return 2 * half_pin
    elif pin_type >= 20 and pin_type < 40:
        return half_pin + half_pin[::-1]
    elif pin_type >= 40 and pin_type < 60:
        return half_pin + half_pin[0] + random.choice(string.digits)
    elif pin_type >= 60 and pin_type < 80:
        return half_pin + random.choice(string.digits) + half_pin[1]
    elif pin_type >= 80:
        return half_pin + half_pin[1] + random.choice(string.digits)


def get_hash(salt, pin):
    hash = hashlib.sha1()
    hash.update(salt + bytes(pin, 'utf-8'))
    return hash.hexdigest()


def auth(salt_len, pretty, pin_len, use_chars):
    salt = create_salt(salt_len)
    if pretty == True:
        pin = create_pretty_pin()
    else:
        pin = create_pin(pin_len, use_chars)

    hash = get_hash(salt, pin)
    return {
	"pin": pin,
	"salt": salt,
	"hash": hash
	}


@app.post("/")
async def PIN(request: RequestParams):
	return auth(request.salt_len, request.pretty,
	request.pin_len, request.use_chars)
