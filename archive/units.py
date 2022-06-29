from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def set(cls):
        return set(map(lambda c: c.value, cls))
    
    @classmethod
    def getUnit(cls, val):
        l =  list(map(lambda c: c.value, cls))
        print(l)
        return l[l.index(val)]
    
    

class LongUnits(ExtendedEnum):
    DDD = 3
    DDDMM = 5
    DDDMMSS = 7

    @classmethod
    def set(cls):
        return set(map(lambda c: c.value, cls))

class LatUnits(ExtendedEnum):
    DD = 2
    DDMM = 4
    DDMMSS = 6