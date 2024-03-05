from array import array
from random import randrange
from display import display
from Draw import PreloadSprites

_WindowWidth = const(72)
_WindowHeight = const(40)
_FRAME_CHASE = const(0x400) # vanilla 0x200
_FRAME_OFFSET_X = const((_WindowWidth // 3) * 0x200)
_FRAME_OFFSET_Y = const((_WindowHeight // 3) * 0x200)

_gKey = const(0)
_gKeyTrg = const(1)
_gKeyLeft = const(0x00000001)
_gKeyRight = const(0x00000002)
_gKeyUp = const(0x00000004)
_gKeyDown = const(0x00000008)
_gKeyShot = const(0x00000020)
_gKeyJump = const(0x00000040)

_EQUIP_BOOSTER_0_8 = const(0x01)
_EQUIP_MAP = const(0x02)
_EQUIP_ARMS_BARRIER = const(0x04)
_EQUIP_TURBOCHARGE = const(0x08)
_EQUIP_AIR_TANK = const(0x10)
_EQUIP_BOOSTER_2_0 = const(0x20)
_EQUIP_MIMIGA_MASK = const(0x40)
_EQUIP_WHIMSICAL_STAR = const(0x80)
_EQUIP_NIKUMARU_COUNTER = const(0x0100)
_CARET_TINY_PARTICLES = const(13)

_ARMS_code = const(0)
_ARMS_level = const(1)

@micropython.viper
def RECT(top, left, bottom, right):
    return array('h', [left, top, right, bottom])
_LEFT = const(0)
_TOP = const(1)
_RIGHT = const(2)
_BOTTOM = const(3)

@micropython.viper
def OTHER_RECT(front, top, back, bottom):
    return array('h', [front, top, back, bottom])
_FRONT = const(0)
_BACK = const(2)

class MYCHAR:
    hit = OTHER_RECT(0, 0, 0, 0)
    view = OTHER_RECT(0, 0, 0, 0)
    rect = RECT(0, 0, 0, 0)
    rect_arms = RECT(0, 0, 0, 0)
    i = array('i', 0 for i in range(38))
_MYCHAR_cond = const(0)
_MYCHAR_flag = const(1)
_MYCHAR_direct = const(2)
_MYCHAR_unit = const(3)
_MYCHAR_equip = const(4)
_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_MYCHAR_tgt_x = const(7)
_MYCHAR_tgt_y = const(8)
_MYCHAR_index_x = const(9)
_MYCHAR_index_y = const(10)
_MYCHAR_xm = const(11)
_MYCHAR_ym = const(12)
_MYCHAR_ani_wait = const(13)
_MYCHAR_ani_no = const(14)
_MYCHAR_level = const(15)
_MYCHAR_exp_wait = const(16)
_MYCHAR_exp_count = const(17)
_MYCHAR_shock = const(18)
_MYCHAR_no_life = const(19)
_MYCHAR_rensha = const(20)
_MYCHAR_bubble = const(21)
_MYCHAR_life = const(22)
_MYCHAR_star = const(23)
_MYCHAR_max_life = const(24)
_MYCHAR_a = const(25)
_MYCHAR_lifeBr = const(26)
_MYCHAR_lifeBr_count = const(27)
_MYCHAR_air = const(28)
_MYCHAR_air_get = const(29)
_MYCHAR_boost_sw = const(30)
_MYCHAR_boost_cnt = const(31)
_MYCHAR_no_splash_or_air_limit_underwater = const(32)
_MYCHAR_jump_y = const(33)
_MYCHAR_up = const(34) # bool
_MYCHAR_down = const(35) # bool
_MYCHAR_sprash = const(36) # bool
_MYCHAR_ques = const(37) # bool
    
@micropython.viper
def _physics_normal():
    return array('h', [0x32C, 0x5FF, 0x50, 0x20, 0x55, 0x20, 0x33, 0x500])

@micropython.viper
def _physics_underwater():
    return array('h', [0x196, 0x2ff, 0x28, 0x10, 0x2a, 0x10, 0x19, 0x280])
_physics_max_dash = const(0)
_physics_max_move = const(1)
_physics_gravity1 = const(2)
_physics_gravity2 = const(3)
_physics_dash1 = const(4)
_physics_dash2 = const(5)
_physics_resist = const(6)
_physics_jump = const(7)
    
class MyChar:
    def __init__(self, KeyControl, ArmsItem, g_GameFlags):
        self.KeyControl = KeyControl
        self.ArmsItem = ArmsItem
        self.g_GameFlags = g_GameFlags
        self.gMC = MYCHAR()
        self._physics_normal = _physics_normal()
        self._physics_underwater = _physics_underwater()

    @micropython.viper
    def InitMyChar(self):
        self.gMC = MYCHAR()
        gMC = self.gMC
        gMC_i = ptr32(gMC.i)
    
        gMC_i[_MYCHAR_cond] = 0x80
        gMC_i[_MYCHAR_direct] = 2

        gMC.view[_FRONT] = 8 * 0x200
        gMC.view[_TOP] = 8 * 0x200
        gMC.view[_BACK] = 8 * 0x200
        gMC.view[_BOTTOM] = 8 * 0x200

        gMC.hit[_FRONT] = 5 * 0x200
        gMC.hit[_TOP] = 8 * 0x200
        gMC.hit[_BACK] = 5 * 0x200
        gMC.hit[_BOTTOM] = 8 * 0x200

        gMC_i[_MYCHAR_life] = 3
        gMC_i[_MYCHAR_max_life] = 3
        gMC_i[_MYCHAR_unit] = 0

        gMC_i[_MYCHAR_no_splash_or_air_limit_underwater] = 0
        gMC_i[_MYCHAR_jump_y] = int(0x7fffffff)
        
        # preload sprite sheet
        rcLeft = [
        RECT(0, 0, 16, 16),
        RECT(16, 0, 32, 16),
        RECT(0, 0, 16, 16),
        RECT(32, 0, 48, 16),
        RECT(0, 0, 16, 16),
        RECT(48, 0, 64, 16),
        RECT(64, 0, 80, 16),
        RECT(48, 0, 64, 16),
        RECT(80, 0, 96, 16),
        RECT(48, 0, 64, 16),
        RECT(96, 0, 112, 16),
        RECT(112, 0, 128, 16)]

        rcRight = [
        RECT(0, 16, 16, 32),
        RECT(16, 16, 32, 32),
        RECT(0, 16, 16, 32),
        RECT(32, 16, 48, 32),
        RECT(0, 16, 16, 32),
        RECT(48, 16, 64, 32),
        RECT(64, 16, 80, 32),
        RECT(48, 16, 64, 32),
        RECT(80, 16, 96, 32),
        RECT(48, 16, 64, 32),
        RECT(96, 16, 112, 32),
        RECT(112, 16, 128, 32)]
        
        self.tiles_left = PreloadSprites("MyChar", rcLeft)
        self.tiles_left_mask = PreloadSprites("MyChar_mask", rcLeft)
        self.tiles_right = PreloadSprites("MyChar", rcRight)
        self.tiles_right_mask = PreloadSprites("MyChar_mask", rcRight)

    @micropython.viper
    def AnimationMyChar(self, bKey: bool):
        KeyControl_i = ptr8(self.KeyControl.i)
        gKey = KeyControl_i[_gKey]
        gMC = self.gMC
        gMC_i = ptr32(gMC.i)
        cond = gMC_i[_MYCHAR_cond]
        ani_wait = gMC_i[_MYCHAR_ani_wait]
        ani_no = gMC_i[_MYCHAR_ani_no]
        if cond & 2:
            return
        if gMC_i[_MYCHAR_flag] & 8:
            if cond & 1:
                gMC_i[_MYCHAR_ani_no] = 11
            elif gKey & _gKeyUp and gKey & (_gKeyLeft | _gKeyRight) and bKey:
                gMC_i[_MYCHAR_cond] |= 4
                gMC_i[_MYCHAR_ani_wait] += 1
                if ani_wait > 4:
                    gMC_i[_MYCHAR_ani_wait] = 0
                    gMC_i[_MYCHAR_ani_no] += 1
                    #if ani_no == 7 or ani_no == 9:
                        #PlaySoundObject(24, SOUND_MODE_PLAY)
                if ani_no > 9 or ani_no < 6:
                    gMC_i[_MYCHAR_ani_no] = 6
            elif gKey & (_gKeyLeft | _gKeyRight) and bKey:
                gMC_i[_MYCHAR_cond] |= 4
                gMC_i[_MYCHAR_ani_wait] += 1
                if ani_wait > 4:
                    gMC_i[_MYCHAR_ani_wait] = 0
                    gMC_i[_MYCHAR_ani_no] += 1
                    #if ani_no == 2 or ani_no == 4:
                        #PlaySoundObject(24, SOUND_MODE_PLAY)
                if ani_no > 4 or ani_no < 1:
                    gMC_i[_MYCHAR_ani_no] = 1
            elif gKey & _gKeyUp and bKey:
                #if cond & 4:
                    #PlaySoundObject(24, SOUND_MODE_PLAY)
                gMC_i[_MYCHAR_cond] &= ~4
                gMC_i[_MYCHAR_ani_no] = 5
            else:
                #if cond & 4:
                    #PlaySoundObject(24, SOUND_MODE_PLAY)
                gMC_i[_MYCHAR_cond] &= ~4
                gMC_i[_MYCHAR_ani_no] = 0
        elif gMC_i[_MYCHAR_up]:
            gMC_i[_MYCHAR_ani_no] = 6
        elif gMC_i[_MYCHAR_down]:
            gMC_i[_MYCHAR_ani_no] = 10
        else:
            if gMC_i[_MYCHAR_ym] > 0:
                gMC_i[_MYCHAR_ani_no] = 1
            else:
                gMC_i[_MYCHAR_ani_no] = 3

    @micropython.viper
    def PutMyChar(self, fx: int, fy: int):
        gMC = self.gMC
        gMC_i = ptr32(gMC.i)
        view = ptr16(gMC.view)
        cond = gMC_i[_MYCHAR_cond]
        if not cond & 0x80 or cond & 0x02:
            return

        # Draw weapon
        rect_arms = ptr16(gMC.rect_arms)
        #self.rect_arms[_LEFT] = (gArmsData[gSelectedArms].code % 13) * 24
        #self.rect_arms[_RIGHT] = self.rect_arms.left + 24
        #self.rect_arms[_TOP] = (gArmsData[gSelectedArms].code // 13) * 96
        #self.rect_arms[_BOTTOM] = self.rect_arms.top + 16
        
        arms_offset_y = 0
        direct = gMC_i[_MYCHAR_direct]
        if direct == 2:
            rect_arms[_TOP] += 16
            rect_arms[_BOTTOM] += 16
        if gMC_i[_MYCHAR_up]:
            arms_offset_y = -4
            rect_arms[_TOP] += 32
            rect_arms[_BOTTOM] += 32
        elif gMC_i[_MYCHAR_down]:
            arms_offset_y = 4
            rect_arms[_TOP] += 64
            rect_arms[_BOTTOM] += 64

        ani_no = gMC_i[_MYCHAR_ani_no]
        if ani_no == 1 or ani_no == 3 or ani_no == 6 or ani_no == 8:
            rect_arms[_TOP] += 1

        '''if gMC_i[_MYCHAR_direct] == 0:
            PutBitmap3(
                &grcGame,
                SubpixelToScreenCoord(self.x - view[_FRONT]) - SubpixelToScreenCoord(fx) - PixelToScreenCoord(8),
                SubpixelToScreenCoord(self.y - view[_TOP]) - SubpixelToScreenCoord(fy) + PixelToScreenCoord(arms_offset_y),
                &self.rect_arms,
                SURFACE_ID_ARMS)
        else:
            PutBitmap3(
                &grcGame,
                SubpixelToScreenCoord(self.x - view[_FRONT]) - SubpixelToScreenCoord(fx),
                SubpixelToScreenCoord(self.y - view[_TOP]) - SubpixelToScreenCoord(fy) + PixelToScreenCoord(arms_offset_y),
                &self.rect_arms,
                SURFACE_ID_ARMS)'''

        if (gMC_i[_MYCHAR_shock] // 2 % 2) > 0:
            return

        # Draw player
        gMIMCurrentNum = 0 ## dunno what it's for, so we set it to zero for now. might be message related
        rect = ptr16(gMC.rect)
        rect[1] += 32 * gMIMCurrentNum
        rect[3] += 32 * gMIMCurrentNum
        if gMC_i[_MYCHAR_equip] & _EQUIP_MIMIGA_MASK:
            rect[1] += 32
            rect[3] += 32

        if direct == 0: 
            # facing left
            display.blitWithMask(self.tiles_left[ani_no], (gMC_i[_MYCHAR_x] - view[_FRONT] - fx + 0x1ff) // 0x200, (gMC_i[_MYCHAR_y] - view[_TOP] - fy + 0x1ff) // 0x200, 16, 16, self.tiles_left_mask[ani_no])
        else: 
            # facing right
            display.blitWithMask(self.tiles_right[ani_no], (gMC_i[_MYCHAR_x] - view[_FRONT] - fx + 0x1ff) // 0x200, (gMC_i[_MYCHAR_y] - view[_TOP] - fy + 0x1ff) // 0x200, 16, 16, self.tiles_right_mask[ani_no])
            
        '''# Draw air tank
        RECT rcBubble[2] = 
            56, 96, 80, 120,
            80, 96, 104, 120,
        
        ++self.bubble
        if (gMC.equip & _EQUIP_AIR_TANK and gMC.flag & 0x100)
            PutBitmap3(&grcGame, SubpixelToScreenCoord(gMC.x) - PixelToScreenCoord(12) - SubpixelToScreenCoord(fx), SubpixelToScreenCoord(gMC.y) - PixelToScreenCoord(12) - SubpixelToScreenCoord(fy), &rcBubble[(gMC.bubble // 2) % 2], SURFACE_ID_CARET)
        elif (gMC.unit == 1)
            PutBitmap3(&grcGame, SubpixelToScreenCoord(gMC.x) - PixelToScreenCoord(12) - SubpixelToScreenCoord(fx), SubpixelToScreenCoord(gMC.y) - PixelToScreenCoord(12) - SubpixelToScreenCoord(fy), &rcBubble[(gMC.bubble // 2) % 2], SURFACE_ID_CARET)
'''

    @micropython.viper
    def ActMyChar_Normal_1(self, bKey: bool, gMC_i: ptr32, gKey: int, gKeyTrg: int, physics: ptr16):
        # Don't create "?" effect
        gMC_i[_MYCHAR_ques] = False
    
        # If can't control player, stop boosting
        if not bKey:
            gMC_i[_MYCHAR_boost_sw] = 0
        
        # Movement on the ground
        if gMC_i[_MYCHAR_flag] & 0x38:
            # Stop boosting and refuel
            gMC_i[_MYCHAR_boost_sw] = 0
            if gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_0_8:
                gMC_i[_MYCHAR_boost_cnt] = 50
            elif gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_2_0:
                gMC_i[_MYCHAR_boost_cnt] = 50
            else:
                gMC_i[_MYCHAR_boost_cnt] = 0

            # Move in direction held
            if bKey:
                if gKeyTrg & _gKeyDown and not gMC_i[_MYCHAR_cond] & 0x01 and not int(self.g_GameFlags[0]) & 0x04:
                    gMC_i[_MYCHAR_cond] |= 1
                    gMC_i[_MYCHAR_ques] = True
                else:
                    if gKey & _gKeyLeft and gMC_i[_MYCHAR_xm] > 0 - physics[_physics_max_dash]:
                        gMC_i[_MYCHAR_xm] -= physics[_physics_dash1]
                    if gKey & _gKeyRight and gMC_i[_MYCHAR_xm] < physics[_physics_max_dash]:
                        gMC_i[_MYCHAR_xm] += physics[_physics_dash1]
                    if gKey & _gKeyLeft:
                        gMC_i[_MYCHAR_direct] = 0
                    if gKey & _gKeyRight:
                        gMC_i[_MYCHAR_direct] = 2

            # Friction
            if not gMC_i[_MYCHAR_cond] & 0x20:
                if gMC_i[_MYCHAR_xm] < 0:
                    if (gMC_i[_MYCHAR_xm] > 0 - physics[_physics_resist]):
                        gMC_i[_MYCHAR_xm] = 0
                    else:
                        gMC_i[_MYCHAR_xm] += physics[_physics_resist]
                if gMC_i[_MYCHAR_xm] > 0:
                    if gMC_i[_MYCHAR_xm] < physics[_physics_resist]:
                        gMC_i[_MYCHAR_xm] = 0
                    else:
                        gMC_i[_MYCHAR_xm] -= physics[_physics_resist]

        else:
            # Start boosting
            if bKey:
                if gMC_i[_MYCHAR_equip] & (_EQUIP_BOOSTER_0_8 | _EQUIP_BOOSTER_2_0) and gKeyTrg & _gKeyJump and gMC_i[_MYCHAR_boost_cnt] != 0:
                    gMC_i[_MYCHAR_jump_y] = gMC_i[_MYCHAR_y]
                
                    # Booster 0.8
                    if gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_0_8:
                        gMC_i[_MYCHAR_boost_sw] = 1
                        if gMC_i[_MYCHAR_ym] > 0x100:
                            gMC_i[_MYCHAR_ym] //= 2
                    
                    # Booster 2.0
                    if gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_2_0:
                        if gKey & _gKeyLeft:
                            gMC_i[_MYCHAR_boost_sw] = 1
                            gMC_i[_MYCHAR_ym] = 0
                            gMC_i[_MYCHAR_xm] = -0x5FF
                        elif gKey & _gKeyRight:
                            gMC_i[_MYCHAR_boost_sw] = 1
                            gMC_i[_MYCHAR_ym] = 0
                            gMC_i[_MYCHAR_xm] = 0x5FF
                        elif gKey & _gKeyDown:
                            gMC_i[_MYCHAR_boost_sw] = 3
                            gMC_i[_MYCHAR_xm] = 0
                            gMC_i[_MYCHAR_ym] = 0x5FF
                        else:
                            gMC_i[_MYCHAR_boost_sw] = 2
                            gMC_i[_MYCHAR_xm] = 0
                            gMC_i[_MYCHAR_ym] = -0x5FF

                # Move left and right
                if gKey & _gKeyLeft and gMC_i[_MYCHAR_xm] > 0 - physics[_physics_max_dash]:
                    gMC_i[_MYCHAR_xm] -= physics[_physics_dash2]
                if gKey & _gKeyRight and gMC_i[_MYCHAR_xm] < physics[_physics_max_dash]:
                    gMC_i[_MYCHAR_xm] += physics[_physics_dash2]
                if gKey & _gKeyLeft:
                    gMC_i[_MYCHAR_direct] = 0
                if gKey & _gKeyRight:
                    gMC_i[_MYCHAR_direct] = 2

            # Slow down when stopped boosting (Booster 2.0)
            if gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_2_0 and gMC_i[_MYCHAR_boost_sw] != 0 and (gKey & _gKeyJump or gMC_i[_MYCHAR_boost_cnt] == 0):
                if gMC_i[_MYCHAR_boost_sw] == 1:
                    gMC_i[_MYCHAR_xm] //= 2
                elif gMC_i[_MYCHAR_boost_sw] == 2:
                    gMC_i[_MYCHAR_ym] //= 2

            # Stop boosting
            if gMC_i[_MYCHAR_boost_cnt] == 0 or gKey & _gKeyJump:
                gMC_i[_MYCHAR_boost_sw] = 0

    @micropython.viper
    def ActMyChar_Normal_2(self, bKey: bool, gMC_i: ptr32, gKey: int, gKeyTrg: int, physics: ptr16):
        flag = gMC_i[_MYCHAR_flag]
        # Jumping
        if bKey:
            # Look up and down
            if gKey & _gKeyUp:
                gMC_i[_MYCHAR_up] = True
            else:
                gMC_i[_MYCHAR_up] = False
            if gKey & _gKeyDown and not flag & 0x08:
                gMC_i[_MYCHAR_down] = True
            else:
                gMC_i[_MYCHAR_down] = False
            if gKeyTrg & _gKeyJump and flag & 0x38 and not flag & 0x2000:
                gMC_i[_MYCHAR_ym] = 0 - physics[_physics_jump]
                #PlaySoundObject(15, SOUND_MODE_PLAY)
                
            # Stop interacting when moved
            if gKey & (_gKeyLeft | _gKeyRight | _gKeyUp | _gKeyShot | _gKeyJump):
                gMC_i[_MYCHAR_cond] &= ~1

        # Booster losing fuel
        if gMC_i[_MYCHAR_boost_sw] != 0 and gMC_i[_MYCHAR_boost_cnt] != 0:
            gMC_i[_MYCHAR_boost_cnt] -= 1

        # Wind / current forces
        if flag & 0x1000:
            gMC_i[_MYCHAR_xm] -= 0x88
        if flag & 0x2000:
            gMC_i[_MYCHAR_ym] -= 0x80
        if flag & 0x4000:
            gMC_i[_MYCHAR_xm] += 0x88
        if flag & 0x8000:
            gMC_i[_MYCHAR_ym] += 0x55

        # Booster 2.0 forces and effects
        if gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_2_0 and gMC_i[_MYCHAR_boost_sw] != 0:
            if gMC_i[_MYCHAR_boost_sw] == 1:
                # Go up when going into a wall
                if flag & 5:
                    gMC_i[_MYCHAR_ym] = -0x100

                # Move in direction facing
                if gMC_i[_MYCHAR_direct] == 0:
                    gMC_i[_MYCHAR_xm] -= 0x20
                elif gMC_i[_MYCHAR_direct] == 2:
                    gMC_i[_MYCHAR_xm] += 0x20

                # Boost particles (and sound)
                #if gKeyTrg & _gKeyJump or (gMC_i[_MYCHAR_boost_cnt] % 3) == 1:
                    #if gMC_i[_MYCHAR_direct] == 0:
                        #SetCaret(gMC_i[_MYCHAR_x] + (2 * 0x200), gMC_i[_MYCHAR_y] + (2 * 0x200), CARET_EXHAUST, _DIR_RIGHT)
                    #if gMC_i[_MYCHAR_direct] == 2:
                        #SetCaret(gMC_i[_MYCHAR_x] - (2 * 0x200), gMC_i[_MYCHAR_y] + (2 * 0x200), CARET_EXHAUST, _DIR_LEFT)
                    #PlaySoundObject(113, SOUND_MODE_PLAY)

            elif gMC_i[_MYCHAR_boost_sw] == 2:
                # Move upwards
                gMC_i[_MYCHAR_ym] -= 0x20

                # Boost particles (and sound)
                #if (gKeyTrg & _gKeyJump) or (gMC_i[_MYCHAR_boost_cnt] % 3) == 1:
                    #SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] + (6 * 0x200), CARET_EXHAUST, _DIR_DOWN)
                    #PlaySoundObject(113, SOUND_MODE_PLAY)

            #elif gMC_i[_MYCHAR_boost_sw] == 3 and ((gKeyTrg & _gKeyJump) or (gMC_i[_MYCHAR_boost_cnt] % 3) == 1):
                # Boost particles (and sound)
                #SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] - (6 * 0x200), CARET_EXHAUST, _DIR_UP)
                #PlaySoundObject(113, SOUND_MODE_PLAY)

        # Upwards wind/current
        elif flag & 0x2000:
            gMC_i[_MYCHAR_ym] += physics[_physics_gravity1]
        
        # Booster 0.8
        elif gMC_i[_MYCHAR_equip] & _EQUIP_BOOSTER_0_8 and gMC_i[_MYCHAR_boost_sw] != 0 and gMC_i[_MYCHAR_ym] > -0x400:
            # Upwards force
            gMC_i[_MYCHAR_ym] -= 0x20
            #if (gMC_i[_MYCHAR_boost_cnt] % 3) == 0:
                #SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] + (gMC.hit[_BOTTOM] // 2), CARET_EXHAUST, _DIR_DOWN)
                #PlaySoundObject(113, SOUND_MODE_PLAY)

            # Bounce off of ceiling
            if flag & 2 :
                gMC_i[_MYCHAR_ym] = 0x200
        
        # Gravity while jump is held
        elif gMC_i[_MYCHAR_ym] < 0 and bKey and gKey & _gKeyJump:
            gMC_i[_MYCHAR_ym] += physics[_physics_gravity2]
        # Normal gravity
        else:
            gMC_i[_MYCHAR_ym] += physics[_physics_gravity1]
        
        # Keep player on slopes
        if not bKey or not (gKeyTrg & _gKeyJump):
            if flag & 0x10 and gMC_i[_MYCHAR_xm] < 0:
                gMC_i[_MYCHAR_ym] = 0 - gMC_i[_MYCHAR_xm]
            elif flag & 0x20 and gMC_i[_MYCHAR_xm] > 0:
                gMC_i[_MYCHAR_ym] = gMC_i[_MYCHAR_xm]
            elif (flag & 0x80008) == 0x80008 and gMC_i[_MYCHAR_xm] < 0:
                gMC_i[_MYCHAR_ym] = 0x400
            elif (flag & 0x10008) == 0x10008 and gMC_i[_MYCHAR_xm] > 0:
                gMC_i[_MYCHAR_ym] = 0x400
            elif (flag & 0x60008) == 0x60008:
                gMC_i[_MYCHAR_ym] = 0x400

    @micropython.viper
    def ActMyChar_Normal_3(self, bKey: bool, gMC_i: ptr32, gKey: int, gKeyTrg: int, physics: ptr16):
        # Limit speed
        max_move = 0
        if gMC_i[_MYCHAR_flag] & 0x100 and (gMC_i[_MYCHAR_flag] & (0x8000 | 0x4000 | 0x2000 | 0x1000)) == 0:
            max_move = int(self._physics_underwater[_physics_max_move])    # Underwater or in wind
        else:
            max_move = int(self._physics_normal[_physics_max_move])    # Normal conditions

        gMC_i[_MYCHAR_xm] = int(sorted([0-max_move, gMC_i[_MYCHAR_xm], max_move])[1])
        gMC_i[_MYCHAR_ym] = int(sorted([0-max_move, gMC_i[_MYCHAR_ym], max_move])[1])
        
        # Water splashing
        if gMC_i[_MYCHAR_no_splash_or_air_limit_underwater] == 0 and not gMC_i[_MYCHAR_sprash] and gMC_i[_MYCHAR_flag] & 0x100:
            direct = 0
            if (gMC_i[_MYCHAR_flag] & 0x800) != 0:
                direct = 2
            else:
                direct = 0

            if not gMC_i[_MYCHAR_flag] & 8 and gMC_i[_MYCHAR_ym] > 0x200:
                for a in range(8):
                    x = gMC_i[_MYCHAR_x] + (int(randrange(-8, 8)) * 0x200)
                    #SetNpChar(73, x, gMC_i[_MYCHAR_y], gMC_i[_MYCHAR_xm] + randrange(-0x200, 0x200), randrange(-0x200, 0x80) - (gMC_i[_MYCHAR_ym] // 2), direct, NULL, 0)
                #PlaySoundObject(56, SOUND_MODE_PLAY)
            else:
                if gMC_i[_MYCHAR_xm] > 0x200 or gMC_i[_MYCHAR_xm] < -0x200:
                    for a in range(8):
                        x = gMC_i[_MYCHAR_x] + (int(randrange(-8, 8)) * 0x200)
                        #SetNpChar(73, x, gMC_i[_MYCHAR_y], gMC_i[_MYCHAR_xm] + randrange(-0x200, 0x200), randrange(-0x200, 0x80), direct, NULL, 0)
                    #PlaySoundObject(56, SOUND_MODE_PLAY)
            gMC_i[_MYCHAR_sprash] = True

        if not gMC_i[_MYCHAR_flag] & 0x100:
            gMC_i[_MYCHAR_sprash] = False

        # Spike damage
        #if gMC_i[_MYCHAR_flag] & 0x400:
            #DamageMyChar(10)
            
        # Camera
        if gMC_i[_MYCHAR_direct] == 0:
            gMC_i[_MYCHAR_index_x] -= _FRAME_CHASE
            if (gMC_i[_MYCHAR_index_x] < -_FRAME_OFFSET_X):
                gMC_i[_MYCHAR_index_x] = -_FRAME_OFFSET_X
        else:
            gMC_i[_MYCHAR_index_x] += _FRAME_CHASE
            if (gMC_i[_MYCHAR_index_x] > _FRAME_OFFSET_X):
                gMC_i[_MYCHAR_index_x] = _FRAME_OFFSET_X
        if gKey & _gKeyUp and bKey:
            gMC_i[_MYCHAR_index_y] -= _FRAME_CHASE
            if (gMC_i[_MYCHAR_index_y] < -_FRAME_OFFSET_Y):
                gMC_i[_MYCHAR_index_y] = -_FRAME_OFFSET_Y
        elif gKey & _gKeyDown and bKey: 
            # better camera on thumby when flying upward using a machine gun
            ArmsItem = self.ArmsItem
            gSelectedArms = int(ArmsItem.gSelectedArms)
            arms = ptr8(ArmsItem.gArmsData[gSelectedArms])
            if gKey & _gKeyShot and arms[_ARMS_code] == 4 and arms[_ARMS_level] == 3:
                gMC_i[_MYCHAR_jump_y] = gMC_i[_MYCHAR_y]
                gMC_i[_MYCHAR_index_y] -= _FRAME_CHASE
                if (gMC_i[_MYCHAR_index_y] < -_FRAME_OFFSET_Y):
                    gMC_i[_MYCHAR_index_y] = -_FRAME_OFFSET_Y
            else:
                # vanilla behavior for looking down
                gMC_i[_MYCHAR_index_y] += _FRAME_CHASE
                max_y = _FRAME_OFFSET_Y
                if not gMC_i[_MYCHAR_flag] & 0x38:
                    max_y = max_y << 1
                if (gMC_i[_MYCHAR_index_y] > max_y):
                    gMC_i[_MYCHAR_index_y] = max_y
                
        # move camera below player when falling
        elif not gMC_i[_MYCHAR_flag] & 0x38 and gMC_i[_MYCHAR_ym] > 0:
            if gMC_i[_MYCHAR_index_y] < gMC_i[_MYCHAR_ym] << 2:
                gMC_i[_MYCHAR_index_y] = gMC_i[_MYCHAR_ym] << 2
            if gMC_i[_MYCHAR_y] > gMC_i[_MYCHAR_jump_y]:
                pan_speed = gMC_i[_MYCHAR_ym] >> 2
                gMC_i[_MYCHAR_index_y] += pan_speed
                if (gMC_i[_MYCHAR_index_y] > _FRAME_OFFSET_Y << 1):
                    gMC_i[_MYCHAR_index_y] = _FRAME_OFFSET_Y << 1
        else:
            if (gMC_i[_MYCHAR_index_y] > _FRAME_CHASE):
                gMC_i[_MYCHAR_index_y] -= _FRAME_CHASE
            if (gMC_i[_MYCHAR_index_y] < -_FRAME_CHASE):
                gMC_i[_MYCHAR_index_y] += _FRAME_CHASE
        if gMC_i[_MYCHAR_flag] & 0x38:
            gMC_i[_MYCHAR_jump_y] = gMC_i[_MYCHAR_y]
        
        gMC_i[_MYCHAR_tgt_x] = gMC_i[_MYCHAR_x] + gMC_i[_MYCHAR_index_x]
        gMC_i[_MYCHAR_tgt_y] = gMC_i[_MYCHAR_y] + gMC_i[_MYCHAR_index_y]
        
        # Change position
        if gMC_i[_MYCHAR_xm] > physics[_physics_resist] or gMC_i[_MYCHAR_xm] < 0 - physics[_physics_resist]:
            gMC_i[_MYCHAR_x] += gMC_i[_MYCHAR_xm]
        gMC_i[_MYCHAR_y] += gMC_i[_MYCHAR_ym]

    @micropython.viper
    def ActMyChar_Normal(self, bKey: bool):
        gMC = self.gMC
        gMC_i = ptr16(gMC.i)
        KeyControl_i = ptr8(self.KeyControl.i)
        gKey = KeyControl_i[_gKey]
        gKeyTrg = KeyControl_i[_gKeyTrg]
    
        # Get speeds and accelerations
        if gMC_i[_MYCHAR_cond] & 2:
            return
        physics = ptr16(self._physics_underwater if gMC_i[_MYCHAR_flag] & 0x100 else self._physics_normal)

        # split the movement into subroutines for viper
        self.ActMyChar_Normal_1(bKey, gMC_i, gKey, gKeyTrg, physics)
        self.ActMyChar_Normal_2(bKey, gMC_i, gKey, gKeyTrg, physics)
        self.ActMyChar_Normal_3(bKey, gMC_i, gKey, gKeyTrg, physics)

    @micropython.viper
    def ActMyChar_Stream(self, bKey: bool):
        gMC = self.gMC
        gMC_i = ptr32(gMC.i)
        KeyControl_i = ptr8(self.KeyControl.i)
        gKey = KeyControl_i[_gKey]
        gKeyTrg = KeyControl_i[_gKeyTrg]
        xm = gMC_i[_MYCHAR_xm]
        ym = gMC_i[_MYCHAR_ym]
    
        gMC_i[_MYCHAR_up] = False
        gMC_i[_MYCHAR_down] = False
        
        if bKey and gKey & _gKeyLeft:
            xm -= 0x100
        elif bKey and gKey & _gKeyRight:
            xm += 0x100
        elif xm < 0x80 and ((bKey and xm > -0x80) or xm > -0x40):
            xm = 0
        elif xm > 0:
            xm -= 0x80
        elif xm < 0:
            xm += 0x80

        if bKey and gKey & _gKeyUp:
            ym -= 0x100
        elif bKey and gKey & _gKeyDown:
            ym += 0x100
        elif ym < 0x80 and ((bKey and ym > -0x80) or ym > -0x40):
            ym = 0
        elif (ym > 0):
            ym -= 0x80
        elif (ym < 0):
            ym += 0x80

        if ym < -0x200 and gMC_i[_MYCHAR_flag] & 2:
            hit = ptr16(gMC.hit)
            SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] - hit[_TOP], _CARET_TINY_PARTICLES, _DIR_OTHER)
        if ym > 0x200 and gMC_i[_MYCHAR_flag] & 8:
            hit = ptr16(gMC.hit)
            SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] + hit[_BOTTOM], _CARET_TINY_PARTICLES, _DIR_OTHER)

        max_speed_pos = 0x400
        if gKey & (_gKeyLeft | _gKeyRight) and gKey & (_gKeyUp | _gKeyDown):
            max_speed_pos = 780
        max_speed_neg = 0 - max_speed_pos

        if xm > max_speed_pos:
            xm = max_speed_pos
        if xm < max_speed_neg:
            xm = max_speed_neg
            
        if ym > max_speed_pos:
            ym = max_speed_pos
        if ym < max_speed_neg:
            ym = max_speed_neg
      
        gMC_i[_MYCHAR_xm] = xm
        gMC_i[_MYCHAR_ym] = ym
        gMC_i[_MYCHAR_x] += xm
        gMC_i[_MYCHAR_y] += ym

    @micropython.viper
    def AirProcess(self):
        gMC_i = ptr32(self.gMC.i)
        if (gMC_i[_MYCHAR_equip] & _EQUIP_AIR_TANK):
            gMC_i[_MYCHAR_air] = 1000
            gMC_i[_MYCHAR_air_get] = 0
        else:
            if not (gMC_i[_MYCHAR_flag] & 0x100) or gMC_i[_MYCHAR_no_splash_or_air_limit_underwater] > 0:
                gMC_i[_MYCHAR_air] = 1000
            else:
                gMC_i[_MYCHAR_air] -= 1
                if gMC_i[_MYCHAR_air] <= 0:
                    if GetNPCFlag(4000):
                        # Core cutscene
                        StartTextScript(1100)
                    else:
                        # Drown
                        StartTextScript(41)
                        if gMC_i[_MYCHAR_direct] == 0:
                            SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y], CARET_DROWNED_QUOTE, _DIR_LEFT)
                        else:
                            SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y], CARET_DROWNED_QUOTE, _DIR_RIGHT)
                        gMC_i[_MYCHAR_cond] &= ~0x80
                    
            if (gMC_i[_MYCHAR_flag] & 0x100):
                gMC_i[_MYCHAR_air_get] = 60
            elif gMC_i[_MYCHAR_air_get] != 0:
                gMC_i[_MYCHAR_air_get] -= 1

    @micropython.viper
    def ActMyChar(self, bKey: bool):
        gMC_i = ptr32(self.gMC.i)

        if (gMC_i[_MYCHAR_cond] & 0x80) == 0:
            return

        if gMC_i[_MYCHAR_exp_wait] > 0:
            gMC_i[_MYCHAR_exp_wait] -= 1

        if gMC_i[_MYCHAR_shock] > 0:
            gMC_i[_MYCHAR_shock] -= 1
        elif gMC_i[_MYCHAR_exp_count] != 0:
            #self.SetValueView(&self.x, &self.y, self.exp_count)
            gMC_i[_MYCHAR_exp_count] = 0

        if gMC_i[_MYCHAR_unit] == 0:
            if (int(self.g_GameFlags[0]) & 0x04) == 0 and bKey:
                self.AirProcess()
            self.ActMyChar_Normal(bKey)
        elif gMC_i[_MYCHAR_unit] == 1:
            self.ActMyChar_Stream(bKey)

        gMC_i[_MYCHAR_cond] &= ~0x20
