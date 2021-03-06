
import math
import random

from rest_framework_jwt.settings import api_settings


def get_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token


# function to generate OTP
def generateOTP():
    digits = "0123456789"
    OTP = ""

    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP
