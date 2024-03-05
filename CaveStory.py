# Cave Story Thumby port by SKELUX
# based off CSE2EX

from machine import freq
freq(250000000)

from sys import path
path.append("/Games/CaveStory")

# Draw loading screen
from display import display
display.middleText("Loading", 1)
display.update()

import Game