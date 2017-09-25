# -*- coding: utf-8 -*-
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
        (client, key_l(client)) for client in clients.values()
        if key_l(client) > 0
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


def transform_pretty_identmap(pretty_identmap):
    '''
    Transforms a list of client ID mappings from a more descriptive format
    to the traditional format of alternative IDs to actual ID.

    :param pretty_identmap: ID mapping in "nice" form
    :type pretty_identmap: list

    :return: ID mapping in simple key/value pairs
    :rtype: dict
    '''

    final_identmap = {}
    for mapping in pretty_identmap:
        for alt_id in mapping['alternate_ids']:
            final_identmap[alt_id] = mapping['primary_id']
    return final_identmap
