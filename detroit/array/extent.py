import math

def extent(values, valueof=None):
    mini = None
    maxi = None
    if valueof is None:
        for value in values:
            if value is not None and (isinstance(value, str) or not math.isnan(value)):
                if mini is None:
                    mini = maxi = value
                else:
                    if mini > value:
                        mini = value
                    if maxi < value:
                        maxi = value
    else:
        index = -1
        for value in values:
            new_value = valueof(value, index := index + 1, values)
            if new_value is not None and (isinstance(new_value, str) or not math.isnan(new_value)):
                value = new_value
                if mini is None:
                    mini = maxi = value
                else:
                    if mini > value:
                        mini = value
                    if maxi < value:
                        maxi = value
    return [mini, maxi]

