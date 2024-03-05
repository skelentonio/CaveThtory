import gc
from array import array
from random import randrange
from display import display
from Draw import PreloadSprites

_CARET_EXHAUST = const(7)
_BULLET_MAX = const(0x08) # vanilla 0x40
_DIR_LEFT = const(0)
_DIR_UP = const(1)
_DIR_RIGHT = const(2)
_DIR_DOWN = const(3)

_MYCHAR_direct = const(2)
_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_MYCHAR_xm = const(11)

@micropython.viper
def _RECT(left, top, right, bottom):
    return array('h', [left, top, right, bottom])
_LEFT = const(0)
_TOP = const(1)
_RIGHT = const(2)
_BOTTOM = const(3)
    
@micropython.viper
def _OTHER_RECT(front, top, back, bottom):
    return array('h', [front, top, back, bottom])
_FRONT = const(0)
_BACK = const(2)

class SPRITE:
    def __init__(self, img, mask, code_bullet):
        self.img = img
        self.mask = mask
        self.code_bullet = code_bullet

class BULLET:
    def __init__(self):
        self.view = _OTHER_RECT(0, 0, 0, 0)
        self.rect = _RECT(0, 0, 0, 0)
        self.i = array('i', 0 for i in range(26))
_BULLET_flag = const(0)
_BULLET_code_bullet = const(1)
_BULLET_bbits = const(2)
_BULLET_cond = const(3)
_BULLET_x = const(4)
_BULLET_y = const(5)
_BULLET_xm = const(6)
_BULLET_ym = const(7)
_BULLET_tgt_x = const(8)
_BULLET_tgt_y = const(9)
_BULLET_act_no = const(10)
_BULLET_act_wait = const(11)
_BULLET_ani_wait = const(12)
_BULLET_ani_no = const(13)
_BULLET_direct = const(14)
_BULLET_count1 = const(15)
_BULLET_count2 = const(16)
_BULLET_life_count = const(17)
_BULLET_damage = const(18)
_BULLET_life = const(19)
_BULLET_enemyXL = const(20)
_BULLET_enemyYL = const(21)
_BULLET_blockXL = const(22)
_BULLET_blockYL = const(23)
_BULLET_sprite_no = const(24)
_BULLET_frame_no = const(25)

