from math import pi, atan2
from fundamental_domain import MAX_HEIGHT, EPSILON

# Upper Half Plane Model
# H represents the upper half plane + its boundary
class H:
    def __init__(self, z, name=""):
        # None represents the point at infinity
        self.z = z
        self.x, self.y = (z.real, z.imag) if z is not None else (None, None)
        assert self.z is None or self.y >= 0
        self.name = name

    def on_boundary(self):
        return self.is_infinity() or abs(self.y) < EPSILON
    
    @staticmethod
    def infinity():
        return H(None)
    
    def is_infinity(self):
        return self.z is None
    
    @staticmethod
    def repr_infinity(x):
        return f"{(x, MAX_HEIGHT)}"
    
    def __eq__(self, other):
        return (self.is_infinity() and other.is_infinity()) or abs(self.z - other.z) < EPSILON
    
    def __repr__(self):
        return "inf" if self.is_infinity() else f"{(self.x, self.y)}"
    
    def __add__(self, other):
        return H(self.z + (other.z if type(other) == H else other))
    
    def __sub__(self, other):
        return H(self.z - (other.z if type(other) == H else other))
    
    def __lmul__(self, other):
        return H(self.z * (other.z if type(other) == H else other))
        
    def __rmul__(self, other):
        return H(self.z * (other.z if type(other) == H else other))
        
    def __mul__(self, other):
        return H(self.z * (other.z if type(other) == H else other))
    
    def __truediv__(self, other):
        return H(self.z / (other.z if type(other) == H else other))
        
    def __abs__(self):
        return abs(self.z)
    
    def angle(self):
        return atan2(self.y, self.x) * (180 / pi)
    
    # asymptote code to draw this
    def to_asy(self):
        return f"dot(\"${self.name}$\",{(self.x, self.y)},dir(90),black);\n" if not self.is_infinity() else "\n"
    
    # latex/tikz code to draw this
    def to_tex(self):
        return f"\\node [black] at {self} {{\\textbullet}};\n" if not self.is_infinity() else "\n"

class HyperbolicLine:
    def __init__(self, z1, z2):
        self.z1, self.z2 = z1, z2

    # intersection of x axis with its perpendicular bisector, center of the euclidean circle pasing through these points
    def center(self):
        x1, y1 = self.z1.x, self.z1.y
        x2, y2 = self.z2.x, self.z2.y
        return (x1 + x2) / 2 + (y1 * y1 - y2 * y2) / (2 * (x1 - x2))

    # asymptote code to draw this
    def to_asy(self, mod=0):
        linewidth = "linewidth(1.5pt)"
        # mod 1 is without draw command
        if mod == 1:
            if self.z1.is_infinity():
                return f"{H.repr_infinity(self.z2.x)} -- {self.z2}"
            if self.z2 .is_infinity():
                return f"{self.z1} -- {H.repr_infinity(self.z1.x)}"
            if abs(self.z1.x - self.z2.x) < EPSILON:
                return f"{self.z1} -- {self.z2}"
            x = self.center()
            return f"arc({(x, 0)},{abs(self.z1-x)},{(self.z1-x).angle()},{(self.z2-x).angle()})"
        # mod 2 is without both draw command and first point
        if mod == 2:
            if self.z1.is_infinity():
                return f"-- {self.z2}"
            if self.z2.is_infinity():
                return f"-- {H.repr_infinity(self.z1.x)}"
            if abs(self.z1.x - self.z2.x) < EPSILON:
                return f"-- {self.z2}"
            x = self.center()
            return f"-- arc({(x, 0)},{abs(self.z1-x)},{(self.z1-x).angle()},{(self.z2-x).angle()})"
        
        if self.z1.is_infinity():
            return f"draw({H.repr_infinity(self.z2.x)} -- {self.z2}, {linewidth});\n"
        if self.z2.is_infinity():
            return f"draw({self.z1} -- {H.repr_infinity(self.z1.x)}, {linewidth});\n"
        if abs(self.z1.x - self.z2.x) < EPSILON:
            return f"draw({self.z1} -- {self.z2}, {linewidth});\n"
        x = self.center()
        return f"draw(arc({(x, 0)},{abs(self.z1-x)},{(self.z1-x).angle()},{(self.z2-x).angle()}), {linewidth});\n"
    
    # latex/tikz code to draw this
    def to_tex(self, mod=0):
        # mod 1 is without draw command
        if mod == 1:
            if self.z1.is_infinity():
                return f"{H.repr_infinity(self.z2.x)} -- {self.z2}"
            if self.z2.is_infinity():
                return f"{self.z1} -- {H.repr_infinity(self.z1.x)}"
            if abs(self.z1.x - self.z2.x) < EPSILON:
                return f"{self.z1} -- {self.z2}"
            x = self.center()
            return f"{self.z1} arc ({(self.z1-x).angle()}:{(self.z2-x).angle()}:{abs(self.z1-x)})"
        # mod 2 is without both draw command and first point
        if mod == 2:
            if self.z1.is_infinity():
                return f"-- {self.z2}"
            if self.z2.is_infinity():
                return f"-- {H.repr_infinity(self.z1.x)}"
            if abs(self.z1.x - self.z2.x) < EPSILON:
                return f"-- {self.z2}"
            x = self.center()
            return f"arc ({(self.z1-x).angle()}:{(self.z2-x).angle()}:{abs(self.z1-x)})"

        if self.z1.is_infinity():
            return f"\draw[very thick] {H.repr_infinity(self.z2.x)} -- {self.z2};\n"
        if self.z2.is_infinity():
            return f"\draw[very thick] {self.z1} -- {H.repr_infinity(self.z1.x)};\n"
        if abs(self.z1.x - self.z2.x) < EPSILON:
            return f"\draw[very thick] {self.z1} -- {self.z2};\n"
        x = self.center()
        return f"\draw[very thick] {self.z1} arc ({(self.z1-x).angle()}:{(self.z2-x).angle()}:{abs(self.z1-x)});\n"

