import unicodedata


def normalizer(text):
    """
    Converts non ASCII letters into latin, for example Müller -> Muller

    :param text: str
    :return: str
    """
    return unicodedata.normalize('NFD', text).encode('ASCII', 'ignore').decode()
