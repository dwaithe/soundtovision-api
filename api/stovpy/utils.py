import secrets
import string
def generate_uniqID():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(5)).lower()
def str_to_float(time_str):
    minutes, seconds = map(float, time_str.split(":"))
    return minutes * 60 + seconds