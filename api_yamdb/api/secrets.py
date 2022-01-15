import hashlib

from django.utils.crypto import get_random_string


def generate_activation_key(username):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(10, chars)
    return hashlib.sha256((secret_key + username).encode('utf-8')).hexdigest()
