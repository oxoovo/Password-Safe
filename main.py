import sys, random, os, cryptocode, traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

class main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.stack = QStackedWidget()
        self.new = New(self)
        self.lis = List(self)
        self.sett = Settings(self)
        
        #color().change("#00ccff")
        
        self.stack.addWidget(Register(self))
        self.stack.addWidget(self.new)
        self.stack.addWidget(self.lis)
        self.stack.addWidget(PreLoader(self))
        self.stack.addWidget(self.sett)
        
        layout = QGridLayout()
        layout.addWidget(self.stack, 0, 0)
        self.setLayout(layout)
        self.show()
        
        self.preload()
        self.tm = QTimer()
        self.tm.setSingleShot(True)
        self.tm.timeout.connect(self.reg)
        self.tm.start(1000)
        
    def set(self, pswd):
        self.stack.setCurrentIndex(4)
        self.sett.act(pswd)
        
    def preload(self):
        self.stack.setCurrentIndex(3)
        
    def reg(self):
        self.stack.setCurrentIndex(0)
        
    def connc(self, pswd=None):
        self.stack.setCurrentIndex(1)
        if pswd:
            self.new.act(pswd)
        
    def list(self, pswd=None):
        self.stack.setCurrentIndex(2)
        if pswd:
            self.lis.act(pswd)
        
class PreLoader(QWidget):
    def __init__(self, main2, parent=None):
        super().__init__(parent)
        
        self.logo = QSvgWidget("icons/logo.svg")
        self.logo.setFixedSize(1000, 1000)
        self.main = main2
        gr = QGridLayout()
        gr.addWidget(self.logo, 1, 1)
        
        effect = QGraphicsOpacityEffect(self.logo)
        self.logo.setGraphicsEffect(effect)
        self.setLayout(gr)
        
        self.anim_2 = QPropertyAnimation(effect, b"opacity")
        self.anim_2.setStartValue(1)
        self.anim_2.setEndValue(0)
        self.anim_2.setDuration(1000)
        self.anim_2.start()
        
class IcBt(QSvgWidget):
    def __init__(self, to, icon, size=100):
        super().__init__()
        self.clicked=pyqtSignal()
        self.main = main
        
        #self.setIcon("icons/" + icon + ".svg")
        self.setFixedSize(size, size)
        self.to = to
        self.load("icons/" + icon + ".svg")
        
    def mouseReleaseEvent(self, event):
        self.to()
        
        
