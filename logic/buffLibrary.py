"""
buff library
==________==
"""


def kill(player):
    player.status = False
    player.save()
    return player