class HyperbolicTriangle:
    def __init__(self, z1, z2, z3):
        self.z1, self.z2, self.z3 = z1, z2, z3

    # asymptote code to draw this
    def to_asy(self, label=None):
        a, b, c = self.z1, self.z2, self.z3
        if a.is_infinity():
            c, a = a, c
        if b.is_infinity():
            b, c = c, b
        x = (a.x + b.x) / 2 if c.is_infinity() else (a.x + b.x + c.x) / 3
        y = sum(map(lambda u: MAX_HEIGHT if u is None else u, (a.y, b.y, c.y))) / 3
        linewidth = "linewidth(1.5pt)"
        # return f"filldraw((0, 0) -- (5, 0) -- (0, 5) -- cycle, grey, {linewidth});\n"
        return f"fill({HyperbolicLine(c, a).to_asy(mod=1)} {HyperbolicLine(a, b).to_asy(mod=2)} {HyperbolicLine(b, c).to_asy(mod=2)} -- cycle, RGB(204, 204, 204));\n" + f"draw({HyperbolicLine(c, a).to_asy(mod=1)} {HyperbolicLine(a, b).to_asy(mod=2)} {HyperbolicLine(b, c).to_asy(mod=2)}, {linewidth});\n" + ("" if label is None else f"label(\"\\tiny ${label}$\",({x}, {y}));\n")
    
    # latex/tikz code to draw this
    def to_tex(self, label=None):
        a, b, c = self.z1, self.z2, self.z3
        if a.is_infinity():
            c, a = a, c
        if b.is_infinity():
            b, c = c, b
        x = (a.x + b.x) / 2 if c.is_infinity() else (a.x + b.x + c.x) / 3
        y = sum(map(lambda u: MAX_HEIGHT if u is None else u, (a.y, b.y, c.y))) / 3
        return f"\\draw[very thick,fill=gray!30] {HyperbolicLine(c, a).to_tex(mod=1)} {HyperbolicLine(a, b).to_tex(mod=2)} {HyperbolicLine(b, c).to_tex(mod=2)};\n" + ("" if label is None else f"\\node[] at ({x}, {y}) {{\\tiny ${label}$}};\n")
