from display import display

@micropython.viper
def BACK():
    return bytearray([2, 0])
_BACK_color = const(0)
_BACK_bkType = const(1)

class Back:
    def __init__(self):
        self.gBack = BACK()
    
    @micropython.viper
    def InitBack(self, fName, bkType: int) -> bool:
        color = 0
        if fName == "bkBlue":
            color = 2
        gBack = ptr8(self.gBack)
        gBack[_BACK_color] = color
        gBack[_BACK_bkType] = bkType
        return True
        
    @micropython.viper
    def PutBack(self):
        display.fill(self.gBack[_BACK_color])
