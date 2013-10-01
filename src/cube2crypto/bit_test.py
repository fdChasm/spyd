def bit_test(num, bit):
    return int(num) & (0x1 << bit) != 0
