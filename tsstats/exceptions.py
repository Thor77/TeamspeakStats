class InvalidConfiguration(Exception):
    '''
    The configuration is invalid (either config-file or cli-args)
    '''


class InvalidLog(Exception):
    '''
    Something impossible appeared at the logs,
    for example a disconnect before a connect
    '''
    pass
