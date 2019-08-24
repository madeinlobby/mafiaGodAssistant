import random
import string


class MakeRandomPassword:

    @staticmethod
    def random_string_digits(string_length=6):
        letters_digits = string.ascii_letters + string.digits
        return ''.join(random.choices(letters_digits, k=string_length))

    @staticmethod
    def make_pass():
        first_part = random.randrange(100, 500)
        second_part = MakeRandomPassword.random_string_digits(8)
        return second_part + str(first_part)
