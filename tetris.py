from tetris.gui import UI

m = UI()

try:
    m.doWelcome()
    m.gameLoop()
except (ZeroDivisionError, KeyboardInterrupt) as e:
    pass
except Exception as e:
    raise e
finally:
    m.doFinish()