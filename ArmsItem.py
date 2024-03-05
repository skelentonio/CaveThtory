@micropython.viper
def ARMS(code: int, level: int, max_num: int, num: int):
    return bytearray([code, level, 0, max_num, num])
_ARMS_code = const(0)
_ARMS_level = const(1)
_ARMS_exp = const(2)
_ARMS_max_num = const(3)
_ARMS_num = const(4)

class ArmsItem:
    def __init__(self):
        self.gArmsData = []
        self.gItemData = []
        self.gSelectedArms = 0
        self.gSelectedItem = 0
        
        self.gArmsData.append(ARMS(4, 3, 100, 100)) ## give us a gun for testing
        
    @micropython.viper
    def UseArmsEnergy(self, num: int) -> bool:
        gSelectedArms = int(self.gSelectedArms)
        arms = ptr8(self.gArmsData[gSelectedArms])
    
        if arms[_ARMS_max_num] == 0:
            return True	# No ammo needed
        if arms[_ARMS_num] == 0:
            return False	# No ammo left
        arms[_ARMS_num] -= num
        if arms[_ARMS_num] < 0:
            arms[_ARMS_num] = 0
        return True	# Was able to spend ammo

    @micropython.viper
    def ChargeArmsEnergy(self, num: int):
        gSelectedArms = int(self.gSelectedArms)
        arms = ptr8(self.gArmsData[gSelectedArms])
        arms[_ARMS_num] += num
        # Cap the ammo to the maximum ammunition
        if arms[_ARMS_num] > arms[_ARMS_max_num]:
            arms[_ARMS_num] = arms[_ARMS_max_num]
