import random
import string


def generate_random_username(length: int):
    return 'user_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))
