
class Enum(object):
    """Simple implementation of an enum"""
    def __init__(self, *enum_attrs):
        i = 0
        for attr in enum_attrs:
            setattr(self, attr, i)
            i += 1
    
    def __iter__(self):
        return vars(self).values().__iter__()