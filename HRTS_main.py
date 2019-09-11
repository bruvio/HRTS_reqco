#!/usr/bin/env python


# ----------------------------
__author__ = "Bruno Viola"
__Name__ = "HRTS RO tool GUI"
__version__ = "0"
__release__ = "2"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
#__status__ = "Production"



from PyQt4 import QtGui
from pathlib import Path
import os
from reqco_window_gui import Ui_reqco_window
from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *
#sys.path.append('../')
#from status_flags.status_flag import GetSF

from test_reqco_ver01 import *

from numpy import arange,asscalar
import matplotlib.pyplot as plt
plt.rcParams["savefig.directory"] = os.chdir(os.getcwd())



class HRTSRO_tool(QtGui.QMainWindow, reqco_window_gui.Ui_reqco_window):

    def __init__(self, parent=None):
        """
        Setup the GUI, and connect the buttons to functions.
        """
        import os
        super(KG1RO_tool, self).__init__(parent)
        self.setupUi(self)
        logging.debug('start')

        cwd = os.getcwd()
        self.home = cwd
        if "USR" in os.environ:
            logging.debug('USR in env')
            # self.owner = os.getenv('USR')
            self.owner = os.getlogin()
        else:
            logging.debug('using getuser to authenticate')
            import getpass
            self.owner = getpass.getuser()

        logging.debug('this is your username {}'.format(self.owner))
        homefold = os.path.join(os.sep, 'u', self.owner)
        logging.debug('this is your homefold {}'.format(homefold))
        home = str(Path.home())

        cwd = os.getcwd()
        self.home = cwd

        logging.debug('we are in %s', cwd)




def main():
    """
    Main function

    the only input to the GUI is the debug

    by default is set to INFO
    """
    logger.info("Running KG1 tool.")

    app = QtGui.QApplication(argv)
    MainWindow = HRTSRO_tool()
    MainWindow.show()
    app.exec_()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run GO_HRTS_tools')
    parser.add_argument("-d", "--debug", type=int,
                        help="Debug level. 0: Info, 1: Warning, 2: Debug,"
                            " 3: Error; \n default level is INFO", default=0)
    parser.add_argument("-doc", "--documentation", type=str,
                        help="Make documentation. yes/no", default='no')




    args = parser.parse_args(sys.argv[1:])
    debug_map = {0: logging.INFO,
                1: logging.WARNING,
                2: logging.DEBUG,
                3: logging.ERROR}

    logger = logging.getLogger(__name__)
    fmt = MyFormatter()
    hdlr = logging.StreamHandler(sys.stdout)

    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)
    cwd = os.getcwd()
    pathlib.Path(cwd + os.sep + 'kg1_tools_logbook').mkdir(parents=True,exist_ok=True)
    fh = handlers.RotatingFileHandler('./kg1_tools_logbook/LOGFILE.DAT', maxBytes=(1048576*5), backupCount=7)
    fh.setFormatter(fmt)
    logging.root.addHandler(fh)

    logging.root.setLevel(level=debug_map[args.debug])


    main()