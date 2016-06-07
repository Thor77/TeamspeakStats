# -*- coding: utf-8 -*-


def sort_clients(clients, key):
    '''
    sort `clients` by `key`

    :param clients: clients to sort
    :param key: key to sort clients with

    :type clients: tsstats.client.Clients
    :type key: str

    :return: sorted `clients`
    :rtype: list
    '''
    cl_data = [(client, client[key]) for client in clients if client[key] > 0]
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
