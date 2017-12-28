# Eric Pai
# Started: Spring 2014

from tetris.gui import Main

m = Main()

try:
    m.doWelcome()
    m.gameLoop()
except (ZeroDivisionError, KeyboardInterrupt) as e:
    pass
except Exception as e:
    raise e
finally:
    m.doFinish()