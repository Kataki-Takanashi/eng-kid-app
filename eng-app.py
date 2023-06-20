#Eng-App by: Kataki_Takanashi

#Imports
import json
import sys
from time import *
import threading
import random

from PyQt5.QtCore import pyqtSignal

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QIcon



def settings():
    with open('settings.json', 'r') as f:
        global config
        config = json.load(f)
        return config

class homeScreen(QDialog):

    def __init__(self):
        super(homeScreen, self).__init__()
        uic.loadUi("The Book-INATOR.ui", self)

        self.game.hide()

        self.difclt_Slider.setValue(settings()["words"])
        self.difclt_Seconds.setValue(settings()["secs"])
        self.difclt_Slider.valueChanged.connect(self.wordCount)
        self.difclt_Seconds.valueChanged.connect(self.secCount)
        self.wordCount()
        self.secCount()
        self.play.setIcon(QIcon("Play-button-icon-in-yellow-color-on-transparent-background-PNG-2.png"))
        self.play.clicked.connect(lambda: self.start(self.words, self.secs))
        self.next_Button.clicked.connect(self.next)
        self.next_Flag = False
        self.current_Index = 0

    def wordCount(self):
        global words
        self.difclt_Num.display(self.difclt_Slider.value()*100)
        self.words = self.difclt_Slider.value()

    def secCount(self):
        global secs
        self.secs = self.difclt_Seconds.value()

    def next(self):
        self.next_Flag = True

    def timer(self, secs):
        self.time_left = secs

        for i in range(secs):
            self.time_left -= 1
            sleep(1)
            # self.timer_Bar.setValue(int(self.time_left/secs*100))
            if self.time_left <= 0:
                self.nextWord()
                self.wrong_words.append(self.wods[self.current_Index])
                break
            if self.next_Flag:
                self.nextWord()
                self.used_words.append(self.wods[self.current_Index])
                break
            print(self.time_left)

    def start(self, words, secs):
        config = {
    "words": self.words,
    "secs": self.secs
  }
        with open('settings.json', 'w') as f:
            json.dump(config, f)

        # Start
        self.used_words = []
        self.wrong_words = []
        with open('words.json', 'r') as f:
            self.wods = json.load(f)["logs"]

        random.shuffle(self.wods)
        self.nextWord()


    def nextWord(self):
        enwords = [(i, c) for i, c in enumerate(self.wods)]
        if self.current_Index >= self.words*100:
            self.word.setText(f"Accuracy: {len(self.used_words)/(len(self.used_words) + len(self.wrong_words))*100}%")
            sys.exit()

        self.word.setText(self.wods[self.current_Index])
        timeer = threading.Thread(target=lambda: self.timer(self.secs))
        timeer.start()
        self.current_Index += 1
        self.next_Flag = False





class mainUi(QDialog):

    def __int__(self):
        super(mainUi, self).__int__()
        uic.loadUi("testPage.ui", self)

        self.home_Button.clicked.connect(self.go_Home)

    def go_Home(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()
login_scrn = homeScreen()
main_scrn = mainUi()
widget.addWidget(login_scrn)
widget.addWidget(main_scrn)
widget.show()
app.exec_()