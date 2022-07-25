import sys, random, os, cryptocode
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSvg import *

USER_ME = 0
USER_THEM = 1
USER_BOT = 2

BUBBLE_COLORS = {USER_ME: "#3DD9F5", USER_THEM: "#66FF66", USER_BOT: "#ff0000"}

BUBBLE_PADDING = QMargins(15, 5, 15, 5)
TEXT_PADDING = QMargins(25, 15, 25, 15)

class main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.stack = QStackedWidget()
        self.new = New(self)
        self.lis = List(self)
        
        self.stack.addWidget(Register(self))
        self.stack.addWidget(self.new)
        self.stack.addWidget(self.lis)
        self.stack.addWidget(PreLoader(self))
        
        layout = QGridLayout()
        layout.addWidget(self.stack, 0, 0)
        self.setLayout(layout)
        self.show()
        
        self.preload()
        self.tm = QTimer()
        self.tm.setSingleShot(True)
        self.tm.timeout.connect(self.reg)
        self.tm.start(2000)
        
    def preload(self):
        self.stack.setCurrentIndex(3)
        
    def reg(self):
        self.stack.setCurrentIndex(0)
        
    def connc(self, pswd):
        self.stack.setCurrentIndex(1)
        self.new.act(pswd)
        
    def list(self, pswd):
        self.stack.setCurrentIndex(2)
        self.lis.act(pswd)
        
class PreLoader(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        logo = QSvgWidget("icons/logo.svg")
        logo.setFixedSize(1000, 1000)
        self.main = main
        gr = QGridLayout()
        gr.addWidget(logo, 1, 1)
        
        rnd = random.randint(0, 10)
        if rnd == 5:
            RickDialog()
        
        effect = QGraphicsOpacityEffect(logo)
        logo.setGraphicsEffect(effect)
        self.setLayout(gr)
        self.anim_2 = QPropertyAnimation(effect, b"opacity")
        self.anim_2.setStartValue(1)
        self.anim_2.setEndValue(0)
        self.anim_2.setDuration(2000)
        self.anim_2.start()
        
        
class List(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        self.pss = QListWidget()
        self.pss.itemClicked.connect(self.click)
        self.pss.setStyleSheet("""QListWidget::item{
                                              background: #5c5c5c;
                                              border-radius: 10px;
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
        
        self.add = QPushButton("\n\n")
        self.add.setIcon(QIcon("icons/add.png"))
        self.add.setIconSize(QSize(100, 100))
        self.add.setStyleSheet("border: None;")
        self.add.clicked.connect(self.new)
        
        ly.addWidget(self.add, 4, 6)
        ly.addWidget(self.pss, 5, 5)
        ly.addWidget(self.tx, 5, 6)
        
        self.setLayout(ly)
        
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
        
class New(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
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
        
        back = QPushButton("\n\n")
        back.clicked.connect(self.back)
        back.setIcon(QIcon("icons/back.png"))
        back.setIconSize(QSize(100, 100))
        back.setStyleSheet("border: None;")
        
        self.finish = QPushButton("\n\n")
        self.finish.setIcon(QIcon("icons/save.png"))
        self.finish.setIconSize(QSize(100, 100))
        self.finish.setStyleSheet("border: None;")
        self.finish.clicked.connect(self.save)
        
        wg = QGroupBox()
        wl = QVBoxLayout()
        wl.addWidget(self.webT)
        wl.addWidget(self.web)
        wg.setLayout(wl)
        
        bg = QGroupBox()
        bl = QVBoxLayout()
        bl.addWidget(back)
        bl.addWidget(self.finish)
        bg.setLayout(bl)
        
        ug = QGroupBox()
        ul = QVBoxLayout()
        ul.addWidget(self.userT)
        ul.addWidget(self.user)
        ug.setLayout(ul)
        
        pg = QGroupBox()
        pl = QVBoxLayout()
        pl.addWidget(self.psswdT)
        pl.addWidget(self.psswd)
        pg.setLayout(pl)
        
        
        ly.addWidget(wg, 5, 1)
        ly.addWidget(ug, 6, 0)
        ly.addWidget(pg, 6, 1)
        ly.addWidget(bg, 5, 0)
        
        self.setLayout(ly)
        
    def back(self):
        main.list(self.main, self.p)
        
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
        self.setStyleSheet("QDialog{ border: 4px solid #00ccff; border-radius: 20px; }")
        self.exec()
        
        
class Register(QWidget):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        
        ly = QGridLayout()
        self.main = main
        
        if os.path.exists("psswds.pws"):
            lab = QLabel("Please enter your password. The password is required to encrypt your saved passwords. It will not be saved.")
        else:
            lab = QLabel("Please choose a Password. The password is required to encrypt your saved passwords. It will not be saved.")
        lab.setAlignment(Qt.AlignCenter)
        lab.setWordWrap(True)
        self.us = QLineEdit()
        self.us.setPlaceholderText("Password")
        fertig = QPushButton("finish")
        fertig.setStyleSheet("border: 10px solid #00CCFF; border-radius: 50px;")
        fertig.setFixedHeight(100)
        fertig.clicked.connect(self.regg)
        
        ly.addWidget(fertig, 3, 1)
        ly.addWidget(self.us, 2, 1)
        ly.addWidget(lab, 1, 1)
        
        self.setLayout(ly)
        
    def regg(self):
        print(self.us.text())
        if not os.path.exists("psswds.pws"):
            with open("psswds.pws", "w") as f:
                f.write(cryptocode.encrypt("None", self.us.text()))
            main.connc(self.main, self.us.text())
        else:
            with open("psswds.pws", "r") as f:
                inp = f.read()
            if cryptocode.decrypt(inp, self.us.text()):
                main.list(self.main, self.us.text())
            else:
                MessageDialog("Wrong password!", "Wrong password!")




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
