from ConfigParser import ConfigParser


# This module will handle loading all of the OGC content using a human readable
# storage format, such as confloader


class DictParser(ConfigParser):
    """ includes 'as_dict' method which returns an ordered dict """
    def as_dict(self):
        """ clean up _sections and return an ordered dict """
        d = self._sections
        for section in d:
            d[section].pop('__name__', None)
        return d


def load_file(path, defaults={}):
    """
    Parses a path, with an optional default dictionary, and returns an ordered
    dict
    """
    # Load the default parser arguments
    c = DictParser(defaults)
    # open the file load it with the parser
    c.read([path])
    return c.as_dict()


def prep_section(section, prep_funcs):
    """ preprocess strings from the config for use with the game """
    prepped = []
    for i in range(len(section)):
        prepped.append(prep_funcs[i](section[i]))
    return prepped
