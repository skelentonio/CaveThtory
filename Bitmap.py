import gc
from array import array
import File
gc.collect()

@micropython.viper
def RECT(top, left, bottom, right):
    return array('h', [left, top, right, bottom])
_LEFT = const(0)
_TOP = const(1)
_RIGHT = const(2)
_BOTTOM = const(3)

@micropython.viper
def ReadRows(data: ptr8, width: int, height: int):
    bytes_per_row = width // 0x08
    byte_count = bytes_per_row * height
    pixel_padding = bytes_per_row % 4
    image_buffer = bytearray(byte_count - (pixel_padding * height))
    ptr = ptr8(image_buffer)
    i = 0
    k = 0
    l = 0
    while i < byte_count:
        j = 0
        while j < bytes_per_row:
            ptr[k] = data[l]
            j += 1
            k += 1
            l += 1
        l += pixel_padding
        i += bytes_per_row
    return image_buffer

@micropython.viper
def ReadCols(data: ptr8, width: int, height: int):
    bytes_per_row = width // 0x08
    byte_count = bytes_per_row * height
    pixel_padding = bytes_per_row % 4
    image_buffer = bytearray(byte_count - (pixel_padding * height))
    ptr = ptr8(image_buffer)
    block_count = (height // 8)
    block = 0
    k = 0
    while block < block_count:
        i = 0
        a = byte_count - ((block + 1) * 8 * bytes_per_row)
        while i < width:
            column = 0
            j = 0
            shift = i % 8
            mask = 0x80 >> shift
            b = a + (i // 8)
            while j < 8:
                column |= ((data[(bytes_per_row * j) + b] & mask) << shift) >> j
                j += 1
            ptr[k] = column
            i += 1
            k += 1
        block += 1
    return image_buffer

@micropython.viper
def DecodeBitmapFromFile(path, crop: ptr16):
    # Open file
    fp = File.OpenFile(path, "rb")

    if "BM" not in fp.read(2):  # identifier, always "BM"
        print("Not a valid bmp: " + path)
        fp.close()
        return None

    size = int(File.File_ReadLE32(fp))  # 4 bytes, size of bmp file
    fp.seek(0x0a)  # junk data
    pixel_offset = int(File.File_ReadLE32(fp))
    fp.seek(0x12)  # header size
    width = int(File.File_ReadLE32(fp))  # width also controls how many bits per line in the pixel data
    height = int(File.File_ReadLE32(fp))  # only effects overall size of file
    fp.read(2)  # color planes
    bpp = int(File.File_ReadLE16(fp))  # bits per pixel

    if bpp != 1:
        print("Image must be indexed with 2 colors: " + path)
        fp.close()
        return None

    bytes_per_row = width // 0x08 # must be multiple of 8
    byte_count = bytes_per_row * height
    
    # crop just the part of the bmp we need
    if crop[_LEFT] | crop[_TOP] | crop[_RIGHT] | crop[_BOTTOM]:
        pixel_offset += (height - crop[_BOTTOM]) * bytes_per_row
        height = crop[_BOTTOM] - crop[_TOP]
        byte_count = bytes_per_row * height

    # read data
    fp.seek(pixel_offset)
    data = fp.read(byte_count)
    fp.close()
    gc.collect()
    
    return ReadCols(ReadRows(data, width, height), width, height), width, height
