#!/usr/bin/env python


# ----------------------------
__author__ = "Bruno Viola"
__Name__ = "HRTS RO tool GUI"
__version__ = "1"
__release__ = "0"
__maintainer__ = "Bruno Viola"
__email__ = "bruno.viola@ukaea.uk"
__status__ = "Testing"
#__status__ = "Production"



from PyQt4 import QtGui
from pathlib import Path
import os
import reqco_window_gui
from areyousure_gui import Ui_areyousure_window
import argparse
import json
from collections import OrderedDict
import logging
from PyQt4 import QtCore, QtGui
import pathlib
from logging.handlers import RotatingFileHandler
from logging import handlers
import sys
import pdb
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#sys.path.append('../')
#from status_flags.status_flag import GetSF

from test_reqco_ver01 import *

from numpy import arange,asscalar
import matplotlib.pyplot as plt
plt.rcParams["savefig.directory"] = os.chdir(os.getcwd())
myself = lambda: inspect.stack()[1][3]
logger = logging.getLogger(__name__)


class HRTSRO_tool(QtGui.QMainWindow, reqco_window_gui.Ui_reqco_window):

    def __init__(self, parent=None):
        """
        Setup the GUI, and connect the buttons to functions.
        """
        import os
        super(HRTSRO_tool, self).__init__(parent)
        self.setupUi(self)
        logging.debug('start')

        cwd = os.getcwd()
        self.home = cwd
        if "USR" in os.environ:
            logger.debug('USR in env')
            # self.owner = os.getenv('USR')
            self.owner = os.getlogin()
        else:
            logger.debug('using getuser to authenticate')
            import getpass
            self.owner = getpass.getuser()

        logger.debug('this is your username {}'.format(self.owner))
        homefold = os.path.join(os.sep, 'u', self.owner)
        logger.debug('this is your homefold {}'.format(homefold))
        home = str(Path.home())

        cwd = os.getcwd()
        self.home = cwd

        logger.debug('we are in %s', cwd)


        with open('./user_installation_data.json', mode='r', encoding='utf-8') as f:
            # Remove comments from input json
            with open("temp.json", 'w') as wf:
                for line in f.readlines():
                    if line[0:2] == '//' or line[0:1] == '#':
                        continue
                    wf.write(line)

        with open("temp.json", 'r') as f:
            self.input_dict = json.load(f, object_pairs_hook=OrderedDict)
            os.remove('temp.json')


        folder=self.input_dict['install_folder']
        self.basefolder = self.input_dict['base_folder']
        self.installationfolder= folder



        initpulse = pdmsht()
        self.lineEdit_pulse.setText(str(initpulse))


        self.done_button.setChecked(False)
        self.impossible_button.setChecked(False)
        self.closed_button.setChecked(False)

        self.done_button.clicked.connect(self.mark_pulse_done)
        self.impossible_button.clicked.connect(
            self.mark_pulse_impossible)
        self.closed_button.clicked.connect(self.mark_pulse_closed)
        # self/home/.done_button.clicked.connect(lambda:self.handle_areyousure(self.ui_reqco.done_button))
        # self.ui_reqco.impossible_button.clicked.connect(lambda:self.handle_areyousure(self.ui_reqco.impossible_button))

        self.run_button.clicked.connect(self.scan_reqco_database)
        self.run_button_2.clicked.connect(self.download_reqco_database)

        self.done_button.setToolTip(
            'marks Reqco request for selected pulse as DONE')
        self.impossible_button.setToolTip(
            'marks Reqco request for selected pulse as IMPOSSIBLE')
        self.closed_button.setToolTip(
            'marks Reqco request for selected pulse as CLOSED')
        self.lineEdit_pulse.setToolTip(
            'insert JPN for handling single pulse request')


    def mark_pulse_done(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as done in  Reqco database
        """

        button = self.done_button
        self.done_button.setChecked(True)
        logger.debug('pressed button %s', button.text())
        logger.info('are you sure?')
        logger.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)

    # ----------------------------
    def mark_pulse_impossible(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as impossible in  Reqco database
        """

        button = self.impossible_button
        self.impossible_button.setChecked(True)
        logger.debug('pressed button %s', button.text())
        logger.info('are you sure?')
        logger.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)
        #

    # ----------------------------
    def mark_pulse_closed(self):
        """
        function that manages event
        if user wants to mark request for selected pulse
        as closed in  Reqco database

        Essentially "closed" means it's not done, but for non-physics reasons.
        """

        button = self.closed_button
        self.closed_button.setChecked(True)
        logger.debug('pressed button %s', button.text())
        logger.info('are you sure?')
        logger.info('waiting for user to click button')

        self.areyousure_window = QtGui.QMainWindow()
        self.ui_areyousure = Ui_areyousure_window()
        self.ui_areyousure.setupUi(self.areyousure_window)
        self.areyousure_window.show()

        self.ui_areyousure.pushButton_YES.clicked.connect(self.handle_yes)
        self.ui_areyousure.pushButton_NO.clicked.connect(self.handle_no)
        #

    # ----------------------------
    def download_reqco_database(self):
        """
        scan Reqco database for selected process to see if there is any pulse that
        can be marked as done/impossible, i.e. if there is a pulse already validated for that process


        """
        import os
        import stat
        process = 'hrts'
        logger.info('\n')
        logger.info('scanning database for process %s', process)

        writing_requests_pulse_list(process,'/'+self.basefolder+'/'+self.owner+ '/'+self.installationfolder+'/hrts_tools_logbook/')

        logger.info('file(s) written to {}'.format('/'+self.basefolder+'/'+self.owner+ '/'+self.installationfolder+'/hrts_tools_logbook/'))


    # ----------------------------
    def scan_reqco_database(self):
        """
        scan Reqco database for selected process to see if there is any pulse that
        can be marked as done/impossible, i.e. if there is a pulse already validated for that process


        """
        import os
        import stat
        process = 'hrts'
        logger.info('\n')
        logger.info('scanning database for process %s', process)
        cwd = os.getcwd()
        run_reqco = './test_reqco_ver01.py'
        #run_reqco = './test_reqco_ver01.py'
        st = os.stat(run_reqco)
        os.chmod(run_reqco, st.st_mode | stat.S_IEXEC)

        os.system("{} {} ".format(run_reqco, process))


    # ----------------------------
    def handle_yes(self):
        """
        functions that ask to confirm if user wants to proceed

        to set request for selected pulse as done/impossible/closed
        """
        logger.debug("pressed %s button", self.ui_areyousure.pushButton_YES.text())
        if self.done_button.isChecked() == True:
            logger.debug("continue")
            self.set_pulse_done()
            self.done_button.setChecked(False)

        if self.impossible_button.isChecked() == True:
            logger.debug("continue")
            self.set_pulse_impossible()
            self.impossible_button.setChecked(False)

        if self.closed_button.isChecked() == True:
            logger.debug("continue")
            self.set_pulse_closed()
            self.closed_button.setChecked(False)

        self.ui_areyousure.pushButton_YES.setChecked(False)

        self.areyousure_window.hide()

    # ----------------------------
    def set_pulse_closed(self):
        """
        request for
        (pulse/process) marked as closed
        """

        process = "hrts"
        pulse = int(self.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logger.error(
                "the selected combination of process %s and pulse %s is not in Reqco database",
                process.upper(),
                str(pulse),
            )
        else:

            for req in reqs:
                id = req["id"]
                logger.info("marking JPN %s as closed", str(pulse))

                ppf = "HRTS"

                if yes_or_no("set message to requester? Y/N"):
                    sms = input()
                else:
                    sms = None
                try:
                    r = set_request_closed(id, ppf, message=sms)
                except:
                    logger.error("error! check error message")

                #
                if r.status_code != 200:
                    logger.error("Server returned error:")
                    logger.error("%s", str(r.text))
                else:
                    logger.info(
                        "JPN %s marked as closed", str(pulse)
                    )  # ----------------------------

    def set_pulse_done(self):
        """
        request for
        (pulse/process) marked as done
        """


        process = "hrts"
        pulse = int(self.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logger.error(
                "the selected combination of process %s and pulse %s is not in Reqco database",
                process.upper(),
                str(pulse),
            )
        else:

            for req in reqs:
                id = req["id"]
                logger.info("marking JPN %s as done", str(pulse))

                ppf = "HRTS"

                if yes_or_no("set message to requester? Y/N"):
                    sms = input()
                else:
                    sms = None
                try:
                    r = set_request_done(id, ppf, message=sms)
                except:
                    logger.error("error! check error message")

                #
                if r.status_code != 200:
                    logger.error("Server returned error:")
                    logger.error("%s", str(r.text))
                else:
                    logger.info("JPN %s marked as done", str(pulse))

    # ----------------------------
    def set_pulse_impossible(self):
        """
    request for
    (pulse/process) marked as impossible
    """


        process = "hrts"
        pulse = int(self.lineEdit_pulse.text())

        reqs = waiting_requests_for_pulse(process, str(pulse))
        if not reqs:
            logger.error(
                "the selected combination of process %s and pulse %s is not in Reqco database",
                process.upper(),
                str(pulse),
            )
        else:

            for req in reqs:
                id = req["id"]
                logger.info("marking JPN %s as impossible", str(pulse))

                if yes_or_no("set message to requester? Y/N"):
                    sms = input()
                else:
                    sms = None
                try:
                    r = set_request_impossible(id, message=sms)
                except:
                    logger.error("error! check error message")

                # r = set_request_impossible(id, ppf)
                #
                if r.status_code != 200:
                    logger.error("Server returned error:")
                    logger.error("%s", str(r.text))
                else:
                    logger.info("JPN %s marked as impossible", str(pulse))

    # ----------------------------
    def handle_no(self):
        """
    functions that ask to confirm if user wants NOT to proceed

    to set request for selected pulse as done/impossible/closed
    """

        logger.debug("pressed %s button", self.ui_areyousure.pushButton_NO.text())
        if self.done_button.isChecked() == True:
            self.done_button.setChecked(False)
            logger.debug("go back")

        if self.impossible_button.isChecked() == True:
            self.impossible_button.setChecked(False)
            logger.debug("go back")

        self.ui_areyousure.pushButton_NO.setChecked(False)
        self.impossible_button.setChecked(False)
        self.areyousure_window.hide()

def main():
    """
    Main function

    the only input to the GUI is the debug

    by default is set to INFO
    """
    logger.info("Running HRTS tool.")

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
    pathlib.Path(cwd + os.sep + 'hrts_tools_logbook').mkdir(parents=True,exist_ok=True)
    fh = handlers.RotatingFileHandler('./hrts_tools_logbook/LOGFILE.DAT', maxBytes=(1048576*5), backupCount=7)
    fh.setFormatter(fmt)
    logging.root.addHandler(fh)

    logging.root.setLevel(level=debug_map[args.debug])


    main()
