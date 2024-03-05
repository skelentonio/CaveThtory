_WindowWidth = const(72)
_WindowHeight = const(40)

_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_FRAME_map_w = const(5)
_FRAME_map_l = const(6)
_FRAME_min_w = const(7)
_FRAME_min_l = const(8)
_FRAME_bound_w = const(9)
_FRAME_bound_l = const(10)

class Stage:
    def __init__(self, Map, Frame, Back, Bullet, TextScr, gMC):
        self.Frame = Frame
        self.Back = Back
        self.Bullet = Bullet
        self.TextScr = TextScr
        self.gMC = gMC
        self.Map = Map
        self.gStageNo = 0

    @micropython.viper
    def TransferStage(self, no: int, w: int, x: int, y: int) -> bool:
        Map = self.Map
    
        # Get path
        path_dir = "stage"

        #path = path_dir + '/' + gTMT[no].parts + ".pxa"
        path = path_dir + "/Mimi.pxa" ## for testing
        Map.LoadAttributeData(path)

        # Load tilemap
        #path = path_dir + '/' + gTMT[no].map + ".pxm"
        path = path_dir + "/Mimi.pxm" ## for testing
        Map.LoadMapData2(path)
        
        # Load tileset
        #path = path_dir + "/Prt" + gTMT[no].parts
        path = path_dir + "/PrtMimi" ## for testing
        Map.LoadTiles(path)

        # Load NPCs
        #path = path_dir + '/' + gTMT[no].map + ".pxe"
        #if (!LoadEvent(path.c_str()))
        #    bError = TRUE

        # Load script
        #path = path_dir + '/' + gTMT[no].map + ".tsc"
        path = path_dir + "/mimi.tsc"
        #self.TextScr.LoadTextScript_Stage(path)

        # Load background
        #path = gTMT[no].back
        path = "bkBlue" ## for testing
        bkType = 0
        self.Back.InitBack(path, bkType)

        '''# Get path
        path_dir = "Npc"

        # Load NPC sprite sheets
        path = path_dir + "/Npc" + gTMT[no].npc
        if (!ReloadBitmap_File(path.c_str()))
            bError = TRUE

        path = path_dir + "/Npc" + gTMT[no].boss
        if (!ReloadBitmap_File(path.c_str()))
            bError = TRUE'''

        # Load map name
        #ReadyMapName(gTMT[no].name)
        
        # set frame bounds
        gFrame = ptr32(self.Frame.gFrame)
        gFrame[_FRAME_map_w] = int(Map.gMap.width) - 1
        gFrame[_FRAME_map_l] = int(Map.gMap.length) - 1
        gFrame[_FRAME_bound_w] = ((gFrame[_FRAME_map_w] * 16) - _WindowWidth) * 0x200
        gFrame[_FRAME_bound_l] = ((gFrame[_FRAME_map_l] * 16) - _WindowHeight) * 0x200
        gFrame[_FRAME_min_w] = gFrame[_FRAME_map_w] * 16
        gFrame[_FRAME_min_l] = gFrame[_FRAME_map_l] * 16
        
        # position the player
        gMC_i = ptr32(self.gMC.i)
        gMC_i[_MYCHAR_x] = x * 0x2000
        gMC_i[_MYCHAR_y] = y * 0x2000

        #StartTextScript(w)
        self.Frame.SetFrameMyChar()
        self.Bullet.InitBullet()
        #InitCaret()
        #ClearValueView()
        self.Frame.ResetQuake()
        #InitBossChar(gTMT[no].boss_no)
        #ResetFlash()
        self.gStageNo = no
        
        return True
