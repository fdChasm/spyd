from gfield import GField
from modular_inverse import modular_inverse
from num_bits import num_bits
from bit_test import bit_test
import ecc_params as _ecc_params

class Jacobian(object):
    ecc_params = None
    _x, _y, _z = None, None, None
    
    def __init__(self, x, y, z, ecc_params=_ecc_params):
        self.ecc_params = ecc_params
        self._x = GField(x)
        self._y = GField(y)
        self._z = GField(z)
        
    @staticmethod
    def base(ecc_params=_ecc_params):
        epb = ecc_params.base
        return Jacobian(epb[0], epb[1], epb[2], ecc_params)
        
    @staticmethod
    def origin(ecc_params=_ecc_params):
        epo = ecc_params.origin
        return Jacobian(epo[0], epo[1], epo[2], ecc_params)
        
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
        
    @property
    def z(self):
        return self._z
        
    @staticmethod
    def parse(s, ecc_params=_ecc_params):
        '''Takes a 192 bit integer in hex with a + or - sign on the front and
        returns a Jacobian object.'''
        assert s[0] in ('-', '+')

        ybit, s = s[0] == '-', s[1:]
        x = GField(int(s, 16), ecc_params)
        
        _ = x.mul2().add(x)
        y2 = x.pow(3).sub(x.mul(3)).add(ecc_params.B)
        y = y2.legendre_sqrt()
        if y is None:
            y = 0
        if bit_test(y, 0) != ybit:
            y = -y
        
        z = 1
        
        return Jacobian(x, y, z, ecc_params)
        
    def __str__(self):
        if bit_test(self.y, 0):
            sign = '-'
        else:
            sign = '+'
            
        return sign+str(self.x)
        
    def __repr__(self):
        return "Jacobian<{}, {}, {}>".format(int(self.x), int(self.y), int(self.z))
        
    def normalize(self):
        if int(self.z) in (0, 1):
            return self
            
        z = GField(modular_inverse(int(self.z), self.ecc_params.P), self.ecc_params)
        tmp = z.sqr()
        
        x = self.x.mul(tmp)
        y = self.y.mul(tmp).mul(z)
        z = 1
        return Jacobian(x, y, z, self.ecc_params)
        
    def mul(self, n):
        this = Jacobian.origin(self.ecc_params)
        for i in xrange(num_bits(int(n))-1,-1,-1):
            this = this.double()
            if bit_test(n, i):
                this = this.add(self)
        return this
        
    def double(self):
        if int(self.z) == 0:
            return self
        elif int(self.y) == 0:
            return Jacobian.origin(self.ecc_params)
            
        c = self.z.sqr()
        d = self.x.sub(c)
        c = c.add(self.x)
        d = d.mul(c)
        c = d.mul(3)
        z = self.z.mul(self.y).mul2()
        a = self.y.sqr()
        b = a.mul2()
        d = self.x.mul2().mul(b)
        x = c.sqr().sub(d.mul2())
        a = b.sqr().mul2()
        y = d.sub(x).mul(c).sub(a)
        return Jacobian(x, y, z, self.ecc_params)
        
        
    def add(self, q):
        if int(q.z) == 0:
            return self
        elif int(self.z) == 0:
            return q
        
        _, _, c, d, e, f = 0,0,0,0,0,0
        
        a = self.z.sqr()
        b = q.y.mul(a).mul(self.z)
        a = a.mul(q.x)
        
        if int(q.z) == 1:
            c = self.x.add(a)
            d = self.y.add(b)
            a = self.x.sub(a)
            b = self.y.sub(b)
        else:
            e = q.z.sqr()
            f = self.y.mul(e).mul(q.z)
            e = e.mul(self.x)
            c = e.add(a)
            d = f.add(b)
            a = e.sub(a)
            b = f.sub(b)
        
        if int(a) == 0:
            if int(b) == 0:
                return self.double()
            else:
                return Jacobian.origin(self.ecc_params)
        
        if int(q.z) != 1:
            z = self.z.mul(q.z)
        else:
            z = self.z
        
        z = z.mul(a)
        
        e = a.sqr()
        f = c.mul(e)
        x = b.sqr().sub(f)
        
        e = e.mul(a).mul(d)
        y = f.sub(x).sub(x).mul(b).sub(e)
        y = y.div2(y)
        
        return Jacobian(x, y, z, self.ecc_params)
        
