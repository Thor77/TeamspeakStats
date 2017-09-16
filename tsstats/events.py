# -*- coding: utf-8 -*-
from collections import namedtuple

Event = namedtuple(
    'Event', ['timestamp', 'identifier', 'action', 'arg', 'arg_is_client']
)


def nick(timestamp, identifier, nick):
    return Event(timestamp, identifier, 'set_nick', nick, arg_is_client=False)


def connect(timestamp, identifier):
    return Event(
        timestamp, identifier, 'connect', arg=timestamp, arg_is_client=False
    )


def disconnect(timestamp, identifier):
    return Event(
        timestamp, identifier, 'disconnect', arg=timestamp, arg_is_client=False
    )


def kick(timestamp, identifier, target_identifier):
    return Event(
        timestamp, identifier, 'kick', target_identifier, arg_is_client=True
    )


def ban(timestamp, identifier, target_identifier):
    return Event(
        timestamp, identifier, 'ban', target_identifier, arg_is_client=True
    )