class List(QWidget):
    def __init__(self, main2, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main2
        
        self.pss = QListWidget()
        self.pss.itemClicked.connect(self.click)
        QScroller.grabGesture(self.pss.viewport(), QScroller.LeftMouseButtonGesture)
        self.pss.setVerticalScrollMode(self.pss.ScrollPerPixel)
        self.pss.setStyleSheet("""QListWidget::item{
                                              background: #5c5c5c;
                                              border-radius: 10px;
                                              margin-left: 10px;
                                              margin-right: 10px;
                                              min-height: 100px;
                                              margin-top: 10px;
                                              }
                                             QListWidget::item:hover{
                                             background: #5c5c5f;
                                             }
                                             """)
        
        self.tx = QTextEdit()
        self.tx.setReadOnly(True)
        
        #self.tx.setMarkdown("# Website\n \n \n \n* username\n\n* password")
        
        self.add = IcBt(self.new, "add")
        #self.add.setIcon(QIcon("icons/add.png"))
        #self.add.setIconSize(QSize(100, 100))
        #self.add.setStyleSheet("border: None;")
        #self.add.clicked.connect(self.new)
        
        self.seti = IcBt(self.set, "settings")
        
        ly.addWidget(self.add, 4, 6, alignment=Qt.AlignCenter)
        ly.addWidget(self.seti, 4, 5, alignment=Qt.AlignCenter)
        ly.addWidget(self.pss, 5, 5)
        ly.addWidget(self.tx, 5, 6)
        
        self.setLayout(ly)
        
    def set(self):
        main.set(self.main, self.p)
        
    def new(self):
        main.connc(self.main, self.p)
        
    def search(self, s):
        with open("psswds.pws", "r") as f:
            inp = f.read()
        content = cryptocode.decrypt(inp, self.p)
        pswds = content.split("%$#@%")
        p = None
        for it in pswds:
            if it.split("%$#@/%")[-1] == s:
                p = it
        return p
        
    def click(self, item):
        self.tx.setMarkdown("# " + str(self.search(item.text()).split("%$#@/%")[-1]) + "\n \n \n \n* username: " + str(self.search(item.text()).split("%$#@/%")[-2]) + "\n\n* password: " + str(self.search(item.text()).split("%$#@/%")[-3]))
        
    def act(self, ps):
        self.p = ps
        self.pss.clear()
        with open("psswds.pws", "r") as f:
            inp = f.read()
        content = cryptocode.decrypt(inp, self.p)
        pswds = content.split("%$#@%")
        for it in pswds:
            if not it.split("%$#@/%")[-1] == "" and not it == "None":
                self.pss.addItem(QListWidgetItem(it.split("%$#@/%")[-1]))
                
class Settings(QWidget):
    def __init__(self, main2, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main2
        
        
        back = IcBt(self.back, "back")
        
        lb = QLabel("Settings")
        lb.setStyleSheet("font-size: 75px; font: bold;")
        
        self.lw = QListWidget()
        QScroller.grabGesture(self.lw.viewport(), QScroller.LeftMouseButtonGesture)
        self.lw.setVerticalScrollMode(self.lw.ScrollPerPixel)
        self.lw.itemClicked.connect(self.click)
        self.lw.setStyleSheet("""QListWidget::item{
                                              background: #5c5c5c;
                                              border-radius: 10px;
                                              margin-left: 10px;
                                              margin-right: 10px;
                                              min-height: 100px;
                                              margin-top: 10px;
                                              padding-left: 10px;
                                              }
                                             QListWidget::item:hover{
                                             background: #5c5c5f;
                                             }
                                             """)
                                             
        self.lw.addItem(QListWidgetItem("color"))
        self.lw.addItem(QListWidgetItem("password"))
        
        
        ly.addWidget(back, 0, 0, alignment=Qt.AlignCenter)
        ly.addWidget(lb, 0, 1)
        ly.addWidget(self.lw, 1, 0, 1, 2)
        
        self.setLayout(ly)
        
    def act(self, ps):
        self.p = ps
        
    def back(self):
        main.list(self.main)
        
    def click(self, item):
        if item.text() == "color":
            col = QColorDialog()
            col.exec()
            self.color = str(col.currentColor().name())
            color().change(self.color)
            MessageDialog("restart", "Please restart Password-Safe to change the color of the buttons.")
        elif item.text() == "password":
            pss, pssok = QInputDialog.getText(self, 'Please enter a new password.', 'Please enter a new password: ')
            if pssok and pss != "":
                MessageDialog("^", pss)
                with open("psswds.pws", "r") as f:
                    inp = f.read()
                content = cryptocode.decrypt(inp, self.p)
                #MessageDialog("j", content)
                nw = cryptocode.encrypt(content, pss)
                #MessageDialog("t", nw)
                with open("psswds.pws", "w") as f:
                    f.write(nw)
                main.list(self.main, pss)
                self.p = pss
                MessageDialog("finish", "your password has been saved.")
        else:
            MessageDialog("error", "error " + item.text() + " couldn't found.")
        
class New(QWidget):
    def __init__(self, main2, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main2
        
        self.p = None
        
        self.psswd = QLineEdit()
        self.psswd.setPlaceholderText("Password")
        self.psswdT = QLabel("Password")
        self.psswdT.setAlignment(Qt.AlignCenter)
        
        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")
        self.userT = QLabel("Username")
        self.userT.setAlignment(Qt.AlignCenter)
        
        self.web = QLineEdit()
        self.web.setPlaceholderText("Website/App")
        self.webT = QLabel("Website/App")
        self.webT.setAlignment(Qt.AlignCenter)
        
        back = IcBt(self.back, "back")
        
        self.finish = IcBt(self.save, "save")
        
        gene =  IcBt(self.generate, "password", 75)
        
        wg = QGroupBox()
        wl = QVBoxLayout()
        wl.addWidget(self.webT)
        wl.addWidget(self.web)
        wg.setLayout(wl)
        
        bg = QGroupBox()
        bl = QVBoxLayout()
        bl.addWidget(back, alignment=Qt.AlignCenter)
        bl.addWidget(self.finish, alignment=Qt.AlignCenter)
        bg.setLayout(bl)
        
        ug = QGroupBox()
        ul = QVBoxLayout()
        ul.addWidget(self.userT)
        ul.addWidget(self.user)
        ug.setLayout(ul)
        
        pg = QGroupBox()
        pl = QGridLayout()
        pl.addWidget(self.psswdT, 1, 1, 1, 2)
        pl.addWidget(self.psswd, 2, 1)
        pl.addWidget(gene, 2, 2)
        pg.setLayout(pl)
        
        
        ly.addWidget(wg, 5, 1)
        ly.addWidget(ug, 6, 0)
        ly.addWidget(pg, 6, 1)
        ly.addWidget(bg, 5, 0)
        
        self.setLayout(ly)
        
    def generate(self):
        self.psswd.setText(str(PasswordDialog().pss))
        
    def back(self):
        main.list(self.main)
        
    def save(self):
        if not "%$#@%" in self.psswd.text() and not "%$#@%" in self.user.text() and not "%$#@%" in self.web.text() and not "%$#@/%" in self.psswd.text() and not "%$#@/%" in self.user.text() and not "%$#@/%" in self.web.text():
            print("%$#@%" + self.psswd.text() + "%$#@/%" + self.user.text() + "%$#@/%" + self.web.text())
            with open("psswds.pws", "r") as f:
                inp = f.read()
            content = cryptocode.decrypt(inp, self.p)
            if content == "None":
                with open("psswds.pws", "w") as f:
                    f.write(cryptocode.encrypt("%$#@%" + self.psswd.text() + "%$#@/%" + self.user.text() + "%$#@/%" + self.web.text(), self.p))
            else:
                f = open("psswds.pws", "w")
                f.write(cryptocode.encrypt(content + "%$#@%" + self.psswd.text() + "%$#@/%" + self.user.text() + "%$#@/%" + self.web.text(), self.p))
                print(cryptocode.encrypt("%$#@%" + self.psswd.text() + "%$#@/%" + self.user.text() + "%$#@/%" + self.web.text(), self.p))
                f.close()
            MessageDialog("Finished", "Your password has been saved.")
            self.psswd.setText("")
            self.user.setText("")
            self.web.setText("")
            main.list(self.main, self.p)
        else:
            MessageDialog("Error", "The password, username or website cannot contain %$#@% or %$#@/%.")
        
    def act(self, ps):
        self.p = ps
        
class MessageDialog(QDialog):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        message.setWordWrap(True)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.setStyleSheet("QDialog{ border: 4px solid " + color().color + "; border-radius: 20px; }")
        self.exec()
        
class PasswordDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate password")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.click)
        self.layout = QVBoxLayout()
        
        self.cb1 = QCheckBox()
        self.cb1.setText("uppercase letters")
        self.cb1.setChecked(True)
        
        self.cb2 = QCheckBox()
        self.cb2.setText("lowercase letters")
        self.cb2.setChecked(True)
        
        self.cb3 = QCheckBox()
        self.cb3.setText("numbers")
        self.cb3.setChecked(True)
        
        self.cb4 = QCheckBox()
        self.cb4.setText("special characters")
        self.cb4.setChecked(True)
        
        self.spin = QSpinBox()
        #self.spin.setRange(5, 20)
        self.spin.setValue(8)
        
        self.layout.addWidget(self.cb1)
        self.layout.addWidget(self.cb2)
        self.layout.addWidget(self.cb3)
        self.layout.addWidget(self.cb4)
        self.layout.addWidget(self.spin)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.setStyleSheet("QDialog{ border: 4px solid " + color().color + "; border-radius: 20px; }")
        self.exec()
        
    def click(self):
        chr = ""
        if self.cb1.isChecked():
            chr += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if self.cb2.isChecked():
            chr += "abcdefghijklmnopqrstuvwxyz"
        if self.cb3.isChecked():
            chr += "1234567890"
        if self.cb4.isChecked():
            chr += "!*#,;?+-_.=~^%(){}[]|:/"
        if chr != "":
            self.pss = "".join(random.choices(chr,k=int(self.spin.text())))
            #MessageDialog(self.pss, self.pss)
            self.accept()
        else:
            MessageDialog("ERROR", "You didn't select anything!")
            

        
class Register(QWidget):
    def __init__(self, main2, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main2
        
        if os.path.exists("psswds.pws"):
            lab = QLabel("Please enter your password. The password is required to encrypt your saved passwords. It will not be saved.")
        else:
            lab = QLabel("Please choose a Password. The password is required to encrypt your saved passwords. It will not be saved.")
        lab.setAlignment(Qt.AlignCenter)
        lab.setWordWrap(True)
        self.us = QLineEdit()
        self.us.setEchoMode(QLineEdit.Password)
        self.us.setPlaceholderText("Password")
        fertig = QPushButton("finish")
        fertig.setStyleSheet("border: 10px solid " + color().color + "; border-radius: 50px;")
        fertig.setFixedHeight(100)
        fertig.clicked.connect(self.regg)
        
        ly.addWidget(fertig, 3, 1)
        ly.addWidget(self.us, 2, 1)
        ly.addWidget(lab, 1, 1)
        
        self.setLayout(ly)
        
    def regg(self):
        print(self.us.text())
        if not os.path.exists("psswds.pws"):
            if self.us.text() != "":
                with open("psswds.pws", "w") as f:
                    f.write(cryptocode.encrypt("None", self.us.text()))
                main.list(self.main, self.us.text())
            else:
                MessageDialog("error", "please  enter a password")
        else:
            with open("psswds.pws", "r") as f:
                inp = f.read()
            if cryptocode.decrypt(inp, self.us.text()):
                main.list(self.main, self.us.text())
            else:
                MessageDialog("Wrong password!", "Wrong password!")
                
class color():
    def __init__(self):
        super().__init__()
        
        try:
            file = open("color.pws", "r")
            self.color = file.read()
            file.close()
        except:
            file = open("color.pws", "a")
            self.color = "#00ccff"
            file.write(self.color)
            file.close()
            
        self.icons = ["add", "back", "color", "password", "save", "settings"]
        
    def change(self, col):
        with open("color.pws", "r") as f:
            oldcol = f.read()
        try:
            os.remove("color.pws")
        except:
            pass
        file = open("color.pws", "a")
        self.color = col
        file.write(self.color)
        file.close()
        
        for icon in self.icons:
            ic = "icons/" + icon + ".svg"
            with open(ic, "r") as f:
                data = f.read()
            with open(ic, "w") as f:
                f.write(data.replace(oldcol, self.color))


def exception_hook(exctype, value, tracebac):
    print(exctype, value, tracebac)
    #sys.__excepthook__(exctype, value, tracebac)
    e1 = traceback.format_exception(exctype, value, tracebac)
    e2 = ""
    for it in e1:
        e2 += it
    MessageDialog("ERROR", "ERROR:\n\n" + e2)
	
sys.excepthook = exception_hook

app = QApplication(sys.argv)

app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)

window = main()
window.show()
app.exec_()