_gBulTbl = [
    # Null
    bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
    # Snake
    bytearray([4, 1, 20, 36, 4, 4, 2, 2, 8, 8, 8, 8]),
    bytearray([6, 1, 23, 36, 4, 4, 2, 2, 8, 8, 8, 8]),
    bytearray([8, 1, 30, 36, 4, 4, 2, 2, 8, 8, 8, 8]),
    # Polar Star
    bytearray([1, 1, 8, 32, 6, 6, 2, 2, 8, 8, 8, 8]),
    bytearray([2, 1, 12, 32, 6, 6, 2, 2, 8, 8, 8, 8]),
    bytearray([4, 1, 16, 32, 6, 6, 2, 2, 8, 8, 8, 8]),
    # Fireball
    bytearray([2, 2, 100, 8, 8, 16, 4, 2, 8, 8, 8, 8]),
    bytearray([3, 2, 100, 8, 4, 4, 4, 2, 8, 8, 8, 8]),
    bytearray([3, 2, 100, 8, 4, 4, 4, 2, 8, 8, 8, 8]),
    # Machine Gun
    bytearray([2, 1, 20, 32, 2, 2, 2, 2, 8, 8, 8, 8]),
    bytearray([4, 1, 20, 32, 2, 2, 2, 2, 8, 8, 8, 8]),
    bytearray([6, 1, 20, 32, 2, 2, 2, 2, 8, 8, 8, 8]),
    # Missile Launcher
    bytearray([0, 10, 50, 40, 2, 2, 2, 2, 8, 8, 8, 8]),
    bytearray([0, 10, 70, 40, 4, 4, 4, 4, 8, 8, 8, 8]),
    bytearray([0, 10, 90, 40, 4, 4, 0, 0, 8, 8, 8, 8]),
    # Missile Launcher explosion
    bytearray([1, 100, 100, 20, 16, 16, 0, 0, 0, 0, 0, 0]),
    bytearray([1, 100, 100, 20, 16, 16, 0, 0, 0, 0, 0, 0]),
    bytearray([1, 100, 100, 20, 16, 16, 0, 0, 0, 0, 0, 0]),
    # Bubbler
    bytearray([1, 1, 20, 8, 2, 2, 2, 2, 4, 4, 4, 4]),
    bytearray([2, 1, 20, 8, 2, 2, 2, 2, 4, 4, 4, 4]),
    bytearray([2, 1, 20, 8, 4, 4, 4, 4, 4, 4, 4, 4]),
    # Bubbler level 3 thorns
    bytearray([3, 1, 32, 32, 2, 2, 2, 2, 4, 4, 4, 4]),
    # Blade slashes
    bytearray([0, 100, 0, 36, 8, 8, 8, 8, 12, 12, 12, 12]),
    # Falling spike that deals 127 damage
    bytearray([127, 1, 2, 4, 8, 4, 8, 4, 0, 0, 0, 0]),
    # Blade
    bytearray([15, 1, 30, 36, 8, 8, 4, 2, 8, 8, 8, 8]),
    bytearray([6, 3, 18, 36, 10, 10, 4, 2, 12, 12, 12, 12]),
    bytearray([1, 100, 30, 36, 6, 6, 4, 4, 12, 12, 12, 12]),
    # Super Missile Launcher
    bytearray([0, 10, 30, 40, 2, 2, 2, 2, 8, 8, 8, 8]),
    bytearray([0, 10, 40, 40, 4, 4, 4, 4, 8, 8, 8, 8]),
    bytearray([0, 10, 40, 40, 4, 4, 0, 0, 8, 8, 8, 8]),
    # Super Missile Launcher explosion
    bytearray([2, 100, 100, 20, 12, 12, 0, 0, 0, 0, 0, 0]),
    bytearray([2, 100, 100, 20, 12, 12, 0, 0, 0, 0, 0, 0]),
    bytearray([2, 100, 100, 20, 12, 12, 0, 0, 0, 0, 0, 0]),
    # Nemesis
    bytearray([4, 4, 20, 32, 4, 4, 3, 3, 8, 8, 24, 8]),
    bytearray([4, 2, 20, 32, 2, 2, 2, 2, 8, 8, 24, 8]),
    bytearray([1, 1, 20, 32, 2, 2, 2, 2, 8, 8, 24, 8]),
    # Spur
    bytearray([4, 4, 30, 64, 6, 6, 3, 3, 8, 8, 8, 8]),
    bytearray([8, 8, 30, 64, 6, 6, 3, 3, 8, 8, 8, 8]),
    bytearray([12, 12, 30, 64, 6, 6, 3, 3, 8, 8, 8, 8]),
    # Spur trail
    bytearray([3, 100, 30, 32, 6, 6, 3, 3, 4, 4, 4, 4]),
    bytearray([6, 100, 30, 32, 6, 6, 3, 3, 4, 4, 4, 4]),
    bytearray([11, 100, 30, 32, 6, 6, 3, 3, 4, 4, 4, 4]),
    # Curly's Nemesis
    bytearray([4, 4, 20, 32, 4, 4, 3, 3, 8, 8, 24, 8]),
    # Screen-nuke that kills all enemies
    bytearray([0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0]),
    # Whimsical Star
    bytearray([1, 1, 1, 36, 1, 1, 1, 1, 1, 1, 1, 1]),]
_gBulTbl_damage = const(0)
_gBulTbl_life = const(1)
_gBulTbl_life_count = const(2)
_gBulTbl_bbits = const(3)
_gBulTbl_enemyXL = const(4)
_gBulTbl_enemyYL = const(5)
_gBulTbl_blockXL = const(6)
_gBulTbl_blockYL = const(7)
_gBulTbl_view_front = const(8)
_gBulTbl_view_top = const(9)
_gBulTbl_view_back = const(10)
_gBulTbl_view_bottom = const(11)

