from math import sqrt
from random import shuffle, random
from fundamental_domain.hyperbolic_plane import H, HyperbolicTriangle
from fundamental_domain import MAX_HEIGHT

class SL2Z:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        assert self.det() == 1

    @staticmethod
    def identity():
        return SL2Z(1, 0, 0, 1)
    
    # translation
    @staticmethod
    def t():
        return SL2Z(1, 1, 0, 1)
    
    # translation by n
    @staticmethod
    def tn(n):
        return SL2Z(1, n, 0, 1)
    
    # inversion
    @staticmethod
    def s():
        return SL2Z(0, -1, 1, 0)
    
    # determinant
    def det(self):
        return self.a * self.d - self.b * self.c
    
    # inverse
    def inv(self):
        return SL2Z(self.d, -self.b, -self.c, self.a)
    
    def __mul__(self, other):
        a1 = self.a * other.a + self.b * other.c
        b1 = self.a * other.b + self.b * other.d
        c1 = self.c * other.a + self.d * other.c
        d1 = self.c * other.b + self.d * other.d
        return SL2Z(a1, b1, c1, d1)

    def __eq__(self, other):
        return (self.a, self.b, self.c, self.d) == (other.a, other.b, other.c, other.d) or (self.a, self.b, self.c, self.d) == (-other.a, -other.b, -other.c, -other.d)
    
    def __repr__(self):
        return f"[{self.a} {self.b} {self.c} {self.d}]"
    
    # action of this on z
    def __call__(self, z):
        if z.is_infinity():
            if self.c == 0:
                return H.infinity()
            return H(self.a / self.c)
        return H((self.a * z.z + self.b) / (self.c * z.z + self.d))

# representative of a coset of gamma
class CosetRepresentative:
    def __init__(self, matrix, distance=0, name=""):
        self.matrix = matrix
        self.distance = distance
        self.name = name
        self.t = None
        self.t_inv = None
        self.s = None
    
    # corners of the fundamental domain of SL_2(Z)
    @staticmethod
    def F():
        w = sqrt(3) / 2
        F = [H(0.5 + w * 1j), H(-0.5 + w * 1j), H.infinity()]
        return F
    
    def coset(self):
        A = list(map(self.matrix, CosetRepresentative.F()))
        return A
    
    def appearance(self):
        y_coordinates = list(map(lambda u: u.y if not u.is_infinity() else MAX_HEIGHT, self.coset()))
        return sum(y_coordinates) / 3
    
    # asymptote code to draw this, also returns information about the size of the figure
    def to_asy(self, label=False):
        A = self.coset()
        return HyperbolicTriangle(*A).to_asy(label=self.name if label else None), max([abs(a.x) for a in A if not a.is_infinity()])
    
    # latex/tikz code to draw this, also returns information about the size of the figure
    def to_tex(self, label=False):
        A = self.coset()
        return HyperbolicTriangle(*A).to_tex(label=self.name if label else None), max([abs(a.x) for a in A if not a.is_infinity()])    
    
# subgroup of SL_2(Z), takes a function checking if a given element is a member of the group or not
class Gamma:
    def __init__(self, membership_check):
        self.membership_check = membership_check
    
    def equiv(self, a, b):
        return self.membership_check(a * b.inv())

    @staticmethod
    def sl2z():
        return Gamma(lambda m: True)

    @staticmethod
    def gamma_0_n(n):
        return Gamma(lambda m: m.c % n == 0)
    
    @staticmethod
    def gamma_1_n(n):
        return Gamma(lambda m: m.a % n == 1 and m.c % n == 0 and m.d % n == 1)
    
    @staticmethod
    def gamma_n(n):
        return Gamma(lambda m: m.a % n == 1 and m.b % n == 0 and m.c % n == 0 and m.d % n == 1)
    
    def get_fundamental_domain(self, choice_function):
        coset_representatives = [CosetRepresentative(SL2Z.identity())]
        while True:
            possible_options = []
            for cri, cr in enumerate(coset_representatives):
                # t direction
                if cr.t is None:
                    mt = cr.matrix * SL2Z.t()
                    for crki, crk in enumerate(coset_representatives):
                        if self.equiv(mt, crk.matrix):
                            cr.t = crki
                            crk.t_inv = cri
                    if cr.t is None:
                        crn = CosetRepresentative(mt, cr.distance + 1, cr.name + "T")
                        crn.t_inv = cri
                        possible_options.append(crn)
                
                # t_inv direction
                if cr.t_inv is None:
                    mt_inv = cr.matrix * SL2Z.t().inv()
                    for crki, crk in enumerate(coset_representatives):
                        if self.equiv(mt_inv, crk.matrix):
                            cr.t_inv = crki
                            crk.t = cri
                    if cr.t_inv is None:
                        crn = CosetRepresentative(mt_inv, cr.distance + 1, cr.name + "T^{-1}")
                        crn.t = cri
                        possible_options.append(crn)
                
                # s direction
                if cr.s is None:
                    ms = cr.matrix * SL2Z.s()
                    for crki, crk in enumerate(coset_representatives):
                        if self.equiv(ms, crk.matrix):
                            cr.s = crki
                            crk.s = cri
                    if cr.s is None:
                        crn = CosetRepresentative(ms, cr.distance + 1, cr.name + "S")
                        crn.s = cri
                        possible_options.append(crn)
            if not possible_options:
                break
            coset_representatives.append(max(possible_options, key=choice_function))
        return coset_representatives

# asymptote code to draw fundamental domain
def fundamental_domain_to_asy(cosets, label=False):
    with open("templates/template.asy", "r+") as file:
        template = file.read()
    lst = [cr.to_asy(label) for cr in cosets]
    return template.replace("FUNDAMENTAL_DOMAIN", "".join([k[0] for k in lst])).replace("MAX_HEIGHT", str(MAX_HEIGHT)).replace("MAX_WIDTH", str(max([k[1] for k in lst])))

# latex/tikz code to draw fundamental domain
def fundamental_domain_to_tex(cosets, label=False):
    with open("templates/template.tex", "r+") as file:
        template = file.read()
    lst = [cr.to_tex(label) for cr in cosets]
    return template.replace("FUNDAMENTAL_DOMAIN", "".join([k[0] for k in lst])).replace("MAX_HEIGHT", str(MAX_HEIGHT)).replace("MAX_WIDTH", str(max([k[1] for k in lst])))

    
