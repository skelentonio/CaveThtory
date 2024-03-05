import gc
import polysynth
import midi
gc.collect()
from display import display_update
gc.collect()
from MyChar import MyChar
gc.collect()
from Frame import Frame
gc.collect()
from Stage import Stage
gc.collect()
from MycHit import MycHit
gc.collect()
from KeyControl import KeyControl
gc.collect()
from Shoot import Shoot
gc.collect()
from Bullet import Bullet
gc.collect()
from BulHit import BulHit
gc.collect()
from Caret import Caret
gc.collect()
from Back import Back
gc.collect()
from Map import Map
gc.collect()
from ArmsItem import ArmsItem
gc.collect()
from TextScr import TextScr

gModulePath = "/Games/CaveStory"
gDataPath = gModulePath + "/data"

_WindowWidth = const(72)
_WindowHeight = const(40)
_FRAME_x = const(0)
_FRAME_y = const(1)

class grcGame:
    left = 0
    top = 0
    right = _WindowWidth
    bottom = _WindowHeight
 
class Game:
    def __init__(self):
        self.g_GameFlags = bytearray([0])
        self.KeyControl = KeyControl()
        self.ArmsItem = ArmsItem()
        self.MyChar = MyChar(self.KeyControl, self.ArmsItem, self.g_GameFlags)
        self.Frame = Frame(self.MyChar, self.g_GameFlags)
        self.Map = Map()
        self.Bullet = Bullet(self.MyChar)
        self.BulHit = BulHit(self.Bullet, self.Map.gMap)
        self.TextScr = TextScr()
        self.Back = Back()
        self.Stage = Stage(self.Map, self.Frame, self.Back, self.Bullet, self.TextScr, self.MyChar.gMC)
        self.Caret = Caret()
        self.Shoot = Shoot(self.KeyControl, self.Bullet, self.Caret, self.MyChar, self.ArmsItem)
        self.MycHit = MycHit(self.MyChar, self.Stage.Map.gMap, self.g_GameFlags)
        gc.collect()

    @micropython.viper
    def run(self):
        ## play some music for testing
        polysynth.configure()
        song = midi.load(open(gModulePath + "/data/midi/mura.mid", "rb"))
        polysynth.play(song, loop=True)
        
        #ModeOpening = self.ModeOpening
        #ModeTitle = self.ModeTitle
        ModeAction = self.ModeAction
        mode = 3
        while mode > 0:
            if mode == 1:
                mode = int(ModeOpening())
            if mode == 2:
                mode = int(ModeTitle())
            if mode == 3:
                mode = int(ModeAction())

    @micropython.viper
    def ModeAction(self) -> int:
        # Reset stuff
        frame_x = 0
        frame_y = 0
        gCounter = 0
        g_GameFlags_ptr = ptr8(self.g_GameFlags)
        g_GameFlags_ptr[0] = 3
        
        # Initialize everything
        self.MyChar.InitMyChar()
        #InitNpChar()
        self.Bullet.InitBullet()
        #InitCaret()
        #InitStar()
        #InitFade()
        #InitFlash()
        #ClearArmsData()
        #ClearItemData()
        #ClearPermitStage()
        #StartMapping()
        #InitFlags()
        #InitBossLife()
        
        self.Stage.TransferStage(0, 100, 8, 6) ## warp to level 0 for testing
        self.Frame.SetFrameTargetMyChar(8) ## for testing, set camera to target player. eventually move this to Profile.py

        #if (bContinue)
        #    if (!LoadProfile(NULL) && !InitializeGame()):
        #        return 0
        #else
        #    if (!InitializeGame()):
        #        return 0
        
        # extra preparation for python
        gFrame = ptr32(self.Frame.gFrame)
        GetTrg = self.KeyControl.GetTrg
        ActMyChar = self.MyChar.ActMyChar
        HitMyCharMap = self.MycHit.HitMyCharMap
        HitBulletMap = self.BulHit.HitBulletMap
        ShootBullet = self.Shoot.ShootBullet
        ActBullet = self.Bullet.ActBullet
        MoveFrame3 = self.Frame.MoveFrame3
        AnimationMyChar = self.MyChar.AnimationMyChar
        PutBack = self.Back.PutBack
        PutStage = self.Map.PutStage
        PutBullet = self.Bullet.PutBullet
        PutMyChar = self.MyChar.PutMyChar
        gc.collect()
        print("Free: " + str(gc.mem_free()))

        while (True):
            g_GameFlags = int(g_GameFlags_ptr[0])
            # Get pressed keys
            GetTrg()
            if g_GameFlags & 1:
                if g_GameFlags & 2:
                    ActMyChar(True)
                else:
                    ActMyChar(False)

                '''ActStar()
                ActNpChar()
                ActBossChar()
                ActValueView()
                ActBack()'''
                HitMyCharMap()
                #HitMyCharNpChar()
                #HitMyCharBoss()
                #HitNpCharMap()
                #HitBossMap()
                HitBulletMap()
                #HitNpCharBullet()
                #HitBossBullet()
                if g_GameFlags & 2:
                    ShootBullet()
                ActBullet()
                #ActCaret()
                MoveFrame3()
                frame_x = gFrame[_FRAME_x] # GetFramePosition
                frame_y = gFrame[_FRAME_y]
                #ActFlash(frame_x, frame_y)

                if g_GameFlags & 2:
                    AnimationMyChar(True)
                else:
                    AnimationMyChar(False)

            '''if (g_GameFlags & 8)
            
                ActionCredit()
                ActionIllust()
                ActionStripper()
           
            ProcFade()
            CortBox(&grcFull, color)'''
            frame_x = gFrame[_FRAME_x] # GetFramePosition
            frame_y = gFrame[_FRAME_y]
            PutBack() # background
            PutStage(frame_x, frame_y, 0)
            #PutBossChar(frame_x, frame_y)
            #PutNpChar(frame_x, frame_y)
            PutBullet(frame_x, frame_y)
            PutMyChar(frame_x, frame_y)
            #PutStar(frame_x, frame_y)
            #PutMapDataVector(frame_x, frame_y)
            PutStage(frame_x, frame_y, 1)
            #PutBlackBars(frame_x, frame_y)
            #PutFlash()
            #PutCaret(frame_x, frame_y)
            #PutValueView(frame_x, frame_y)
            #PutBossLife()
            #PutFade()

            '''if (!(g_GameFlags & 4))
                # Open inventory
                if (gKeyTrg & gKeyItem)
                
                    BackupSurface(SURFACE_ID_SCREEN_GRAB, &grcGame)

                    switch (CampLoop())
                    
                        case enum_ESCRETURN_exit:
                            return 0

                        case enum_ESCRETURN_restart:
                            return 1
                    

                    gMC.cond &= ~1
                
                else if (gMC.equip & _EQUIP_MAP && gKeyTrg & gKeyMap)
                
                    BackupSurface(SURFACE_ID_SCREEN_GRAB, &grcGame)

                    switch (MiniMapLoop())
                    
                        case enum_ESCRETURN_exit:
                            return 0

                        case enum_ESCRETURN_restart:
                            return 1
                    
                
            if (g_GameFlags & 2)
            
                if (gKeyTrg & gKeyArms)
                    RotationArms()
                else if (gKeyTrg & gKeyArmsRev)
                    RotationArmsRev()
            

            switch (TextScriptProc())
            
                case enum_ESCRETURN_exit:
                    return 0

                case enum_ESCRETURN_restart:
                    return 1
                
            

            PutMapName(FALSE)
            PutTimeCounter(16, 8)

            if (g_GameFlags & 2)
            
                PutMyLife(TRUE)
                PutArmsEnergy(TRUE)
                PutMyAir((_WindowWidth /// 2) - 40, (_WindowHeight // 2) - 16)
                PutActiveArmsList()
            

            if (g_GameFlags & 8)
            
                PutIllust()
                PutStripper()
            

            PutTextScript()

            PutFramePerSecound()

            if (!Flip_SystemTask())
                return 0

            ++gCounter'''
            display_update()
        return 0
        
Game().run()