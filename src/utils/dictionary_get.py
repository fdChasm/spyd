def dictget(dictionary, *keys):
    values = []
    for key in keys:
        values.append(dictionary[key])
    return values