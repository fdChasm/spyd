import string

def filtertext(src, whitespace, maxlen):
    def allowchar(c):
        if not whitespace and c.isspace():
            return False
        
        if c == '\f':
            return False
        
        return (c in string.printable)
    
    dst = filter(allowchar, src)
    
    if len(dst) > maxlen:
        dst = dst[:maxlen]
    
    return dst