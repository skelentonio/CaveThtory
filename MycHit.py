_gKey = const(0)
_gKeyTrg = const(1)
_gKeyLeft = const(0x00000001)
_gKeyRight = const(0x00000002)
_gWaterY = const(0x1e0000) # 240 * 0x10 * 0x200
_gWaterY_surface = const(_gWaterY + (4 * 0x200))

_LEFT = const(0)
_TOP = const(1)
_RIGHT = const(2)
_BOTTOM = const(3)
_FRONT = const(0)
_BACK = const(2)

_MYCHAR_cond = const(0)
_MYCHAR_flag = const(1)
_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_MYCHAR_xm = const(11)
_MYCHAR_ym = const(12)

class MycHit:
    def __init__(self, MyChar, gMap, g_GameFlags):
        self.MyChar = MyChar
        self.gMap = gMap
        self.g_GameFlags = g_GameFlags
        self.offx = bytearray([0, 1, 0, 1])
        self.offy = bytearray([0, 0, 1, 1])
        
    @micropython.viper
    def PutlittleStar(self):
        pass
    
    @micropython.viper
    def JudgeHitMyCharBlock(self, x: int, y: int) -> int:
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_hit = ptr16(gMC.hit)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        gMC_xm = gMC_i[_MYCHAR_xm]
        gMC_ym = gMC_i[_MYCHAR_ym]
        gMC_hit_top = gMC_hit[_TOP]
        gMC_hit_back = gMC_hit[_BACK]
        gMC_hit_bottom = gMC_hit[_BOTTOM]
        KeyControl_i = ptr8(self.MyChar.KeyControl.i)
        gKey = KeyControl_i[_gKey]
        x *= 0x10
        y *= 0x10

        hit = 0
        if (gMC_y - gMC_hit_top < (y + 4) * 0x200
            and gMC_y + gMC_hit_bottom > (y - 4) * 0x200):
            # Left wall
            if (gMC_x - gMC_hit_back < (x + 8) * 0x200
                and gMC_x - gMC_hit_back > x * 0x200):
                # Clip
                gMC_x = ((x + 8) * 0x200) + gMC_hit_back
                # Halt momentum
                if gMC_xm < -0x180:
                    gMC_xm = -0x180
                if not gKey & _gKeyLeft and gMC_xm < 0:
                    gMC_xm = 0
                # Set that a left wall was hit
                hit |= 1

            # Right wall
            if (gMC_x + gMC_hit_back > (x - 8) * 0x200
                and gMC_x + gMC_hit_back < x * 0x200):
                # Clip
                gMC_x = ((x - 8) * 0x200) - gMC_hit_back
                # Halt momentum
                if gMC_xm > 0x180:
                    gMC_xm = 0x180
                if not gKey & _gKeyRight and gMC_xm > 0:
                    gMC_xm = 0
                # Set that a right wall was hit
                hit |= 4

        
        if gMC_x - gMC_hit_back < (x + 5) * 0x200:
            # Ceiling
            if (gMC_x + gMC_hit_back > (x - 5) * 0x200
                and gMC_y - gMC_hit_top < (y + 8) * 0x200
                and gMC_y - gMC_hit_top > y * 0x200):
                # Clip
                gMC_y = ((y + 8) * 0x200) + gMC_hit_top
                # Halt momentum
                if (gMC_i[_MYCHAR_cond] & 2) == 0 and gMC_ym < -0x200:
                    self.PutlittleStar()
                if gMC_ym < 0:
                    gMC_ym = 0
                # Set that a ceiling was hit
                hit |= 2

        # Floor
            if (gMC_x + gMC_hit_back > ((x - 5) * 0x200)
                and gMC_y + gMC_hit_bottom > (y - 8) * 0x200
                and gMC_y + gMC_hit_bottom < y * 0x200):
                # Clip
                gMC_y = ((y - 8) * 0x200) - gMC_hit_top
                # Halt momentum
                #if (gMC_ym > 0x400):
                #    PlaySoundObject(23, SOUND_MODE_PLAY)
                if gMC_ym > 0:
                    gMC_ym = 0
                # Set that a floor was hit
                hit |= 8
            
        gMC_i[_MYCHAR_x] = gMC_x
        gMC_i[_MYCHAR_y] = gMC_y
        gMC_i[_MYCHAR_xm] = gMC_xm
        gMC_i[_MYCHAR_ym] = gMC_ym
        return hit

    @micropython.viper
    def JudgeHitMyCharTriangleUp(self, x: int, y: int, angle: int) -> int:
        # combines ceiling slope collision JudgeHitMyCharTriangleA, B, C, D
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_hit = ptr16(gMC.hit)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        hit = 0
        x *= 0x10
        y *= 0x10
        
        a = 0x800
        if angle == 1 or angle == 2:
            a = 0-a
        b = (gMC_x - x * 0x200) // 2
        if angle == 0 or angle == 1:
            b = 0-b
        
        if (gMC_x < (x + 8) * 0x200
            and gMC_x > (x - 8) * 0x200
            and gMC_y - gMC_hit[_TOP] < (y * 0x200) + b + a
            and gMC_y + gMC_hit[_BOTTOM] > (y - 8) * 0x200):
        
            # Clip
            gMC_i[_MYCHAR_y] = (y * 0x200) + b + a + gMC_hit[_TOP]
            # Halt momentum
            if not (gMC_i[_MYCHAR_cond] & 2) and gMC_i[_MYCHAR_ym] < -0x200:
                self.PutlittleStar()
            if (gMC_i[_MYCHAR_ym] < 0):
                gMC_i[_MYCHAR_ym] = 0
            # Set that hit a ceiling
            hit = 2
        
        return hit
    
    @micropython.viper
    def JudgeHitMyCharTriangleDown(self, x: int, y: int, angle: int) -> int:
        # combines floor slope collision JudgeHitMyCharTriangleE, F, G, H
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_hit = ptr16(gMC.hit)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        hit = 1 << (0x10 + angle)
        x *= 0x10
        y *= 0x10
        
        a = 0x800
        if angle == 0 or angle == 3:
            a = 0-a
        b = (gMC_x - x * 0x200) // 2
        if angle == 2 or angle == 3:
            b = 0-b
        
        if (gMC_x < (x + 8) * 0x200
            and gMC_x > (x - 8) * 0x200
            and gMC_y + gMC_hit[_BOTTOM] > (y * 0x200) + b + a
            and gMC_y - gMC_hit[_TOP] < (y + 8) * 0x200):
        
            # Clip
            gMC_i[_MYCHAR_y] = (y * 0x200) + b + a - gMC_hit[_BOTTOM]
            # Halt momentum
            #if (gMC_i[_MYCHAR_ym] > 0x400):
            #    PlaySoundObject(23, SOUND_MODE_PLAY)
            if (gMC_i[_MYCHAR_ym] > 0):
                gMC_i[_MYCHAR_ym] = 0
            # Set that hit this slope
            if angle == 0 or angle == 1:
                hit |= 0x28
            else:
                hit |= 0x18
        
        return hit
    
    @micropython.viper
    def JudgeHitMyCharWater(self, x: int, y: int) -> int:
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_hit = ptr16(gMC.hit)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        gMC_hit_back = gMC_hit[_BACK]
        hit = 0
        x *= 0x10
        y *= 0x10
        if (gMC_x - gMC_hit_back < (x + 5) * 0x200
            and gMC_x + gMC_hit_back > ((x - 5) * 0x200)
            and gMC_y - gMC_hit[_TOP] < ((y + 5) * 0x200)
            and gMC_y + int(gMC_hit[_BOTTOM] )> y * 0x200):
            hit |= 0x100
        return hit
    
    @micropython.viper
    def JudgeHitMyCharDamage(self, x: int, y: int, angle: int) -> int:
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        hit = 0
        x *= 0x10
        y *= 0x10
        if (gMC_x - 0x800 < (x + 4) * 0x200
            and gMC_x + 0x800 > (x - 4) * 0x200
            and gMC_y - 0x800 < (y + 3) * 0x200
            and gMC_y + 0x800 > (y - 3) * 0x200):
            if angle == 0:
                hit = 0x400
            else:
                hit = 0xD00
        return hit
    
    @micropython.viper
    def JudgeHitMyCharVect(self, x: int, y: int, angle: int) -> int:
        # combines JudgeHitMyCharVectLeft, Up, Right, Down
        gMC = self.MyChar.gMC
        gMC_i = ptr32(gMC.i)
        gMC_hit = ptr16(gMC.hit)
        gMC_x = gMC_i[_MYCHAR_x]
        gMC_y = gMC_i[_MYCHAR_y]
        gMC_hit_back = gMC_hit[_BACK]
        hit = 0
        x *= 0x10
        y *= 0x10
        if (gMC_x - gMC_hit_back < (x + 6) * 0x200
            and gMC_x + gMC_hit_back > (x - 6) * 0x200
            and gMC_y - gMC_hit[_TOP] < (y + 6) * 0x200
            and gMC_y + gMC_hit[_BOTTOM] > (y - 6) * 0x200):
            hit = 1 << (0x0c + angle)
        return hit

    @micropython.viper
    def HitMyCharMap(self):
        gMC_i = ptr32(self.MyChar.gMC.i)
        flag = 0 # ResetMyCharFlag
        gMap_width = int(self.gMap.width)
        gMap_length = int(self.gMap.length)
        gMap_data = ptr8(self.gMap.data)
        gMap_atrb = ptr8(self.gMap.atrb)
        offx = ptr8(self.offx)
        offy = ptr8(self.offy)
        x = gMC_i[_MYCHAR_x] // 0x10 // 0x200
        y = gMC_i[_MYCHAR_y] // 0x10 // 0x200

        for i in range(4):
            # GetAttribute
            posx = x + offx[i]
            posy = y + offy[i]
            if posx < 0 or posy < 0 or posx >= gMap_width or posy >= gMap_length:
                continue
            tile_id = gMap_data[posx + (posy * gMap_width)]
            atrb = gMap_atrb[tile_id]
            if atrb == 0:
                continue
            a = atrb & 0xfc
            b = atrb & 0x03
        
            # Block
            if atrb == 0x05 or atrb == 0x41 or atrb == 0x43 or atrb == 0x46 or atrb == 0x61:
                flag |= int(self.JudgeHitMyCharBlock(posx, posy))
            # Slopes & water slopes
            elif a == 0x50 or a == 0x70: #0x50 to 0x53, or 0x70 to 0x73
                flag |= int(self.JudgeHitMyCharTriangleUp(posx, posy, b))
            elif a == 0x54 or a == 0x74: #0x54 to 0x57, or 0x74 to 0x77
                flag |= int(self.JudgeHitMyCharTriangleDown(posx, posy, b))
            # Wind & water current
            elif a == 0x80: #0x80 to 0x83
                flag |= int(self.JudgeHitMyCharVect(posx, posy, b))
            elif a == 0xa0: #0xa0 to 0xa3
                flag |= int(self.JudgeHitMyCharVect(posx, posy, b))
            # Spikes
            elif atrb == 0x42:
                flag |= int(self.JudgeHitMyCharDamage(posx, posy, 0))
            # Water spikes
            elif atrb == 0x62:
                flag |= int(self.JudgeHitMyCharDamage(posx, posy, 1))
            # Water
            if a == 0x60 or a == 0x70 or a == 0xa0 or atrb == 0x02:
                flag |= int(self.JudgeHitMyCharWater(posx, posy))

        if gMC_i[_MYCHAR_y] > _gWaterY_surface:
            flag |= 0x100
        
        gMC_i[_MYCHAR_flag] = flag
