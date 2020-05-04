from datetime import datetime


class Utils:
    @staticmethod
    def get_dict(obj):
        res = {}
        for key, val in vars(obj).items():
            if key[:1] != '_':
                if isinstance(val, datetime):
                    val = val.__str__()
                res[key] = val
        return res

    @staticmethod
    def set_vars(obj1, obj2):
        for a in obj2.__dict__:
            if a[:1] != '_':
                setattr(obj1, a, getattr(obj2, a))
