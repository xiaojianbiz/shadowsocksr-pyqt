import sys
import time
import subprocess

from PyQt4 import QtCore, QtGui, uic
from shadowsocks import shell
Ui_MainWindow, QtBaseClass = uic.loadUiType("gui/gui.ui")

ssr_main = subprocess.Popen(["python", "ssr.py", "-v"],stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

class server():
    def __init__(self, ip , port, enable):
        self.ip = ip
        self.port = port
        self.enable = QtGui.QCheckBox()
        self.enable.setChecked(enable)

class Main(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.server_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.server_table.setColumnWidth(0, 210)
        self.server_table.setColumnWidth(1, 30)
        self.show_servers()
        self.button_connect.clicked.connect(run)
        self.button_disconnect.clicked.connect(stop)
        ssr_log.log.connect(self.ssrlog)


    def show_servers(self):
        global config
        servers = config._config['configs']
        i = 0
        for x in servers:
            self.server_table.insertRow(i)
            servertmp = server(x['server'], x['server_port'], x['enable'])
            serveritem = QtGui.QTableWidgetItem(str(servertmp.ip)+":"+str(servertmp.port))
            self.server_table.setItem(i, 0, serveritem)
            self.server_table.setCellWidget(i, 1, servertmp.enable)
            i += 1

    def closeEvent(self,event):
        global ssr_main
        global ssr_log
        ssr_main.kill()
        ssr_log.exit(0)


    def close(self):
        global ssr_main
        global ssr_log
        ssr_main.kill()
        ssr_log.exit(0)

    def ssrlog(self, string):
        self.ssr_log.append(string)


class SSRLog(QtCore.QThread):

    log = QtCore.pyqtSignal(str)

    def __int__(self):
        super(SSRLog,self).__init__()

    def run(self):
        global ssr_main
        if ssr_main is None:
            return
        returncode = ssr_main.poll()
        while returncode is None:
            if ssr_main is None:
                return
            else:
                line = ssr_main.stdout.readline()
                returncode = ssr_main.poll()
                self.log.emit(str(line))
        self.log.emit(str("Stop ...."))


class cfgjson():

    _config = shell.get_config(True)

    def __int__(self):
        self._config = shell.get_config(True)

    def printcfg(self):
        print(str(self._config))



def stop():
    global ssr_main
    global ssr_log
    ssr_log.exit(0)
    ssr_main.kill()


def run():
    global ssr_main
    global ssr_log
    ssr_log.exit(0)
    ssr_main.kill()
    ssr_main = subprocess.Popen(["python", "ssr.py", "-v"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    ssr_log.start()


ssr_log = SSRLog()
config = cfgjson()

if __name__ == '__main__':
    ssr_log.start()
    app = QtGui.QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    sys.exit(app.exec_())
