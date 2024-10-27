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
    def __init__(self, matrix, distance=0):
        self.matrix = matrix
        self.t_direction = False
        self.t_inv_direction = False
        self.s_direction = False
        self.m_index_t_direction = None
        self.m_index_t_inv_direction = None
        self.m_index_s_direction = None
        self.distance = distance
    
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
    def to_asy(self):
        A = self.coset()
        return HyperbolicTriangle(*A), max([abs(a.x) for a in A if not a.is_infinity()])
    
    # latex/tikz code to draw this, also returns information about the size of the figure
    def to_tex(self):
        A = self.coset()
        return HyperbolicTriangle(*A), max([abs(a.x) for a in A if not a.is_infinity()])    
    
# subgroup of SL_2(Z), takes a function checking if a given element is a member of the group or not
class Gamma:
    def __init__(self, membership_check):
        self.membership_check = membership_check
    
    def equiv(self, a, b):
        return self.membership_check(a * b.inv())
    
    # this randomly tries going in the T/T^-1/S directions from a randomly chosen element, can be modified to get better looking results
    
    # get fundamental domain step by step, can modify what to choose next
    def get_fundamental_domain(self, choice_function=None):
        coset_representatives = [CosetRepresentative(SL2Z.identity())]
        while True:
            # check t/t_inv/s direction to see if they are already included
            for cri, cr in enumerate(coset_representatives):
                # t direction
                if not cr.t_direction:
                    mt = cr.matrix * SL2Z.t()
                    for crki, crk in enumerate(coset_representatives):
                        if crki == cri:
                            continue
                        if self.equiv(mt, crk.matrix):
                            cr.t_direction = True
                            cr.m_index_t_direction = crki
                            crk.t_inv_direction = True
                            crk.m_index_t_inv_direction = cri

                # t_inv direction
                if not cr.t_inv_direction:
                    mt_inv = cr.matrix * SL2Z.t().inv()
                    for crki, crk in enumerate(coset_representatives):
                        if crki == cri:
                            continue
                        if self.equiv(mt_inv, crk.matrix):
                            cr.t_inv_direction = True
                            cr.m_index_t_inv_direction = crki
                            crk.t_direction = True
                            crk.m_index_t_direction = cri
                
                # s direction
                if not cr.s_direction:
                    ms = cr.matrix * SL2Z.s()
                    for crki, crk in enumerate(coset_representatives):
                        if crki == cri:
                            continue
                        if self.equiv(ms, crk.matrix):
                            cr.s_direction = True
                            cr.m_index_s_direction = crki
                            crk.s_direction = True
                            crk.m_index_s_direction = cri

            possible_options = []
            # get possible options for the new element
            for cri, cr in enumerate(coset_representatives):
                # t direction
                if not cr.t_direction:
                    mt = cr.matrix * SL2Z.t()
                    possible_options.append((cri, cr, "T", CosetRepresentative(mt, cr.distance + 1)))
                    
                # t_inv direction
                if not cr.t_inv_direction:
                    mt_inv = cr.matrix * SL2Z.t().inv()
                    possible_options.append((cri, cr, "T_inv", CosetRepresentative(mt_inv, cr.distance + 1)))
                    
                # s direction
                if not cr.s_direction:
                    ms = cr.matrix * SL2Z.s()
                    possible_options.append((cri, cr, "S", CosetRepresentative(ms, cr.distance + 1)))
            
            # choose one of the possible options
            if not possible_options:
                break
            cri, cr, typ, crn = max(possible_options, key=choice_function)
            if typ == "T":
                crn.t_inv_direction = True
                crn.m_index_t_inv_direction = cri
            elif typ == "T_inv":
                crn.t_direction = True
                crn.m_index_t_direction = cri
            elif typ == "S":
                crn.s_direction = True
                crn.m_index_s_direction = cri
            coset_representatives.append(crn)
        return coset_representatives

# asymptote code to draw fundamental domain
def fundamental_domain_to_asy(cosets):
    with open("templates/template.asy", "r+") as file:
        template = file.read()
    lst = [cr.to_asy() for cr in cosets]
    return template.replace("FUNDAMENTAL_DOMAIN", "".join([k[0].to_asy() for k in lst])).replace("MAX_HEIGHT", str(MAX_HEIGHT)).replace("MAX_WIDTH", str(max([k[1] for k in lst])))

# latex/tikz code to draw fundamental domain
def fundamental_domain_to_tex(cosets):
    with open("templates/template.tex", "r+") as file:
        template = file.read()
    lst = [cr.to_tex() for cr in cosets]
    return template.replace("FUNDAMENTAL_DOMAIN", "".join([k[0].to_tex() for k in lst])).replace("MAX_HEIGHT", str(MAX_HEIGHT)).replace("MAX_WIDTH", str(max([k[1] for k in lst])))

    
