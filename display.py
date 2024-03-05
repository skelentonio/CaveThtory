from machine import Pin, SPI, mem32
from utime import sleep_ms, ticks_diff, ticks_ms
from os import stat

emulator = None
try:
    import emulator
    import ssd1306 # no idea why, but emulator needs this
except ImportError:
    pass

_FPS = const(50)
_FPS_TIME = const(1000 // _FPS)
_WIDTH = const(72)
_HEIGHT = const(40)
_BUFF_SIZE = const((_HEIGHT // 8) * _WIDTH) # 360

# Push the buffer to the hardware display.
class GraphicsClass():
    def __init__(self):
        self._spi = SPI(0, sck=Pin(18), mosi=Pin(19))
        self._dc = Pin(17)
        self._cs = Pin(16)
        self._res = Pin(20)
        self.drawBuffer = bytearray(_BUFF_SIZE)
        self.buffer = memoryview(self.drawBuffer)
        self.lastUpdateEnd = 0
        self.textBitmapSource = None
        
    @micropython.native
    def setFont(self, fontFile, width, height, space):
        if self.textBitmapSource == fontFile:
            return
        self.textBitmapSource = fontFile
        self.textBitmapFile = open(fontFile, 'rb')
        self.textWidth = width
        self.textHeight = height
        self.textSpaceWidth = space
        self.textBitmap = bytearray(self.textWidth)
        self.textCharCount = stat(fontFile)[6] // self.textWidth

    @micropython.viper
    def update(self):
        if emulator:
            mem32[0xD0000000+0x01C] = 1 << 2
        else:
            self._dc(1)
            self._spi.write(self.buffer)
    
        lastUpdateEnd = self.lastUpdateEnd
        frameTimeRemaining = _FPS_TIME - int(ticks_diff(ticks_ms(), lastUpdateEnd))
        while(frameTimeRemaining>1):
            sleep_ms(1)
            frameTimeRemaining = _FPS_TIME - int(ticks_diff(ticks_ms(), lastUpdateEnd))
        while(frameTimeRemaining>0):
            frameTimeRemaining = _FPS_TIME - int(ticks_diff(ticks_ms(), lastUpdateEnd))
        self.lastUpdateEnd=ticks_ms()

    @micropython.viper
    def fill(self, color:int):
        buf = ptr8(self.buffer)
        if color==0: # black
            for i in range(_BUFF_SIZE):
                buf[i]=0
        elif color==1: # white
            for i in range(_BUFF_SIZE):
                buf[i]=0xff
        elif color==2: # checkers
            b=0xaa
            for i in range(_BUFF_SIZE):
                buf[i]=b
                b^=0xff
        elif color==3: # horizontal stripes
            for i in range(_BUFF_SIZE):
                buf[i]=0xaa
        elif color==4: # vertical stripes
            b=0xff
            for i in range(_BUFF_SIZE):
                buf[i]=b
                b^=0xff
                
    # Draw a string with top left corner (x, y) in a given color.
    @micropython.viper
    def drawText(self, stringToPrint:ptr8, x:int, y:int, color:int):
        xPos=x
        charNum=0
        charBitMap=0
        ptr = ptr8(self.buffer)
        sprtptr = ptr8(self.textBitmap)
        textHeight=int(self.textHeight)
        textWidth=int(self.textWidth)
        maxChar=int(self.textCharCount)
        textSpaceWidth=int(self.textSpaceWidth)
        while(stringToPrint[charNum]):
            charBitMap=int(stringToPrint[charNum] - 0x20)
            if 0 <= charBitMap <= maxChar:
                if xPos+textWidth>0 and xPos<_WIDTH and y+textHeight>0 and y<_HEIGHT:
                    self.textBitmapFile.seek(textWidth*charBitMap)
                    self.textBitmapFile.readinto(self.textBitmap)
                    xStart=xPos
                    yStart=y
                    blitHeight=textHeight
                    yFirst=0-yStart
                    if yFirst<0:
                        yFirst=0
                    if yStart+textHeight>40:
                        blitHeight = 40-yStart
                    yb=yFirst
                    xFirst=0-xStart
                    blitWidth=textWidth
                    if xFirst<0:
                        xFirst=0
                    if xStart+textWidth>72:
                        blitWidth = 72-xStart
                    if(color==0):
                        while yb < blitHeight:
                            x=xFirst
                            while x < blitWidth:
                                if(sprtptr[(yb >> 3) * textWidth + x] & (1 << (yb & 0x07))):
                                    ptr[((yStart+yb) >> 3) * _WIDTH + xStart+x] &= 0xff ^ (1 << (yStart+yb & 0x07))
                                x+=1
                            yb+=1
                    else:
                        while yb < blitHeight:
                            x=xFirst
                            while x < blitWidth:
                                if(sprtptr[(yb >> 3) * textWidth + x] & (1 << (yb & 0x07))):
                                    ptr[((yStart+yb) >> 3) * _WIDTH + xStart+x] |= 1 << ((yStart+yb) & 0x07)
                                x+=1
                            yb+=1
            charNum+=1
            xPos+=(textWidth+textSpaceWidth)
            
    @micropython.viper
    def middleText(self, stringToPrint: object, color: int):
        linewidth = (int(self.textWidth) + int(self.textSpaceWidth)) * int(len(stringToPrint))
        self.drawText(stringToPrint, (_WIDTH // 2) - (linewidth // 2), (_HEIGHT // 2) - (int(self.textHeight) // 2), color)
            
    @micropython.viper
    def blit(self, sprtptr:ptr8, x:int, y:int, width:int, height:int):
        if x+width<0 or x>=_WIDTH:
            return
        if y+height<0 or y>=_HEIGHT:
            return
        xStart=x
        yStart=y
        ptr = ptr8(self.buffer)
        
        yFirst=0-yStart
        blitHeight=height
        if yFirst<0:
            yFirst=0
        if yStart+height>40:
            blitHeight = 40-yStart
        
        xFirst=0-xStart
        blitWidth=width
        if xFirst<0:
            xFirst=0
        if xStart+width>72:
            blitWidth = 72-xStart
        
        y=yFirst
        while y < blitHeight:
            x=xFirst
            a=(y >> 3) * width
            b=a+x
            c=1 << (y & 0x07)
            d=yStart+y
            e=(d >> 3) * 72
            f=1 << (d & 0x07)
            while x < blitWidth:
                if(sprtptr[b] & c):
                    ptr[e+xStart+x] |= f
                else:
                    ptr[e+xStart+x] &= 0xff ^ f
                x+=1
                b+=1
            y+=1
            
    @micropython.viper
    def blitWithMask(self, sprtptr:ptr8, x:int, y:int, width:int, height:int, maskptr:ptr8):
        if x+width<0 or x>=_WIDTH:
            return
        if y+height<0 or y>=_HEIGHT:
            return
        xStart=x
        yStart=y
        ptr = ptr8(self.buffer)
        
        yFirst=0-yStart
        blitHeight=height
        if yFirst<0:
            yFirst=0
        if yStart+height>40:
            blitHeight = 40-yStart
        
        xFirst=0-xStart
        blitWidth=width
        if xFirst<0:
            xFirst=0
        if xStart+width>72:
            blitWidth = 72-xStart
            
        y=yFirst
        while y < blitHeight:
            x=xFirst
            a=(y >> 3) * width
            b=a+x
            c=1 << (y & 0x07)
            d=yStart+y
            e=(d >> 3) * 72
            f=1 << (d & 0x07)
            while x < blitWidth:
                if(maskptr[b] & c):
                    if(sprtptr[b] & c):
                        ptr[e+xStart+x] |= f
                    else:
                        ptr[e+xStart+x] &= 0xff ^ f
                x+=1
                b+=1
            y+=1
            
display = GraphicsClass()
display_update = display.update

class _GraphicsLauncher():
    def __init__(self):
        display._spi.init(baudrate=10 * 1024 * 1024, polarity=0, phase=0)
        display._res.init(Pin.OUT, value=1)
        display._dc.init(Pin.OUT, value=0)
        display._cs.init(Pin.OUT, value=1)
        display._cs(0)
        display.fill(0)
        display.setFont('lib/font5x7.bin', 5, 7, 1)
        if (emulator):
            self.init_emu_screen()
            mem32[0xD0000000+0x01C] = 1 << 2

    @micropython.viper
    def init_emu_screen(self):
        emulator.screen_breakpoint(ptr8(display.drawBuffer))
    
_GraphicsLauncher()
del _GraphicsLauncher