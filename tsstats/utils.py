# -*- coding: utf-8 -*-
import datetime


def sort_clients(clients, key_l):
    '''
    sort `clients` by `key`

    :param clients: clients to sort
    :param key_l: lambda/function returning the value of `key` for a client

    :type clients: tsstats.client.Clients
    :type key_l: function

    :return: sorted `clients`
    :rtype: list
    '''
    cl_data = [
        (client, key_l(client)) for client in clients if key_l(client) > 0
    ]
    return sorted(cl_data, key=lambda data: data[1], reverse=True)


def seconds_to_text(seconds):
    '''
    convert `seconds` to a text-representation

    :param seconds: seconds to convert
    :type seconds: int

    :return: `seconds` as text-representation
    :rtype: str
    '''
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours = str(hours) + 'h ' if hours > 0 else ''
    minutes = str(minutes) + 'm ' if minutes > 0 else ''
    seconds = str(seconds) + 's' if seconds > 0 else ''
    return hours + minutes + seconds


def filter_threshold(clients, threshold):
    '''
    Filter clients by threshold

    :param clients: List of clients as returned by tsstats.utils.sort_clients
    :type clients: list

    :return: Clients matching given threshold
    :rtype: list
    '''
    return list(filter(lambda c: c[1] > threshold, clients))


class UTC(datetime.tzinfo):
    '''
    Reimplementation of `timezone.utc` for Python2-Compatibility
    '''

    def utcoffset(self, dt):
        return datetime.timedelta(0)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC'


def tz_aware_datime(datetime, timezone=UTC()):
    '''
    Make `datetime` aware of it's timezone (UTC by default)

    :param datetime: Target datetime
    :param timezone: Target timezone

    :type datetime: datetime.datetime
    :type timezone: datetime.timezone
    '''
    return datetime.replace(tzinfo=timezone)
