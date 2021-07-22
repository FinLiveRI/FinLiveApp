

def dictTolist(data):
    result = []
    if isinstance(data, dict) and data.__len__() > 0:
        result.append(data)
    elif isinstance(data, list) and data.__len__() > 0:
        result = data
    else:
        result = None
    return result
