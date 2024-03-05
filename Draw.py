import gc
from array import array
import Bitmap

_gDataPath = "/Games/CaveStory/data"

@micropython.viper
def RECT(top, left, bottom, right):
    return array('h', [left, top, right, bottom])
_LEFT = const(0)
_TOP = const(1)
_RIGHT = const(2)
_BOTTOM = const(3)

class BitmapImage:
    @micropython.viper
    def __init__(self, image, width, height):
        self.image = image
        self.width = width
        self.height = height
        
@micropython.viper
def CutTile(sheet_image: ptr8, sheet_width: int, rect: ptr16, crop: ptr16):
    top = rect[_TOP] - crop[_TOP]
    bottom = rect[_BOTTOM] - crop[_TOP]
    offset = rect[_LEFT] + ((top // 8) * sheet_width)
    #if top % 8 > 0:
    #    print("bad tile: " + str(rect))
    width = rect[_RIGHT] - rect[_LEFT]
    height = (bottom - top) // 8
    image_buffer = bytearray(width * height)
    ptr = ptr8(image_buffer)
    j = 0
    k = 0
    while j < height:
        i = 0
        while i < width:
            ptr[k] = sheet_image[offset + i]
            i += 1
            k += 1
        offset += sheet_width
        j += 1
    return image_buffer

@micropython.viper
def PreloadTiles(name, data: ptr8, size: int):
    path = _gDataPath + "/" + name + ".bmp"
    tiles = []
    i = 0
    sheet_loaded = False
    while i < 256: # tile count, no tilesheets exceed 256x256
        if i % 16 == 0:
            sheet_loaded = False
        # check if the tile is actually used in the map
        found = False
        for j in range(size):
            if data[j] == i:
                found = True
                break
        if found:
            left = (i % 16) * 16
            top = (i // 16) * 16
            # grab next row of tilesheet
            if not sheet_loaded:
                crop = RECT(top, 0, top + 16, 0)
                image_buffer, width, height = Bitmap.DecodeBitmapFromFile(path, crop)
                gc.collect()
                sheet_loaded = True
            tiles.append(CutTile(image_buffer, width, RECT(top, left, top + 16, left + 16), crop))
        else:
            # insert a dummy tile, since it isn't used by the map
            tiles.append(0)
        i += 1
    return tiles

@micropython.viper
def PreloadSprites(path, stencil):
    tiles = []
    tile_count = int(len(stencil))
    path = _gDataPath + "/" + path + ".bmp"

    # uses less ram/cpu while reading a bmp, by only read the part we need
    crop = RECT(512, 512, 0, 0)
    crop_ptr = ptr16(crop)
    for i in range(tile_count):
        rect = ptr16(stencil[i])
        if rect[_TOP] < crop_ptr[_TOP]:
            crop_ptr[_TOP] = rect[_TOP]
        if rect[_BOTTOM] > crop_ptr[_BOTTOM]:
            crop_ptr[_BOTTOM] = rect[_BOTTOM]
    image_buffer, width, height = Bitmap.DecodeBitmapFromFile(path, crop)

    i = 0
    while i < tile_count:
        tiles.append(CutTile(image_buffer, width, stencil[i], crop))
        i += 1
    return tiles