_bul_sprite = [
    # None
    [ # 00
    0],
    # Snake
    [ # 01
    _RECT(120, 64, 136, 80),
    _RECT(136, 64, 152, 80),
    _RECT(120, 80, 136, 96),
    _RECT(136, 80, 152, 96)],
    [ # 02
    _RECT(192, 16, 208, 32),
    _RECT(208, 16, 224, 32),
    _RECT(224, 16, 240, 32)],
    [ # 03, dupe of 02
    _RECT(192, 16, 208, 32),
    _RECT(208, 16, 224, 32),
    _RECT(224, 16, 240, 32)],
    # Polar Star
    [ # 04
    _RECT(128, 32, 144, 48),
    _RECT(144, 32, 160, 48)],
    [ # 05
    _RECT(160, 32, 176, 48),
    _RECT(176, 32, 192, 48)],
    [ # 06
    _RECT(128, 48, 144, 64),
    _RECT(144, 48, 160, 64)],
    # Fireball
    [ # 07
    _RECT(128, 16, 144, 32),
    _RECT(144, 16, 160, 32),
    _RECT(160, 16, 176, 32),
    _RECT(176, 16, 192, 32)],
    [ # 08
    _RECT(224, 16, 240, 32),
    _RECT(208, 16, 224, 32),
    _RECT(192, 16, 208, 32)],
    [ # 09, dupe of 08
    _RECT(224, 16, 240, 32),
    _RECT(208, 16, 224, 32),
    _RECT(192, 16, 208, 32)],
    # Machine Gun
    [ # 10
    _RECT(64, 0, 80, 16),
    _RECT(80, 0, 96, 16),
    _RECT(96, 0, 112, 16),
    _RECT(112, 0, 128, 16)],
    [ # 11
    _RECT(64, 16, 80, 32),
    _RECT(80, 16, 96, 32),
    _RECT(96, 16, 112, 32),
    _RECT(112, 16, 128, 32)],
    [ # 12
    _RECT(64, 32, 80, 48),
    _RECT(80, 32, 96, 48),
    _RECT(96, 32, 112, 48),
    _RECT(112, 32, 128, 48)],
    # Missile Launcher
    [ # 13
    _RECT(0, 0, 16, 16),
    _RECT(16, 0, 32, 16),
    _RECT(32, 0, 48, 16),
    _RECT(48, 0, 64, 16)],
    [ # 14
    _RECT(0, 16, 16, 32),
    _RECT(16, 16, 32, 32),
    _RECT(32, 16, 48, 32),
    _RECT(48, 16, 64, 32)],
    [ # 15
    _RECT(0, 32, 16, 48),
    _RECT(16, 32, 32, 48),
    _RECT(32, 32, 48, 48),
    _RECT(48, 32, 64, 48)],
    # Missile Launcher explosion
    [ # 16
    0],
    [ # 17
    0],
    [ # 18
    0],
    # Bubbler
    [ # 19
    _RECT(192, 0, 200, 8),
    _RECT(200, 0, 208, 8),
    _RECT(208, 0, 216, 8),
    _RECT(216, 0, 224, 8)],
    [ # 20
    _RECT(192, 8, 200, 16),
    _RECT(200, 8, 208, 16),
    _RECT(208, 8, 216, 16),
    _RECT(216, 8, 224, 16)],
    [ # 21
    _RECT(240, 16, 248, 24),
    _RECT(248, 16, 256, 24),
    _RECT(240, 24, 248, 32),
    _RECT(248, 24, 256, 32)],
    # Bubbler level 3 spines
    [ # 22
    _RECT(224, 0, 232, 8), # rcLeft/Right
    _RECT(232, 0, 240, 8),
    _RECT(224, 8, 232, 16), # rcDown
    _RECT(232, 8, 240, 16)],
    # Blade slashes
    [ # 23
    _RECT(0, 64, 24, 88), # rcLeft
    _RECT(24, 64, 48, 88),
    _RECT(48, 64, 72, 88),
    _RECT(72, 64, 96, 88),
    _RECT(96, 64, 120, 88),
    _RECT(0, 88, 24, 112), # rcRight
    _RECT(24, 88, 48, 112),
    _RECT(48, 88, 72, 112),
    _RECT(72, 88, 96, 112),
    _RECT(96, 88, 120, 112)],
    # Falling spike that deals 127 damage
    [ # 24
    0],
    # Blade
    [ # 25
    _RECT(0, 48, 16, 64), # rcLeft
    _RECT(16, 48, 32, 64),
    _RECT(32, 48, 48, 64),
    _RECT(48, 48, 64, 64),
    _RECT(64, 48, 80, 64), # rcRight
    _RECT(80, 48, 96, 64),
    _RECT(96, 48, 112, 64),
    _RECT(112, 48, 128, 64)],
    [ # 26
    _RECT(160, 48, 184, 72), # rcLeft
    _RECT(184, 48, 208, 72),
    _RECT(208, 48, 232, 72),
    _RECT(232, 48, 256, 72),
    _RECT(160, 72, 184, 96), # rcRight
    _RECT(184, 72, 208, 96),
    _RECT(208, 72, 232, 96),
    _RECT(232, 72, 256, 96)],
    [ # 27
    _RECT(272, 0, 296, 24), # rcLeft
    _RECT(296, 0, 320, 24),
    _RECT(272, 48, 296, 72), # rcUp
    _RECT(296, 0, 320, 24),
    _RECT(272, 24, 296, 48), # rcRight
    _RECT(296, 24, 320, 48),
    _RECT(296, 48, 320, 72), # rcDown
    _RECT(296, 24, 320, 48)],
    # Super Missile Launcher
    [ # 28
    _RECT(120, 96, 136, 112),
    _RECT(136, 96, 152, 112),
    _RECT(152, 96, 168, 112),
    _RECT(168, 96, 184, 112)],
    [ # 29
    _RECT(184, 96, 200, 112),
    _RECT(200, 96, 216, 112),
    _RECT(216, 96, 232, 112),
    _RECT(232, 96, 248, 112)],
    [ # 30
    _RECT(120, 96, 136, 112),
    _RECT(136, 96, 152, 112),
    _RECT(152, 96, 168, 112),
    _RECT(168, 96, 184, 112)]
    ]

