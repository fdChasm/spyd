def truncate(string, length):
    if len(string) <= length:
        return string
    else:
        return string[:length]