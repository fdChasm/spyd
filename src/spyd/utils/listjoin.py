def listjoin(l):
    if len(l) > 1:
        return ", ".join(l[:-1]) + ", and " + l[-1]
    elif len(l) == 1:
        return l[0]
    else:
        return ""
