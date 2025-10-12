"""
Эллиптическая точка
"""

class ECPoint:
    def __init__(self, x, y, is_infinity=False):
        self.x = x
        self.y = y
        self.is_infinity = is_infinity

    def __eq__(self, other):
        if not isinstance(other, ECPoint):
            return False
        if self.is_infinity and other.is_infinity:
            return True
        if self.is_infinity != other.is_infinity:
            return False
        return self.x == other.x and self.y == other.y
    
    def __neg__(self):
        if self.is_infinity:
            return ECPoint(None, None, True)
        return ECPoint(self.x, -self.y)
    
    def __repr__(self):
        if self.is_infinity:
            return "(X, X)"
        return f"({self.x}, {self.y})"
    
    def __hash__(self):
        if self.is_infinity:
            return hash((None, None, True))
        return hash((self.x, self.y, False))