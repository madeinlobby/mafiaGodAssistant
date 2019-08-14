import string
from random import randrange, random


class MakeRandomPassword:

    @staticmethod
    def random_string_digits(string_length=6):
        letters_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_digits) for i in range(string_length))

    @staticmethod
    def make_pass():
        first_part = randrange(100, 500)
        second_part = MakeRandomPassword.random_string_digits(8)
        return second_part + first_part
