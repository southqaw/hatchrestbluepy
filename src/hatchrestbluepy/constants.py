from enum import IntEnum

COLOR_GRADIENT = (254, 254, 254)  # setting this color turns on Gradient mode
SERV_TX = "02240001-5EFD-47EB-9C1A-DE53F7A2B232"
CHAR_TX = "02240002-5efd-47eb-9c1a-de53f7a2b232"
SERV_FEEDBACK = "02260001-5efd-47eb-9c1a-de53f7a2b232"
CHAR_FEEDBACK = "02260002-5efd-47eb-9c1a-de53f7a2b232"
MAC_PREFIX = "F3:53:11"


class HatchRestSound(IntEnum):
    none = 0
    stream = 2
    noise = 3
    dryer = 4
    ocean = 5
    wind = 6
    rain = 7
    bird = 9
    crickets = 10
    brahms = 11
    twinkle = 13
    rockabye = 14
