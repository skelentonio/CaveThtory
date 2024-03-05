# cs scripts
from display import display
import File
import Draw

_gDataPath = "/Games/CaveStory/data"
_WindowWidth = const(72)
_WindowHeight = const(40)

class MAP_DATA():
	data = None
	atrb = None
	width = 0
	length = 0

class TILESHEET():
    tile = []
    mask = []
    fill = []

class Map:
    def __init__(self):
        self.gMap = MAP_DATA()
        self.sheet = TILESHEET()
    
    @micropython.native
    def LoadMapData2(self, path_map):
        # Get path
        path = _gDataPath + '/' + path_map

        # Open file
        fp = File.OpenFile(path, "rb")

        # Get width and height
        fp.read(4) # should be "PXM"
        gMap = self.gMap
        gMap.width = File.File_ReadLE16(fp)
        gMap.length = File.File_ReadLE16(fp)
        
        # check how many tiles to render on the screen, previously was in PutStage_Front
        self.num_x = int(min(gMap.width, ((_WindowWidth + 15) // 16) + 1))
        self.num_y = int(min(gMap.length, ((_WindowHeight + 15) // 16) + 1))
        
        # Read tile data
        gMap.data = fp.read(gMap.width * self.gMap.length)
        fp.close()
        
    @micropython.viper
    def LoadTiles(self, path):
        gMap = self.gMap
        sheet = self.sheet
        size = int(len(gMap.data))
        data = gMap.data
        sheet.tile = Draw.PreloadTiles(path, data, size)
        sheet.mask = Draw.PreloadTiles(path + "_mask", data, size)
        
        # check which tiles don't need a mask
        tile_count = int(len(sheet.mask))
        sheet.fill = bytearray(tile_count)
        mask = sheet.mask
        fill = ptr8(sheet.fill)
        for i in range(tile_count):
            ptr = ptr8(mask[i])
            fill[i] = True
            for j in range(32):
                if ptr[j] != 0xff:
                    fill[i] = False
                    break

    @micropython.viper
    def LoadAttributeData(self, path_atrb):
        # Open file
        path = _gDataPath + '/' + path_atrb
        fp = File.OpenFile(path, "rb")

        # Read data
        self.gMap.atrb = fp.read()
        fp.close()

    @micropython.viper
    def PutStage(self, fx: int, fy: int, layer: int):
        # Get range to draw
        put_x = int(max(0, ((fx // 0x200) + 8) // 16))
        put_y = int(max(0, ((fy // 0x200) + 8) // 16))
        range_x = put_x + int(self.num_x)
        range_y = put_y + int(self.num_y)
        coord_fx = (fx // 0x200) + 8
        coord_fy = (fy // 0x200) + 8
        display_blit = display.blit
        display_blitWithMask = display.blitWithMask
        
        gMap = self.gMap
        gMap_width = int(gMap.width)
        gMap_length = int(gMap.length)
        gMap_data = ptr8(gMap.data)
        gMap_atrb = ptr8(gMap.atrb)
        sheet = self.sheet
        tile = sheet.tile
        mask = sheet.mask
        fill = ptr8(sheet.fill)
 
        for j in range(put_y, range_y):
            if j >= gMap_length:
                break
            k = put_x + (j * gMap_width)
            for i in range(put_x, range_x):
                if i >= gMap_width:
                    k += 1
                    continue
                # Get attribute
                tile_id = gMap_data[k]
                atrb = gMap_atrb[tile_id]
                if layer == 0 and (atrb > 0x20 or not atrb):
                    k += 1
                    continue
                if layer == 1 and (not atrb & 0x40 or atrb & 0x80):
                    k += 1
                    continue
                # Draw tile
                if fill[tile_id]:
                    display_blit(tile[tile_id], i * 16 - coord_fx, j * 16 - coord_fy, 16, 16)
                else:
                    display_blitWithMask(tile[tile_id], i * 16 - coord_fx, j * 16 - coord_fy, 16, 16, mask[tile_id])
                k += 1
