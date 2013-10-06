from cube2crypto.bit_test import bit_test
from cube2crypto import ecc_params as _ecc_params

def _GField__big_m_pow(x, exp, carry, ecc_params):
    if carry is None:
        if bit_test(exp, 0):
            carry = x
        else:
            carry = 1
    else:
        if exp == 0:
            return carry
        else:
            x = (x * x) % ecc_params.P
            if bit_test(exp, 0):
                carry = (carry * x) % ecc_params.P
    return _GField__big_m_pow(x, exp>>1, carry, ecc_params)

class GField(object):
    ecc_params = None
    value = 0
    
    def __init__(self, value, ecc_params=_ecc_params):
        self.value = int(value)
        self.ecc_params = ecc_params
        
    def add(self, other):
        ov = int(other)
        nv = (self.value + ov) % self.ecc_params.P
        return GField(nv, self.ecc_params)
        
    def mul2(self):
        return self.add(self)
        
    def sub(self, other):
        ov = int(other)
        nv = (self.value - ov) % self.ecc_params.P
        return GField(nv, self.ecc_params)
        
    def mul(self, other):
        ov = int(other)
        nv = (self.value * ov) % self.ecc_params.P
        return GField(nv, self.ecc_params)
        
    def sqr(self):
        return self.mul(self)
        
    def pow(self, exp):
        ov = int(exp)
        if ov < 8:
            nv = (self.value ** ov) % self.ecc_params.P
        else:
            nv = _GField__big_m_pow(self.value, ov, None, self.ecc_params)
        return GField(nv, self.ecc_params)
        
    def div(self, other):
        ov = int(other)
        nv = (self.value / ov) % self.ecc_params.P
        return GField(nv, self.ecc_params)
        
    def div2(self, other):
        ov = int(other)
        if bit_test(ov, 0):
            nv = (ov + self.ecc_params.P)>>1
        else:
            nv = ov>>1
        return GField(nv, self.ecc_params)
        
    def legendre(self, exp):
        res = int(self.pow((exp-1)/2))
        if res == 0:
            return 0
        elif res == 1:
            return 1
        else:
            return -1
            
    def legendre_sqrt(self):
        check = self.legendre(self.ecc_params.P)
        if check == 0:
            return GField(0, self.ecc_params)
        elif check == -1:
            return None
        elif check == 1:
            return self.pow((self.ecc_params.P+1)/4)
        
    def __str__(self):
        v = hex(self.value)
        if v[-1] == 'L':
            v = v[2:-1]
        else:
            v = v[2:]
        return v.zfill(48)
        
    def __repr__(self):
        return "GField<{}>".format(str(self))
        
    def __int__(self):
        return self.value
        
    def __neg__(self):
        return GField(-self.value, self.ecc_params)


