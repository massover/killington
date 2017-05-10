import random

import requests

from django.conf import settings


def get_random_word(max_length=16):
    word_length = random.randint(1, 16)
    return requests.get(
        'http://www.setgetgo.com/randomword/get.php?len={}'.format(word_length)
   ).content.lower()