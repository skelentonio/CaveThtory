from array import array
from random import randrange

_WindowWidth = const(72)
_WindowHeight = const(40)
_x_delta = const(0 - ((_WindowWidth - 320) // 2) * 0x200)
_y_delta = const(0 - ((_WindowHeight - 240) // 2) * 0x200)
_sub_w = const((_WindowWidth) * 0x200 // 2)
_sub_l = const((_WindowHeight) * 0x200 // 2)

_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_MYCHAR_tgt_x = const(7)

#def FRAME():
_FRAME_x = const(0)
_FRAME_y = const(1)
_FRAME_wait = const(2) # vanilla 16
_FRAME_quake = const(3)
_FRAME_quake2 = const(4)
_FRAME_map_w = const(5)
_FRAME_map_l = const(6)
_FRAME_min_w = const(7)
_FRAME_min_l = const(8)
_FRAME_bound_w = const(9)
_FRAME_bound_l = const(10)

class Frame:
    def __init__(self, MyChar, g_GameFlags):
        self.MyChar = MyChar
        self.g_GameFlags = g_GameFlags
        self.gFrame = array('i', 0 for i in range(11)) # FRAME()
        self.tgt_ptr = 0 # we use this to point directly to an array containing tgt_x and tgt_y
        self.tgt_ptr_offset = 0 # this is the offset in tgt_ptr to read from
  
    @micropython.viper
    def GetFramePosition(self):
        gFrame = ptr32(self.gFrame)
        return gFrame[_FRAME_x], gFrame[_FRAME_y]
        
    @micropython.viper
    def MoveFrame3(self):
        gFrame = ptr32(self.gFrame)
        tgt_ptr = ptr32(self.tgt_ptr)
        tgt_ptr_offset = int(self.tgt_ptr_offset)
        gFrame_tgt_x = tgt_ptr[tgt_ptr_offset]
        gFrame_tgt_y = tgt_ptr[tgt_ptr_offset+1]
        gFrame_x = gFrame[_FRAME_x]
        gFrame_y = gFrame[_FRAME_y]
        gFrame_wait = gFrame[_FRAME_wait]
        map_w = gFrame[_FRAME_map_w]
        map_l = gFrame[_FRAME_map_l]
        min_w = gFrame[_FRAME_min_w]
        min_l = gFrame[_FRAME_min_l]
        bound_w = gFrame[_FRAME_bound_w]
        bound_l = gFrame[_FRAME_bound_l]

        if int(self.g_GameFlags[0]) & 0x08:
            # Use the original camera boundaries during the credits
            gFrame_x += (_x_delta + gFrame_tgt_x - 0x14000 - gFrame_x) // gFrame_wait
            gFrame_y += (_y_delta + gFrame_tgt_y - 0xf000 - gFrame_y) // gFrame_wait

            if gFrame_x < _x_delta:
                gFrame_x = _x_delta
            if gFrame_y < _y_delta:
                gFrame_y = _y_delta

            if gFrame_x > _x_delta + ((map_w * 16) - 320) * 0x200:
                gFrame_x = _x_delta + ((map_w * 16) - 320) * 0x200
            if gFrame_y > _y_delta + ((map_l * 16) - 240) * 0x200:
                gFrame_y = _y_delta + ((map_l * 16) - 240) * 0x200 
        else:
            # Widescreen/tallscreen-safe behaviour
            if min_w < _WindowWidth:
                gFrame_x = 0 - (((_WindowWidth - min_w) * 0x200) // 2)
            else:
                gFrame_x += (gFrame_tgt_x - _sub_w - gFrame_x) // gFrame_wait
                if gFrame_x < 0:
                    gFrame_x = 0
                if gFrame_x > bound_w:
                    gFrame_x = bound_w
 
            if min_l < _WindowHeight:
                gFrame_y = 0 - (((_WindowHeight - min_l) * 0x200) // 2)
            else:
                gFrame_y += (gFrame_tgt_y - _sub_l - gFrame_y) // gFrame_wait
                if gFrame_y < 0:
                    gFrame_y = 0
                if gFrame_y > bound_l:
                    gFrame_y = bound_l
            
        # Vanilla behaviour
        gFrame_x += (gFrame_tgt_x - _sub_w - gFrame_x) // gFrame_wait
        gFrame_y += (gFrame_tgt_y - _sub_l - gFrame_y) // gFrame_wait

        if gFrame_x < 0:
            gFrame_x = 0
        if gFrame_y < 0:
            gFrame_y = 0

        if gFrame_x > (min_w - _WindowWidth) * 0x200:
            gFrame_x = (min_w - _WindowWidth) * 0x200
        if gFrame_y > (min_l - _WindowHeight) * 0x200:
            gFrame_y = (min_l - _WindowHeight) * 0x200

        if gFrame[_FRAME_quake2] > 0:
            gFrame_x += (int(randrange(-5, 5)) * 0x200)
            gFrame_y += (int(randrange(-3, 3)) * 0x200)
            gFrame[_FRAME_quake2] -= 1
        elif gFrame[_FRAME_quake] > 0:
            gFrame_x += (int(randrange(-1, 1)) * 0x200)
            gFrame_y += (int(randrange(-1, 1)) * 0x200)
            gFrame[_FRAME_quake] -= 1
            
        gFrame[_FRAME_x] = gFrame_x
        gFrame[_FRAME_y] = gFrame_y

    @micropython.viper
    def SetFrameMyChar(self):
        # Move frame position
        gFrame = ptr32(self.gFrame)
        gMC_i = ptr32(self.MyChar.gMC.i)
        mc_x = gMC_i[_MYCHAR_x]
        mc_y = gMC_i[_MYCHAR_y]
        map_w = gFrame[_FRAME_map_w]
        map_l = gFrame[_FRAME_map_l]
        min_w = gFrame[_FRAME_min_w]
        min_l = gFrame[_FRAME_min_l]
        bound_w = gFrame[_FRAME_bound_w]
        bound_l = gFrame[_FRAME_bound_l]

        gFrame_x = mc_x - ((_WindowWidth // 2) * 0x200)
        gFrame_y = mc_y - ((_WindowHeight // 2) * 0x200)

        # Keep in bounds
        if int(self.g_GameFlags[0]) & 8:
            # Use the original camera boundaries during the credits
            if gFrame_x < _x_delta:
                gFrame_x = _x_delta
            if gFrame_y < _y_delta:
                gFrame_y = _y_delta
                
            if gFrame_x > _x_delta + (((map_w - 1) * 16) - 320) * 0x200:
                gFrame_x = _x_delta + (((map_w - 1) * 16) - 320) * 0x200
            if gFrame_y > _y_delta + (((map_l - 1) * 16) - 240) * 0x200:
                gFrame_y = _y_delta + (((map_l - 1) * 16) - 240) * 0x200
        else:
            # Widescreen/tallscreen-safe behaviour
            if min_w < _WindowWidth:
                gFrame_x = 0 - (((_WindowWidth - min_w) * 0x200) // 2)
            else:
                if gFrame_x < 0:
                    gFrame_x = 0
                if gFrame_x > bound_w:
                    gFrame_x = bound_w
 
            if min_l < _WindowHeight:
                gFrame_y = 0 - (((_WindowHeight - min_l) * 0x200) // 2)
            else:
                if gFrame_y < 0:
                    gFrame_y = 0
                if gFrame_y > bound_l:
                    gFrame_y = bound_l

        # Vanilla behaviour
        if gFrame_x < 0:
            gFrame_x = 0
        if gFrame_y < 0:
            gFrame_y = 0

        if gFrame_x > (min_w - _WindowWidth) * 0x200:
            gFrame_x = (min_w - _WindowWidth) * 0x200
        if gFrame_y > (min_l - _WindowHeight) * 0x200:
            gFrame_y = (min_l - _WindowHeight) * 0x200

        gFrame[_FRAME_x] = gFrame_x
        gFrame[_FRAME_y] = gFrame_y

    @micropython.native
    def SetFrameTargetMyChar(self, wait):
        gFrame = self.gFrame
        gFrame[_FRAME_wait] = wait
        self.tgt_ptr = self.MyChar.gMC.i
        self.tgt_ptr_offset = _MYCHAR_tgt_x
        
    @micropython.viper
    def ResetQuake(self):
        gFrame = ptr32(self.gFrame)
        gFrame[_FRAME_quake] = 0;
        gFrame[_FRAME_quake2] = 0;
