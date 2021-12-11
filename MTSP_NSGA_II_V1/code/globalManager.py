def _init():
    """ Initialization """
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    """ Define a global variable """
    _global_dict[key] = value


def get_value(key, defValue=None):
    """ Get a global variable, return the default value if it does not exist """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue
