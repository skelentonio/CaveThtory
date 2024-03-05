from machine import Pin

_KEY_LEFT = const(0x00000001)
_KEY_RIGHT = const(0x00000002)
_KEY_UP = const(0x00000004)
_KEY_DOWN = const(0x00000008)
_KEY_MAP = const(0x00000010)
_KEY_SHOT = const(0x00000020)
_KEY_JUMP = const(0x00000040)
_KEY_ARMS = const(0x00000080)
_KEY_ARMSREV = const(0x00000100)
_KEY_F1 = const(0x00000400)
_KEY_F2 = const(0x00000800)
_KEY_ITEM = const(0x00001000)
_KEY_OK = const(0x00002000)
_KEY_CANCEL = const(0x00004000)
_KEY_ESCAPE = const(0x00008000)
_KEY_PAUSE = const(0x00010000)

_gKey = const(0)
_gKeyTrg = const(1)

swL = Pin(3, Pin.IN, Pin.PULL_UP)  # D-pad left
swR = Pin(5, Pin.IN, Pin.PULL_UP)  # D-pad right
swU = Pin(4, Pin.IN, Pin.PULL_UP)  # D-pad up
swD = Pin(6, Pin.IN, Pin.PULL_UP)  # D-pad down
swA = Pin(27, Pin.IN, Pin.PULL_UP)  # right (A) action button
swB = Pin(24, Pin.IN, Pin.PULL_UP)  # left (B) action button

class KeyControl:
    def __init__(self):
        self.i = bytearray([0, 0])

    @micropython.viper
    def GetTrg(self):
        gKey = 0
        if not swL.value():
            gKey |= _KEY_LEFT
        if not swR.value():
            gKey |= _KEY_RIGHT
        if not swU.value():
            gKey |= _KEY_UP
        if not swD.value():
            gKey |= _KEY_DOWN
        if not swA.value():
            gKey |= _KEY_SHOT
        if not swB.value():
            gKey |= _KEY_JUMP
        self_i = ptr8(self.i)
        key_old = self_i[_gKey]
        gKeyTrg = gKey ^ key_old
        gKeyTrg = gKey & gKeyTrg
        self_i[_gKey] = gKey
        self_i[_gKeyTrg] = gKeyTrg