class Bullet:
    def __init__(self, MyChar):
        self.MyChar = MyChar
        self.gBul = []
        self.sprites = []
        self.inc = 0
        
    @micropython.viper
    def InitBullet(self):
        # Identical to ClearBullet
        self.gBul = [BULLET() for i in range(_BULLET_MAX)]
    
    @micropython.viper
    def CountArmsBullet(self, arms_code: int) -> int:
        gBul = self.gBul
        count = 0
        for i in range(_BULLET_MAX):
            bul_i = ptr32(gBul[i].i)
            if bul_i[_BULLET_cond] & 0x80 and (bul_i[_BULLET_code_bullet] + 2) // 3 == arms_code:
                count += 1
        return count
    
    @micropython.viper
    def PutBullet(self, fx: int, fy: int):
        gBul = self.gBul
        sprites = self.sprites
        x = 0
        y = 0
        for i in range(_BULLET_MAX):
            bul = gBul[i]
            bul_i = ptr32(bul.i)
            if not bul_i[_BULLET_cond] & 0x80:
                continue
            direct = bul_i[_BULLET_direct]
            view = ptr16(bul.view)
            if direct == _DIR_LEFT:
                x = bul_i[_BULLET_x] - view[_TOP]
                y = bul_i[_BULLET_y] - view[_BACK]
            elif direct == _DIR_UP:
                x = bul_i[_BULLET_x] - view[_BACK]
                y = bul_i[_BULLET_y] - view[_TOP]
            elif direct == _DIR_RIGHT:
                x = bul_i[_BULLET_x] - view[_FRONT]
                y = bul_i[_BULLET_y] - view[_BACK]
            elif direct == _DIR_DOWN:
                x = bul_i[_BULLET_x] - view[_BACK]
                y = bul_i[_BULLET_y] - view[_FRONT]
            
            sprite = sprites[bul_i[_BULLET_sprite_no]]
            frame_no = bul_i[_BULLET_frame_no]
            img = sprite.img[frame_no]
            mask = sprite.mask[frame_no]

            display.blitWithMask(img, (x // 0x200) - (fx // 0x200), (y // 0x200) - (fy // 0x200), 16, 16, mask)

    @micropython.viper
    def LoadSprites(self, no: int) -> int:
        # check if this sprite is already loaded
        sprites = self.sprites
        length = int(len(sprites))
        i = 0
        while i < length:
            if int(sprites[i].code_bullet) == no:
                return i
            i += 1

        stencil = _bul_sprite[no]

        sprites.append(SPRITE(PreloadSprites("Bullet", stencil), PreloadSprites("Bullet_mask", stencil), no))
        gc.collect()
        return i

    @micropython.viper
    def SetBullet(self, no: int, x: int, y: int, direction: int):
        gBul = self.gBul
        i = 0
        while i < _BULLET_MAX and int(gBul[i].i[_BULLET_cond]) & 0x80:
            i += 1
        if i >= _BULLET_MAX:
            return
        bul = gBul[i]
        bul_i = ptr32(bul.i)
        view = ptr16(bul.view)
        for i in range(int(len(bul.i))):
            bul_i[i] = 0
        tbl = ptr8(_gBulTbl[no])
        bul_i[_BULLET_code_bullet] = no
        bul_i[_BULLET_cond] = 0x80
        bul_i[_BULLET_direct] = direction
        bul_i[_BULLET_damage] = tbl[_gBulTbl_damage]
        bul_i[_BULLET_life] = tbl[_gBulTbl_life]
        bul_i[_BULLET_life_count] = tbl[_gBulTbl_life_count]
        bul_i[_BULLET_bbits] = tbl[_gBulTbl_bbits]
        bul_i[_BULLET_enemyXL] = tbl[_gBulTbl_enemyXL] * 0x200
        bul_i[_BULLET_enemyYL] = tbl[_gBulTbl_enemyYL] * 0x200
        bul_i[_BULLET_blockXL] = tbl[_gBulTbl_blockXL] * 0x200
        bul_i[_BULLET_blockYL] = tbl[_gBulTbl_blockYL] * 0x200
        view[_FRONT] = tbl[_gBulTbl_view_back] * 0x200
        view[_TOP] = tbl[_gBulTbl_view_front] * 0x200
        view[_BACK] = tbl[_gBulTbl_view_top] * 0x200
        view[_BOTTOM] = tbl[_gBulTbl_view_bottom] * 0x200
        bul_i[_BULLET_x] = x
        bul_i[_BULLET_y] = y
        bul_i[_BULLET_sprite_no] = int(self.LoadSprites(no))
        
    @micropython.viper
    def ActBullet_Frontia1(self, bul_i: ptr32):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return
        
        direct = bul_i[_BULLET_direct]
        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_frame_no] = int(randrange(0, 2))
            bul_i[_BULLET_act_no] = 1
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] = -0x600
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] = -0x600
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] = 0x600
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] = 0x600
        else:
            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]
        
        if direct == _DIR_LEFT:
            bul_i[_BULLET_frame_no] -= 1
            if bul_i[_BULLET_frame_no] < 0:
                bul_i[_BULLET_frame_no] = 3
        else:
            bul_i[_BULLET_frame_no] += 1
            if bul_i[_BULLET_frame_no] > 3:
                bul_i[_BULLET_frame_no] = 0
    
    @micropython.viper
    def ActBullet_Frontia2(self, bul_i: ptr32, level: int):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return
    
        direct = bul_i[_BULLET_direct]
        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_frame_no] = int(randrange(0, 2))
            bul_i[_BULLET_act_no] = 1
            
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] = -0x200
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] = -0x200
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] = 0x200
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] = 0x200

            inc = int(self.inc) + 1
            if direct == _DIR_LEFT or direct == _DIR_RIGHT:
                if inc % 2:
                    bul_i[_BULLET_ym] = 0x400
                else:
                    bul_i[_BULLET_ym] = -0x400
            else:
                if inc % 2:
                    bul_i[_BULLET_xm] = 0x400
                else:
                    bul_i[_BULLET_xm] = -0x400
            self.inc = inc
        else:
        
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] -= 0x80
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] -= 0x80
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] += 0x80
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] += 0x80
        
            if bul_i[_BULLET_count1] % 5 == 2:
                if direct == _DIR_LEFT or direct == _DIR_RIGHT:
                    if bul_i[_BULLET_ym] < 0:
                        bul_i[_BULLET_ym] = 0x400
                    else:
                        bul_i[_BULLET_ym] = -0x400
                else:
                    if bul_i[_BULLET_xm] < 0:
                        bul_i[_BULLET_xm] = 0x400
                    else:
                        bul_i[_BULLET_xm] = -0x400
        
            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]
        
            bul_i[_BULLET_frame_no] += 1
            if bul_i[_BULLET_frame_no] > 2:
                bul_i[_BULLET_frame_no] = 0
        
            #if (level == 2)
                #SetNpChar(129, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, -0x200, bul_i[_BULLET_ani_no], NULL, 0x100)
            #else
                #SetNpChar(129, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, -0x200, bul_i[_BULLET_ani_no] + 3], NULL, 0x100)
 
    @micropython.viper
    def ActBullet_PoleStar(self, bul_i: ptr32, level: int):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return
        
        direct = bul_i[_BULLET_direct]
        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_act_no] = 1

            # Set hitbox
            enemyXL = 0x400 * level
            enemyYL = 0x400 * level

            # Set speed
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] = -0x1000
                bul_i[_BULLET_enemyXL] = enemyXL
                bul_i[_BULLET_frame_no] = 0
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] = -0x1000
                bul_i[_BULLET_enemyYL] = enemyYL
                bul_i[_BULLET_frame_no] = 1
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] = 0x1000
                bul_i[_BULLET_enemyXL] = enemyXL
                bul_i[_BULLET_frame_no] = 0
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] = 0x1000
                bul_i[_BULLET_enemyYL] = enemyYL
                bul_i[_BULLET_frame_no] = 1

        else:
            # Move
            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]

    @micropython.viper
    def ActBullet_FireBall(self, bul_i: ptr32, level: int):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return
            
        flag = bul_i[_BULLET_flag]
        direct = bul_i[_BULLET_direct]
        b = False
        if flag & 0x04:
            if flag & 0x01:
                b = True
            if direct == _DIR_RIGHT:
                direct = _DIR_LEFT
                bul_i[_BULLET_direct] = direct
        if flag & 0x0a == 0x0a:
            b = True
        if direct == _DIR_RIGHT and flag & 4:
            direct = _DIR_LEFT
            bul_i[_BULLET_direct] = direct
        if b:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_PROJECTILE_DISSIPATION, _DIR_LEFT)
            #PlaySoundObject(28, SOUND_MODE_PLAY)
            return
        
        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_act_no] = 1
            
            gMC_i = ptr32(self.MyChar.gMC.i)
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] = -0x400
            elif direct == _DIR_UP:
                bul_i[_BULLET_xm] = gMC_i[_MYCHAR_xm]
                if gMC_i[_MYCHAR_xm] < 0:
                    bul_i[_BULLET_direct] = _DIR_LEFT
                else:
                    bul_i[_BULLET_direct] = _DIR_RIGHT
                if gMC_i[_MYCHAR_direct] == _DIR_LEFT:
                    bul_i[_BULLET_xm] -= 0x80
                else:
                    bul_i[_BULLET_xm] += 0x80
                bul_i[_BULLET_ym] = -0x5FF
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] = 0x400
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_xm] = gMC_i[_MYCHAR_xm]
                if gMC_i[_MYCHAR_xm] < 0:
                    bul_i[_BULLET_direct] = _DIR_LEFT
                else:
                    bul_i[_BULLET_direct] = _DIR_RIGHT
                bul_i[_BULLET_ym] = 0x5FF
        else:
        
            if flag & 8:
                bul_i[_BULLET_ym] = -0x400
            elif flag & 1:
                bul_i[_BULLET_xm] = 0x400
            elif flag & 4:
                bul_i[_BULLET_xm] = -0x400
            bul_i[_BULLET_ym] += 85
            if bul_i[_BULLET_ym] > 0x3FF:
                bul_i[_BULLET_ym] = 0x3FF
            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]
            #if flag & 0xD:
            #    PlaySoundObject(34, SOUND_MODE_PLAY)

        frame_no = bul_i[_BULLET_frame_no] + 1
        if level == 1:
            if frame_no > 3:
                frame_no = 0
        else:
            if frame_no > 2:
                frame_no = 0
            #if level == 2:
            #    SetNpChar(129, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, -0x200, bul_i[_BULLET_ani_no, NULL, 0x100)
            #else
            #    SetNpChar(129, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, -0x200, bul_i[_BULLET_ani_no] + 3, NULL, 0x100)
        bul_i[_BULLET_frame_no] = frame_no
    
    @micropython.viper
    def ActBullet_MachineGun(self, bul_i: ptr32, level: int):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return

        direct = bul_i[_BULLET_direct]
        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_frame_no] = bul_i[_BULLET_direct]
            bul_i[_BULLET_act_no] = 1
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] = -0x1000
                bul_i[_BULLET_ym] = int(randrange(-0xAA, 0xAA))
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] = -0x1000
                bul_i[_BULLET_xm] = int(randrange(-0xAA, 0xAA))
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] = 0x1000
                bul_i[_BULLET_ym] = int(randrange(-0xAA, 0xAA))
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] = 0x1000
                bul_i[_BULLET_xm] = int(randrange(-0xAA, 0xAA))
            
        else:
            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]

            #if level == 2:
            #    if bul_i[_BULLET_direct] == _DIR_UP or bul_i[_BULLET_direct] == _DIR_DOWN:
            #        SetNpChar(127, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, 0, _DIR_UP, NULL, 0x100)
            #    else:
            #        SetNpChar(127, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, 0, _DIR_LEFT, NULL, 0x100)
            #if level == 3:
            #    SetNpChar(128, bul_i[_BULLET_x], bul_i[_BULLET_y], 0, 0, bul_i[_BULLET_direct], NULL, 0x100)

    @micropython.viper
    def ActBullet_Missile(self, bul_i: ptr32, level: int):
        bul_i[_BULLET_count1] += 1
        if bul_i[_BULLET_count1] > bul_i[_BULLET_life_count]:
            bul_i[_BULLET_cond] = 0
            #SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y], CARET_SHOOT, _DIR_LEFT)
            return

        bHit = False
        flag = bul_i[_BULLET_flag]
        direct = bul_i[_BULLET_direct]
        if not bul_i[_BULLET_life] == 10:
            bHit = True
        elif direct == _DIR_LEFT and flag & 0xa1:
            bHit = True
        elif direct == _DIR_RIGHT and flag & 0x54:
            bHit = True
        elif direct == _DIR_UP and flag & 2:
            bHit = True
        elif direct == _DIR_DOWN and flag & 8:
            bHit = True

        if bHit:
            #self.SetBullet(level + 15, bul_i[_BULLET_x], bul_i[_BULLET_y], _DIR_LEFT)
            bul_i[_BULLET_cond] = 0

        if bul_i[_BULLET_act_no] == 0:
            bul_i[_BULLET_act_no] = 1
            bul_i[_BULLET_frame_no] = direct

            if direct == _DIR_LEFT or direct == _DIR_RIGHT:
                bul_i[_BULLET_tgt_y] = bul_i[_BULLET_y]
            elif direct == _DIR_UP or direct == _DIR_DOWN:
                bul_i[_BULLET_tgt_x] = bul_i[_BULLET_x]

            if level == 3:
                gMC_i = ptr32(self.MyChar.gMC.i)
                if direct == _DIR_LEFT or direct == _DIR_RIGHT:
                    if bul_i[_BULLET_y] > gMC_i[_MYCHAR_y]:
                        bul_i[_BULLET_ym] = 0x100
                    else:
                        bul_i[_BULLET_ym] = -0x100
                    bul_i[_BULLET_xm] = int(randrange(-0x200, 0x200))

                elif direct == _DIR_UP or direct == _DIR_DOWN:
                    if bul_i[_BULLET_x] > gMC_i[_MYCHAR_x]:
                        bul_i[_BULLET_xm] = 0x100
                    else:
                        bul_i[_BULLET_xm] = -0x100
                    bul_i[_BULLET_ym] = int(randrange(-0x200, 0x200))

                inc = int(self.inc)
                inc += 1
                self.inc = inc
                a = inc % 3
                if a == 0:
                    bul_i[_BULLET_ani_no] = 0x80
                elif a == 1:
                    bul_i[_BULLET_ani_no] = 0x40
                elif a == 2:
                    bul_i[_BULLET_ani_no] = 0x33
                    
            else:
                bul_i[_BULLET_ani_no] = 0x80
            
            # Fallthrough
        elif bul_i[_BULLET_act_no] == 1:
            if direct == _DIR_LEFT:
                bul_i[_BULLET_xm] -= bul_i[_BULLET_ani_no]
            elif direct == _DIR_UP:
                bul_i[_BULLET_ym] -= bul_i[_BULLET_ani_no]
            elif direct == _DIR_RIGHT:
                bul_i[_BULLET_xm] += bul_i[_BULLET_ani_no]
            elif direct == _DIR_DOWN:
                bul_i[_BULLET_ym] += bul_i[_BULLET_ani_no]

            if level == 3:
                if direct == _DIR_LEFT or direct == _DIR_RIGHT:
                    if bul_i[_BULLET_y] < bul_i[_BULLET_tgt_y]:
                        bul_i[_BULLET_ym] += 0x20
                    else:
                        bul_i[_BULLET_ym] -= 0x20
                elif direct == _DIR_UP or direct == _DIR_DOWN:
                    if bul_i[_BULLET_x] < bul_i[_BULLET_tgt_x]:
                        bul_i[_BULLET_xm] += 0x20
                    else:
                        bul_i[_BULLET_xm] -= 0x20

            if bul_i[_BULLET_xm] < -0xA00:
                bul_i[_BULLET_xm] = -0xA00
            if bul_i[_BULLET_xm] > 0xA00:
                bul_i[_BULLET_xm] = 0xA00

            if bul_i[_BULLET_ym] < -0xA00:
                bul_i[_BULLET_ym] = -0xA00
            if bul_i[_BULLET_ym] > 0xA00:
                bul_i[_BULLET_ym] = 0xA00

            bul_i[_BULLET_x] += bul_i[_BULLET_xm]
            bul_i[_BULLET_y] += bul_i[_BULLET_ym]

        bul_i[_BULLET_count2] += 1
        if bul_i[_BULLET_count2] > 2:
            bul_i[_BULLET_count2] = 0

            #if direct == _DIR_LEFT:
            #    SetCaret(bul_i[_BULLET_x] + (8 * 0x200), bul_i[_BULLET_y], CARET_EXHAUST, _DIR_RIGHT)
            #elif direct == _DIR_UP:
            #    SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y] + (8 * 0x200), CARET_EXHAUST, _DIR_DOWN)
            #elif direct == _DIR_RIGHT:
            #    SetCaret(bul_i[_BULLET_x] - (8 * 0x200), bul_i[_BULLET_y], CARET_EXHAUST, _DIR_LEFT)
            #elif direct == _DIR_DOWN:
            #    SetCaret(bul_i[_BULLET_x], bul_i[_BULLET_y] - (8 * 0x200), CARET_EXHAUST, _DIR_UP)

    @micropython.viper
    def ActBullet(self):
        gBul = self.gBul
        for i in range(_BULLET_MAX):
            bul_i = ptr32(gBul[i].i)
            if not bul_i[_BULLET_cond] & 0x80:
                continue
            if bul_i[_BULLET_life] < 1:
                bul_i[_BULLET_cond] = 0
                continue
            code_bullet = bul_i[_BULLET_code_bullet]

            # Whimsical Star
            if code_bullet == 45:
                self.ActBullet_Star(bul_i)

            # Screen-nuke that kills all enemies
            elif code_bullet == 44:
                self.ActBullet_EnemyClear(bul_i)

            # Curly's Nemesis
            elif code_bullet == 43:	# Identical to elif code_bullet == 34
                self.ActBullet_Nemesis(bul_i, 1)

            # Spur trail
            elif code_bullet >= 40:
                self.ActBullet_SpurTail(bul_i, code_bullet - 39)
                
            # Spur
            elif code_bullet >= 37:
                self.ActBullet_Spur(bul_i, code_bullet - 36)
                
            # Nemesis
            elif code_bullet >= 34:	# Identical to elif code_bullet == 43
                self.ActBullet_Nemesis(bul_i, code_bullet - 33)
                
            # Super Missile Launcher explosion
            elif code_bullet >= 31:
                self.ActBullet_SuperBom(bul_i, code_bullet - 30)

            # Super Missile Launcher
            elif code_bullet >= 28:
                self.ActBullet_SuperMissile(bul_i, code_bullet - 27)

            # Blade
            elif code_bullet == 25:
                self.ActBullet_Sword1(bul_i)
            elif code_bullet == 26:
                self.ActBullet_Sword2(bul_i)
            elif code_bullet == 27:
                self.ActBullet_Sword3(bul_i)

            # Falling spike that deals 127 damage
            elif code_bullet == 24:
                self.ActBullet_Drop(bul_i)

            # Blade slashes
            elif code_bullet == 23:
                self.ActBullet_Edge(bul_i)

            # Bubbler level 3 spines
            elif code_bullet == 22:
                self.ActBullet_Spine(bul_i)

            # Bubbler
            elif code_bullet == 19:
                self.ActBullet_Bubblin1(bul_i)
            elif code_bullet == 20:
                self.ActBullet_Bubblin2(bul_i)
            elif code_bullet == 21:
                self.ActBullet_Bubblin3(bul_i)

            # Missile Launcher explosion
            elif code_bullet >= 16:
                self.ActBullet_Bom(bul_i, code_bullet - 15)
                
            # Missile Launcher
            elif code_bullet >= 13:
                self.ActBullet_Missile(bul_i, code_bullet - 12)

            # Machine Gun
            elif code_bullet >= 10:
                self.ActBullet_MachineGun(bul_i, code_bullet - 9)

            # Fireball
            elif code_bullet >= 7:
                self.ActBullet_FireBall(bul_i, code_bullet - 6)

            # Polar Star
            elif code_bullet >= 4:
                self.ActBullet_PoleStar(bul_i, code_bullet - 3)

            # Snake
            elif code_bullet >= 2:
                self.ActBullet_Frontia2(bul_i, code_bullet)
            elif code_bullet == 1:
                self.ActBullet_Frontia1(bul_i)
