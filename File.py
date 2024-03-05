import struct

def OpenFile(path, perm):
    try:
        fp = open(path, perm)
        return fp
    except:
        return False

@micropython.viper
def File_ReadBE32(stream) -> int:
    return int(struct.unpack(">I", stream.read(4))[0])

@micropython.viper
def File_ReadLE16(stream) -> int:
    return int(struct.unpack("<H", stream.read(2))[0])

@micropython.viper
def File_ReadLE32(stream) -> int:
    return int(struct.unpack("<I", stream.read(4))[0])
