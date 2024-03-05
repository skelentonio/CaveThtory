_gKey = const(0)
_gKeyTrg = const(1)
_gKeyShot = const(0x00000020)

_EQUIP_TURBOCHARGE = const(0x08)
_CARET_SHOOT = const(3)

_MYCHAR_cond = const(0)
_MYCHAR_direct = const(2)
_MYCHAR_equip = const(4)
_MYCHAR_x = const(5)
_MYCHAR_y = const(6)
_MYCHAR_ym = const(12)
_MYCHAR_rensha = const(20)
_MYCHAR_up = const(34) # bool
_MYCHAR_down = const(35) # bool

_ARMS_code = const(0)
_ARMS_level = const(1)

@micropython.viper
def SHOOT():
    return bytearray(3)
_SHOOT_soft_rensha = const(0) # 'rensha' is Japanese for 'rapid-fire'
_SHOOT_empty = const(1)
_SHOOT_wait = const(2)

class Shoot:
    def __init__(self, KeyControl, Bullet, Caret, MyChar, ArmsItem):
        self.KeyControl = KeyControl
        self.Bullet = Bullet
        self.Caret = Caret
        self.MyChar = MyChar
        self.ArmsItem = ArmsItem
        self.gArmsData = ArmsItem.gArmsData
        self.gSelectedArms = ArmsItem.gSelectedArms
        self.i = SHOOT()
        self.Bullet.LoadSprites(((int(self.gArmsData[0][0]) - 1) * 3) + int(self.gArmsData[0][1])) ## preload the weapon we are using for debug
        
    @micropython.viper
    def ShootBullet_Frontia1(self, level: int):
        if not int(self.KeyControl.i[_gKeyTrg]) & _gKeyShot:
            return
            
        Bullet = self.Bullet
        if int(self.Bullet.CountArmsBullet(1)) > 3:
            return
            
        gMC_i = ptr32(self.MyChar.gMC.i)
        x = 0x600
        y = 0x2000
        direct = gMC_i[_MYCHAR_direct]
        if gMC_i[_MYCHAR_up]:
            direct = 1
            y = 0-y
        elif gMC_i[_MYCHAR_down]:
            direct = 3
        else:
            x = 0xc00
            y = 0x400
        if gMC_i[_MYCHAR_direct] == 0:
            x = 0-x
        
        Bullet.SetBullet(level, gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, direct)
        #SetCaret(gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, _CARET_SHOOT, 0)
        #PlaySoundObject(33, SOUND_MODE_PLAY)

    @micropython.viper
    def ShootBullet_PoleStar(self, level: int):
        if not int(self.KeyControl.i[_gKeyTrg]) & _gKeyShot:
            return
    
        bul_no = 3 + level
        Bullet = self.Bullet
        if int(Bullet.CountArmsBullet(2)) > 1:
            return

        gMC_i = ptr32(self.MyChar.gMC.i)
        x = 0x200
        y = 0x1000
        direct = gMC_i[_MYCHAR_direct]
        if gMC_i[_MYCHAR_up]:
            direct = 1
            y = 0-y
        elif gMC_i[_MYCHAR_down]:
            direct = 3
        else:
            x = 0xc00
            y = 0x600
        if gMC_i[_MYCHAR_direct] == 0:
            x = 0-x

        Bullet.SetBullet(bul_no, gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, direct)
        #SetCaret(gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, _CARET_SHOOT, 0)

        #if (level == 3)
        #    PlaySoundObject(49, SOUND_MODE_PLAY)
        #else
        #    PlaySoundObject(32, SOUND_MODE_PLAY)
        
    @micropython.viper
    def ShootBullet_FireBall(self, level: int):
        if not int(self.KeyControl.i[_gKeyTrg]) & _gKeyShot:
            return

        bul_no = 6 + level
        Bullet = self.Bullet
        if int(Bullet.CountArmsBullet(3)) > level:
            return

        gMC_i = ptr32(self.MyChar.gMC.i)
        x = 0x800
        y = 0x1000
        direct = gMC_i[_MYCHAR_direct]
        if gMC_i[_MYCHAR_up]:
            direct = 1
            y = 0-y
        elif gMC_i[_MYCHAR_down]:
            direct = 3
        else:
            x = 0xc00
            y = 0x400
        if gMC_i[_MYCHAR_direct] == 0:
            x = 0-x
        
        Bullet.SetBullet(bul_no, gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, direct)
        #SetCaret(gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, _CARET_SHOOT, 0)
        #PlaySoundObject(34, SOUND_MODE_PLAY)
        
    @micropython.viper
    def ShootBullet_Machinegun1(self, level: int):
        if int(self.Bullet.CountArmsBullet(4)) > 4:
            return
            
        bul_no = 9 + level
        shoot_i = ptr8(self.i)
        gMC_i = ptr32(self.MyChar.gMC.i)
        if not int(self.KeyControl.i[_gKey]) & _gKeyShot:
            gMC_i[_MYCHAR_rensha] = 6
            shoot_i[_SHOOT_wait] += 1
            if shoot_i[_SHOOT_wait] > 4 or (gMC_i[_MYCHAR_equip] & _EQUIP_TURBOCHARGE and shoot_i[_SHOOT_wait] > 1):
                if shoot_i[_SHOOT_wait] > 1:
                    shoot_i[_SHOOT_wait] = 0
                    self.ArmsItem.ChargeArmsEnergy(1)

        else:
            gMC_i[_MYCHAR_rensha] += 1
            if gMC_i[_MYCHAR_rensha] < 6:
                return
            gMC_i[_MYCHAR_rensha] = 0
            
            if not self.ArmsItem.UseArmsEnergy(1):
                #PlaySoundObject(37, SOUND_MODE_PLAY)
                if shoot_i[_SHOOT_empty] == 0:
                    #SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y], CARET_EMPTY, 0)
                    shoot_i[_SHOOT_empty] = 50
                return
            
            SetBullet = self.Bullet.SetBullet
            
            x = 0x600
            y = 0x1000
            direct = gMC_i[_MYCHAR_direct]
            if gMC_i[_MYCHAR_up]:
                direct = 1
                y = 0-y
                if level == 3:
                    gMC_i[_MYCHAR_ym] += 0x100
            elif gMC_i[_MYCHAR_down]:
                direct = 3
                if level == 3:
                    if gMC_i[_MYCHAR_ym] > 0:
                        gMC_i[_MYCHAR_ym] //= 2
                    if gMC_i[_MYCHAR_ym] > -0x400:
                        gMC_i[_MYCHAR_ym] -= 0x200
                        if gMC_i[_MYCHAR_ym] < -0x400:
                            gMC_i[_MYCHAR_ym] = -0x400
            else:
                x = 0x2400
                y = 0x600
            if gMC_i[_MYCHAR_direct] == 0:
                x = 0-x

            SetBullet(bul_no, gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, direct)
            #SetCaret(gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, _CARET_SHOOT, 0)

            #if (level == 3)
            #    PlaySoundObject(49, SOUND_MODE_PLAY)
            #else
            #    PlaySoundObject(32, SOUND_MODE_PLAY)
            
    @micropython.viper
    def ShootBullet_Missile(self, level: int, bSuper: bool):
        if not int(self.KeyControl.i[_gKeyTrg]) & _gKeyShot:
            return
    
        Bullet = self.Bullet
        if bSuper:
            bul_no = 27 + level
            if int(Bullet.CountArmsBullet(10)) > level - 1:
                return
            if int(Bullet.CountArmsBullet(11)) > level - 1:
                return
        else:
            bul_no = 12 + level
            if int(Bullet.CountArmsBullet(5)) > level - 1:
                return
            if int(Bullet.CountArmsBullet(6)) > level - 1:
                return

        if not self.ArmsItem.UseArmsEnergy(1):
            shoot_i = ptr8(self.i)
            #PlaySoundObject(37, SOUND_MODE_PLAY)
            if shoot_i[_SHOOT_empty] == 0:
                #SetCaret(gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y], CARET_EMPTY, 0)
                shoot_i[_SHOOT_empty] = 50
            return

        gMC_i = ptr32(self.MyChar.gMC.i)
        x = 0x200
        y = 0x1000
        direct = gMC_i[_MYCHAR_direct]
        if gMC_i[_MYCHAR_up]:
            direct = 1
            y = 0-y
        elif gMC_i[_MYCHAR_down]:
            direct = 3
        else:
            x = 0xc00
            y = 0
            if level == 3:
                y = 0x200
        if gMC_i[_MYCHAR_direct] == 0:
            x = 0-x

        SetBullet = Bullet.SetBullet
        SetBullet(bul_no, gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, direct)
        #SetCaret(gMC_i[_MYCHAR_x] + x, gMC_i[_MYCHAR_y] + y, _CARET_SHOOT, 0)

        if level == 3:
            if gMC_i[_MYCHAR_up] or gMC_i[_MYCHAR_down]:
                SetBullet(bul_no, gMC_i[_MYCHAR_x] + 0x600, gMC_i[_MYCHAR_y], direct)
                SetBullet(bul_no, gMC_i[_MYCHAR_x] - 0x600, gMC_i[_MYCHAR_y], direct)
            else:
                SetBullet(bul_no, gMC_i[_MYCHAR_x], gMC_i[_MYCHAR_y] - 0x1000, direct)
                if gMC_i[_MYCHAR_direct] == 0:
                    SetBullet(bul_no, gMC_i[_MYCHAR_x] + 0x800, gMC_i[_MYCHAR_y] - 0x200, direct)
                else:
                    SetBullet(bul_no, gMC_i[_MYCHAR_x] - 0x800, gMC_i[_MYCHAR_y] - 0x200, direct)

        #PlaySoundObject(32, SOUND_MODE_PLAY)
 
    @micropython.viper
    def ShootBullet(self):
        shoot_i = ptr8(self.i)
        
        if shoot_i[_SHOOT_empty] > 0:
            shoot_i[_SHOOT_empty] -= 1

        # Only let the player shoot every 4 frames
        soft_rensha = shoot_i[_SHOOT_soft_rensha] 
        if soft_rensha > 0:
            soft_rensha -= 1
        if int(self.KeyControl.i[_gKeyTrg]) & _gKeyShot:
            if soft_rensha > 0:
                return
            soft_rensha = 4
        shoot_i[_SHOOT_soft_rensha] = soft_rensha
        
        # Run functions
        if int(self.MyChar.gMC.i[_MYCHAR_cond]) & 2:
            return
            
        gSelectedArms = int(self.gSelectedArms)
        arms = ptr8(self.gArmsData[gSelectedArms])
        code = arms[_ARMS_code]
        level = arms[_ARMS_level]

        if code == 1:
            self.ShootBullet_Frontia1(level)
        elif code == 2:
            self.ShootBullet_PoleStar(level)
        elif code == 3:
            self.ShootBullet_FireBall(level)
        elif code == 4:
            self.ShootBullet_Machinegun1(level)
        elif code == 5:
            self.ShootBullet_Missile(level, False)
        elif code == 7:
            if level == 1:
                self.ShootBullet_Bubblin1()
            else:
                self.ShootBullet_Bubblin2(level)
        elif code == 9:
            self.ShootBullet_Sword(level)
        elif code == 10:
            self.ShootBullet_Missile(level, True)
        elif code == 12:
            self.ShootBullet_Nemesis(level)
        elif code == 13:
            self.ShootBullet_Spur(level)
