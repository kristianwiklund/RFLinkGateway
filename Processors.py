import RangeDict

cardinal_pts_mapping = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW"
]

uv_mapping = RangeDict.RangeDict({
    range(0,3): 'LOW',
    range(3,6): 'MED',
    range(6,8): 'HI',
    range(8,11): 'V.HI',
    range(11,9999): 'EX.HI'
    })

wind_mapping = RangeDict.RangeDict({
    range(0,14): 'LIGHT',
    range(14,42): 'MODERATE',
    range(42,88): 'STRONG',
    range(88,999): 'STORM'
    })

def shex2dec(value):
    try:
        val = int(value, 16)
        if val >= 0x8000: val = -1*(val - 0x8000)
        return val
    except:
        pass
    return value

def hex2dec(value):
    try:
        return int(value, 16)
    except:
        pass
    return value

def str2dec(value):
    try:
        return int(value)
    except:
        pass
    return value

def div10(value):
    try:
        return value / 10
    except:
        pass
    return value

def dir2deg(value):
    try:
        v = int(value) * 22.5
        return v
    except:
        pass
    return value

def dir2car(value):
    try:
        dec = int(value)
        v = cardinal_pts_mapping[dec]
        return v
    except:
        pass
    return value

def uv2level(value):
    try:
        dec = int(value)
        return uv_mapping[dec]
    except:
        pass
    return value

def wind2level(value):
    try:
        dec = int(value)
        return wind_mapping[dec]
    except:
        pass
    return value

processors = {
        "shex2dec" : shex2dec,
        "hex2dec" : hex2dec,
        "str2dec" : str2dec,
        "dir2deg" : dir2deg,
        "dir2car" : dir2car,
        "div10" : div10,
        "uv2level" : uv2level,
        "wind2level" : wind2level
}
