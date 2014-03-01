import string

def filtertext(src, whitespace, maxlen):
    last_was_ctrl_char = [False]

    def allowchar(c):
        if last_was_ctrl_char[0]:
            last_was_ctrl_char[0] = False
            return False

        if not whitespace and c.isspace():
            return False

        if c == '\f':
            last_was_ctrl_char[0] = True
            return False

        return (c in string.printable)

    dst = filter(allowchar, src)

    if len(dst) > maxlen:
        dst = dst[:maxlen]

    return dst
