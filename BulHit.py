_BULLET_MAX = const(0x08) # vanilla 0x40
_BULLET_flag = const(0)
_BULLET_code_bullet = const(1)
_BULLET_bbits = const(2)
_BULLET_cond = const(3)
_BULLET_x = const(4)
_BULLET_y = const(5)
_BULLET_blockXL = const(22)
_BULLET_blockYL = const(23)

class BulHit:
    def __init__(self, Bullet, gMap):
        self.Bullet = Bullet
        self.gMap = gMap
        self.offx = bytearray([0, 1, 0, 1])
        self.offy = bytearray([0, 0, 1, 1])
        
    @micropython.viper
    def Vanish(self, bul_i: ptr32):
        #if (bul_i[_BULLET_code_bullet] != 37 and bul_i[_BULLET_code_bullet] != 38 and bul_i[_BULLET_code_bullet] != 39)
        #    PlaySoundObject(28, SOUND_MODE_PLAY)
        #else
        #    SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_PROJECTILE_DISSIPATION, DIR_UP)
        #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_PROJECTILE_DISSIPATION, DIR_RIGHT)
        bul_i[_BULLET_cond] = 0
    
    @micropython.viper
    def JudgeHitBulletBlock(self, x: int, y: int, atrb: int, bul_i: ptr32) -> int:
        bul_x = bul_i[_BULLET_x]
        bul_y = bul_i[_BULLET_y]
        blockXL = bul_i[_BULLET_blockXL]
        blockYL = bul_i[_BULLET_blockYL]
        x *= 0x10
        y *= 0x10
        hit = 0
        if (bul_x - blockXL < (x + 8) * 0x200
            and bul_x + blockXL > (x - 8) * 0x200
            and bul_y - blockYL < (y + 8) * 0x200
            and bul_y + blockYL > (y - 8) * 0x200):
            hit |= 0x200

        if hit and bul_i[_BULLET_bbits] & 0x60 and atrb == 0x43:
            ## this is probably for bullets hitting breakable blocks
            if not bul_i[_BULLET_bbits] & 0x40:
                bul_i[_BULLET_cond] = 0

            #SetCaret(bul_x, bul_y, CARET_PROJECTILE_DISSIPATION, DIR_LEFT)
            #PlaySoundObject(12, SOUND_MODE_PLAY)

            #for (i = 0 i < 4 ++i)
                #SetNpChar(4, x * 0x200 * 0x10, y * 0x200 * 0x10, Random(-0x200, 0x200), Random(-0x200, 0x200), 0, NULL, 0x100)

            #ShiftMapParts(x, y)

        return hit
    
    @micropython.viper
    def JudgeHitBulletBlock2(self, x: int, y: int, atrb: ptr8, bul_i: ptr32) -> int:
        bul_x = bul_i[_BULLET_x]
        bul_y = bul_i[_BULLET_y]
        blockXL = bul_i[_BULLET_blockXL]
        blockYL = bul_i[_BULLET_blockYL]
        block = bytearray([0, 0, 0, 0])
        hit = 0

        if bul_i[_BULLET_bbits] & 0x40:
            for i in range(4):
                if atrb[i] == 0x41 or atrb[i] == 0x61:
                    block[i] = True
                else:
                    block[i] = False
        else:
            for i in range(4):
                if atrb[i] == 0x41 or atrb[i] == 0x43 or atrb[i] == 0x61:
                    block[i] = True
                else:
                    block[i] = False
        
        workX = ((x * 0x10) + 8) * 0x200
        workY = ((y * 0x10) + 8) * 0x200

        # Left wall
        if block[0] and block[2]:
            if bul_x - blockXL < workX:
                hit |= 1
        elif block[0] and not block[2]:
            if bul_x - blockXL < workX and bul_y - blockYL < workY - 0x600:
                hit |= 1
        elif not block[0] and block[2]:
            if bul_x - blockXL < workX and bul_y + blockYL > workY + 0x600:
                hit |= 1

        # Right wall
        if block[1] and block[3]:
            if bul_x + blockXL > workX:
                hit |= 4
        elif block[1] and not block[3]:
            if bul_x + blockXL > workX and bul_y - blockYL < workY - 0x600:
                hit |= 4
        elif not block[1] and block[3]:
            if bul_x + blockXL > workX and bul_y + blockYL > workY + 0x600:
                hit |= 4

        # Ceiling
        if block[0] and block[1]:
            if bul_y - blockYL < workY:
                hit |= 2
        elif block[0] and not block[1]:
            if bul_y - blockYL < workY and bul_x - blockXL < workX - 0x600:
                hit |= 2
        elif not block[0] and block[1]:
            if bul_y - blockYL < workY and bul_x + blockXL > workX + 0x600:
                hit |= 2

        # Ground
        if block[2] and block[3]:
            if bul_y + blockYL > workY:
                hit |= 8
        elif block[2] and not block[3]:
            if bul_y + blockYL > workY and bul_x - blockXL < workX - 0x600:
                hit |= 8
        elif not block[2] and block[3]:
            if bul_y + blockYL > workY and bul_x + blockXL > workX + 0x600:
                hit |= 8

        # Clip
        if bul_i[_BULLET_bbits] & 8:
            if hit & 1:
                bul_i[_BULLET_x] = workX + blockXL
            elif hit & 4:
                bul_i[_BULLET_x] = workX - blockXL
            elif hit & 2:
                bul_i[_BULLET_y] = workY + blockYL
            elif hit & 8:
                bul_i[_BULLET_y] = workY - blockYL
        else:
            if hit & 0xF:
                self.Vanish(bul_i)

        return hit
    
    @micropython.viper
    def JudgeHitBulletTriangleUp(self, x: int, y: int, angle: int, bul_i: ptr32) -> int:
        bul_x = bul_i[_BULLET_x]
        bul_y = bul_i[_BULLET_y]
        x *= 0x10
        y *= 0x10
        hit = 0
        
        a = (bul_x - (x * 0x200)) // 2
        if angle == 0 or angle == 1:
            a = 0-a
        b = 0x800
        c = 0xc00
        if angle == 1 or angle == 2:
            b = -0x800
            c = -0x400
        
        if (bul_x < (x + 8) * 0x200
            and bul_x > (x - 8) * 0x200
            and bul_y - 0x400 < (y * 0x200) + a + b
            and bul_y + 0x400 > (y - 8) * 0x200):
        
            if bul_i[_BULLET_bbits] & 8:
                bul_i[_BULLET_y] = (y * 0x200) + a + c
            else:
                self.Vanish(bul_i)
            if angle == 0 or angle == 1:
                hit = 0x82
            else:
                hit = 0x42
        
        return hit

    @micropython.viper
    def JudgeHitBulletTriangleDown(self, x: int, y: int, angle: int, bul_i: ptr32) -> int:
        bul_x = bul_i[_BULLET_x]
        bul_y = bul_i[_BULLET_y]
        x *= 0x10
        y *= 0x10
        hit = 0
        
        a = 0x800
        b = 0x400
        if angle == 0 or angle == 3:
            a = -0x800
            b = -0xc00
        c = (bul_x - (x * 0x200)) // 2
        if angle == 2 or angle == 3:
            c = 0-c
        e = bul_x
        if angle == 0:
            e -= 0x200
        
        if (bul_x < (x + 8) * 0x200
            and e > (x - 8) * 0x200
            and bul_y + 0x400 > (y * 0x200) + c + a
            and bul_y - 0x400 < (y + 8) * 0x200):
        
            if bul_i[_BULLET_bbits] & 8:
                bul_i[_BULLET_y] = (y * 0x200) + c + b
            else:
                self.Vanish(bul_i)
            if angle == 0 or angle == 1:
                hit = 0x28
            else: 
                hit = 0x18
        
        return hit
    
    @micropython.viper
    def HitBulletMap(self):
        gBul = self.Bullet.gBul
        gMap = self.gMap
        gMap_width = int(gMap.width)
        gMap_length = int(gMap.length)
        gMap_data = ptr8(gMap.data)
        gMap_atrb = ptr8(gMap.atrb)
        offx = ptr8(self.offx)
        offy = ptr8(self.offy)
        
        for i in range(_BULLET_MAX):
            bul = gBul[i]
            bul_i = ptr32(bul.i)
            if not bul_i[_BULLET_cond] & 0x80:
                continue
            flag = 0
            x = bul_i[_BULLET_x] // 0x10 // 0x200
            y = bul_i[_BULLET_y] // 0x10 // 0x200
            
            if not bul_i[_BULLET_bbits] & 4:
                atrb_arr = bytearray([0, 0, 0, 0])
                for j in range(4):
                    # GetAttribute
                    posx = x + offx[j]
                    posy = y + offy[j]
                    if posx < 0 or posy < 0 or posx >= gMap_width or posy >= gMap_length:
                        continue
                    tile_id = gMap_data[posx + (posy * gMap_width)]
                    atrb = gMap_atrb[tile_id]
                    atrb_arr[j] = atrb
                    a = atrb & 0xfc
                    b = atrb & 0x03

                    if atrb == 0x41 or atrb == 0x43 or atrb == 0x44 or atrb == 0x61 or atrb == 0x64:
                        flag |= int(self.JudgeHitBulletBlock(posx, posy, atrb, bul_i))

                    # Slopes & water slopes
                    elif a == 0x50 or a == 0x70:
                        flag |= int(self.JudgeHitBulletTriangleUp(posx, posy, b, bul_i))
                    elif a == 0x54 or a == 0x74:
                        flag |= int(self.JudgeHitBulletTriangleDown(posx, posy, b, bul_i))

                flag |= int(self.JudgeHitBulletBlock2(x, y, atrb_arr, bul_i))
            bul_i[_BULLET_flag] = flag
