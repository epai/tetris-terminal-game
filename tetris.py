# Eric Pai
# Spring 2014
"""
INSRT TETRIS LOGO HERE


INSERT CREDITS HERE
"""

from __Main__ import *

#### TO DO LIST ####
# ---Game Mechanics---
# - wall kicking XX
# - line completion (sort of)
# - "levels" and associated falling speeds (YES!)
# - score (sort of)
# - "next piece" box (YES!)
# - "retry" option, after losing (YES!)
# - ghosting
# ---Extras/Aesthetics---
# - home page (YES!)
# - "lose" mechanism (YES!)
# - "quit" mechanism" (YES!)
# - "clear line" animations (Maybe later...)
# - adjust layout/make more clean (YES!)
# - add "juciness" (nope)
# - make screen adjustable? (nope)
# - high score system
# ---Other---
# - get tested and advice from other people
# - show andrew as a going-away present!
####################

###### Special Thanks #######
# - carlos caballero
# - jordon wing

m = Main()

try:
    m.doWelcome()
    m.gameLoop()
except ZeroDivisionError as e:
    pass
except KeyboardInterrupt as e:
    pass
except Exception as e:
    raise e
finally:
    m.doFinish()