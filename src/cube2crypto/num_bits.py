def num_bits(a):
    """Returns the number of bits needed to represent abs(a). Returns 1 for 0.
    Based on SO answer: http://stackoverflow.com/a/13663234"""
    if not isinstance(a, (int, long)):
        raise TypeError
    if not a:
        return 1
    # Example: hex(-0xabc) == '-0xabc'. 'L' is appended for longs.
    s = hex(a)
    d = len(s)
    if isinstance(a, long):
        d -= 1
    if a < 0:
        d -= 4
        c = s[3]
    else:
        d -= 3
        c = s[2]
    return {'0': 0, '1': 1, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 3}.get(c, 4) + (d << 2)
