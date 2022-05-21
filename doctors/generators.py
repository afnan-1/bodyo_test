from oauthlib import common


def random_token_generator(length=100):
    # token in accessmodel had max_length of 255
    return common.generate_token(length=100)