# Proiect: Polinoame de aproximare si interpolare
# Disciplina: Calcul Numeric
# Informatica Anul 2 
# Echipa: Tudor Dragos Bogdan, Zibileanu Sabin si Pavel Alexandru Daniel.
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
import random
import win32api
import timeit
import time
import os
from sympy import *
from tracemalloc import stop
from matplotlib.animation import FuncAnimation, writers
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from tkinter import filedialog
from PyQt5.QtGui import *
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt5 import QtCore,QtGui
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDialog,
    QDoubleSpinBox,
    QFontComboBox,
    QGridLayout,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
) # see https://www.pythonguis.com/tutorials/pyqt-basic-widgets/
import re
#COPYRIGHT Tudor Dragos Bogdan
class Aproximare(QMainWindow):
    # constructor
    def __init__(self, parent=None):
        super(Aproximare, self).__init__(parent)
        #initializari
        
        self.setWindowIcon(QtGui.QIcon('fmi.png'))
        self.setWindowTitle("Polinoame de aproximare - Bernstein")
        self.n=0

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.campFunctie = QLineEdit('exp(sin(x))')
        self.campN = QLineEdit('-')
        self.campA = QLineEdit('0')
        self.campB = QLineEdit('10')
        self.campX = QLineEdit('liniar')
        self.bern = QLineEdit('Aici se va afisa polinomul')

        self.setup_validatori()

        layoutF = QHBoxLayout()
        layoutF.addWidget(QLabel('f = '))
        layoutF.addWidget(self.campFunctie)
        layoutF.addWidget(QLabel('n = '))
        layoutF.addWidget(self.campN)
        self.campN.setMaximumWidth(30)

        layoutAB = QGridLayout()#ca sa poata fii adaugate mesaje eroare text sub campuri
        layoutAB.addWidget(QLabel('a = '), 0, 0)
        layoutAB.addWidget(self.campA, 0 , 1)
        self.eroareA = QLabel("a trebuie sa fie mai mic ca b")

        layoutAB.addWidget(self.eroareA, 1, 1)
        #self.eroareA.setVisible(False)
        layoutAB.addWidget(QLabel('b = '), 0, 2)
        layoutAB.addWidget(self.campB, 0, 3)
        self.eroareB = QLabel("b trebuie sa fie mai mare ca a")
        #self.eroareB.setVisible(False)
        layoutAB.addWidget(self.eroareB, 1, 3)

        self.butonLiniar = QPushButton('Liniar')
        self.butonRandom = QPushButton('Random')
        self.butonTxt = QPushButton('Fisier')
        self.butonLiniar.setMaximumWidth(60)
        self.butonRandom.setMaximumWidth(60)
        self.butonTxt.setMaximumWidth(60)

        layoutX = QGridLayout()
        layoutX.addWidget(QLabel('x = '), 0, 0)
        layoutX.addWidget(self.campX, 0, 1)
        layoutX.addWidget(self.butonLiniar, 0, 2)
        layoutX.addWidget(self.butonRandom, 0, 3)
        layoutX.addWidget(self.butonTxt, 0, 4)
        layoutX.addWidget(QLabel("Se accepta doar numere rationale separate prin spatii"), 1, 1)

        self.butonUrmatorul = QPushButton('Urmatorul grad')
        self.butonFilm = QPushButton('Salveaza ca MP4')
        layoutButoane = QHBoxLayout()
        self.butonPlay = QPushButton('Play')
        layoutButoane.addWidget(self.butonPlay)
        self.butonStop = QPushButton('Stop')
        layoutButoane.addWidget(self.butonStop)
        self.butonReset = QPushButton('Reset')
        layoutButoane.addWidget(self.butonReset)

        layout = QVBoxLayout()

        layout.addLayout(layoutF)
        layout.addLayout(layoutAB)
        layout.addLayout(layoutX)
        layout.addWidget(self.canvas)
        layout.addWidget(self.bern)
        layout.addWidget(self.butonFilm)
        layout.addWidget(self.butonUrmatorul)
        layout.addLayout(layoutButoane)
        
        self.butonFilm.clicked.connect(self.film)
        self.butonUrmatorul.clicked.connect(self.next)
        self.butonPlay.clicked.connect(self.play)
        self.butonStop.clicked.connect(self.stop)
        self.butonReset.clicked.connect(self.reset)

        self.butonRandom.clicked.connect(self.random)
        self.butonLiniar.clicked.connect(self.liniar)
        self.butonTxt.clicked.connect(self.fisier)

        self.campN.textChanged.connect(self.modificare_n)

        self.campX.textChanged.connect(self.reset)
        self.campA.textChanged.connect(self.reset)
        self.campB.textChanged.connect(self.reset)
        self.campFunctie.textChanged.connect(self.reset)

        self.canvas.mpl_connect('button_press_event', self.click_canvas)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()

        fs = 'exp(sin(x))'
        x = Symbol('x')
        self.f = lambdify(x,fs)
        self.a=0
        self.b=10
        self.x_val = np.linspace(self.a, self.b, 100)
        self.t_val = (self.x_val-self.a)/(self.b-self.a) # x_val = t_val*(b-a)+a

        ax=self.figure.add_subplot()
        ax.scatter(self.x_val,self.f(self.x_val))

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)

    def parsare_x(self):
        if len(self.campX.text()) == 0:
            win32api.MessageBox(0, 'Campul x este gol!', 'Eroare camp x', 0x00001030) 
            raise Exception("Campul e gol")
        if self.campX.text() == "liniar":
            return np.linspace(self.a, self.b, 100)
        else:
            if self.campX.text() == "random":
                campXRandom = ""
                for i in range(10):
                    campXRandom+= (str(random.random() * (self.b - self.a) + self.a) + " ")
                self.campX.setText(campXRandom)
            ret_str = self.campX.text().split(" ")
            ret = []
            for curent in ret_str:
                try:
                    if len(curent) != 0:
                        ret.append(float(curent))
                except:
                    win32api.MessageBox(0, 'Campul x contine text sau alte simboluri! Folositi doar numere rationale, separate de simbolul spatiu!', 'Eroare camp x', 0x00001030) 
                    raise Exception("Campul contine altceva in afara de numere")
            if len(ret) == 0:
                win32api.MessageBox(0, 'Campul contine doar spatii!', 'Eroare spatii', 0x00001030) 
                raise Exception("Campul contine doar spatii")
            ret.sort()
            if(self.validare_x(ret)):
                return np.array(ret)
            else:
                raise Exception("x-ul este invalid")

    def actualizare(self) -> bool:
        if self.validare_a() and self.validare_b(): 
            fs = self.campFunctie.text()
            try:
                x = Symbol('x')
                self.f = lambdify(x,fs)
            except:
                return False
            self.a = float(self.campA.text())
            self.b = float(self.campB.text())
            try:
                self.x_val = self.parsare_x()
                self.t_val = (self.x_val-self.a)/(self.b-self.a) # x_val = t_val*(b-a)+a
            except:
                return False
        else:
            return False

        return True

    def modificare_n(self):
        if self.validare_n():
            if self.campN.text() == "-":
                self.n = 0
            else:
                self.n = int(self.campN.text())
        else:
            self.stop()#ne oprim la gradul 1028 deoarece altfel int-ul depaseste lungimea maxima in timpul calculului si primim exceptie

    def update_plot(self):
        self.figure.clear()
        ax=self.figure.add_subplot()
        ax.scatter(self.x_val,self.f(self.x_val))
        start = timeit.default_timer()
        self.campN.setText(str(self.n + 1))
        n=self.n
        f=self.f
        x_val=self.x_val
        t_val=self.t_val
        a=self.a
        b=self.b
        bern = np.zeros_like(self.x_val)
        polinom = "0"
        t="((x-"+str(self.a)+")/("+str(self.b-self.a)+"))"
        autoplaying = self.timer.isActive()
        if not autoplaying and self.n > 50:#polinomul de grad 50 poate dura si 15 secunde calcularea si simplificarea
            autoplaying = True
        for k in range(n+1):
            bern+=f((k/n)*(b-a)+a)*math.comb(n,k)*t_val**k*(1-t_val)**(n-k)
            if not autoplaying:
                polinom+="+"+str(f((k/n)*(b-a)+a)*math.comb(n,k))+"*"+t+"**" + str(k) + "*(1-"+t+")**("+str(n-k)+")"
        if not autoplaying:
            polinom="B(x)="+str(simplify(polinom))#consuma foarte mult procesor!
            self.bern.setText(polinom)
        else:
            self.bern.setText("Calcularea string-ului ar dura peste 15 secunde.")
        stop = timeit.default_timer()
        ax.plot(x_val,bern)
        ab = np.array((self.a, self.b))
        ax.scatter(ab, self.f(ab), c ="red")
        plt.suptitle('Gradul '+str(n))
        plt.title('Timp: ' + str(round((stop-start)*1000, 2)) + "ms")
        self.canvas.draw()
    
    def next(self):
        if self.actualizare():
            self.timer.stop()
            self.update_plot()
    def play(self):
        if self.actualizare():
            self.timer.start()
    def stop(self):
        self.timer.stop()
    def reset(self):
        self.timer.stop()
        self.campN.setText("-")
        self.figure.clear()
        ax=self.figure.add_subplot()
        self.actualizare()
        ax.scatter(self.x_val,self.f(self.x_val))
        ab = np.array((self.a, self.b))
        ax.scatter(ab, self.f(ab), c ="red")
        self.canvas.draw()

    def parsare_fisier(self, continut_cifre):
        ret = ""
        try:
            for curent in continut_cifre:
                if len(curent) != 0:
                    ret += str(float(curent)) + " "#convertim de la string la float si inapoi la string pentru a primi exceptie daca nr nu e convertibil la float
            self.campX.setText(ret)
        except:
            win32api.MessageBox(0, 'Fisierul contine caractere nepermise. Pot fii folosite doar numere rationale, separate de spatii, tab-uri sau enter-uri', 'Eroare fisier caractere nepermise', 0x00001030) 

    def liniar(self):
        self.campX.setText("liniar")
    def random(self):
        self.campX.setText("random")
    def fisier(self):
        path_fisier = filedialog.askopenfilename(filetypes=[("Toate acceptate", ".txt .tsv .csv"), ("Fisier text", ".txt"), ("Fisier excel", ".tsv .csv")])
        try:
            nume_fisier_spart = path_fisier.split(".")
            if len(nume_fisier_spart) < 2:
                raise Exception("Fisierul nu are extensie")#se va afisa mesajul din lin 285
            extensie_fisier = nume_fisier_spart[len(nume_fisier_spart) - 1]
            fisier = open(path_fisier, 'r')
            continut = fisier.read()
            fisier.close()
            if extensie_fisier == "txt" or extensie_fisier == "tsv":
                self.parsare_fisier(continut.split()) 
            elif extensie_fisier == "csv":
                self.parsare_fisier(re.split(",|\n", continut))
            else:
                win32api.MessageBox(0, 'Din pacate, acest tip de fisier nu poate fii deschis la acest moment', 'Eroare fisier deschis', 0x00001030) 
        except:
            win32api.MessageBox(0, 'Nu s-a putut deschide fisierul', 'Eroare fisier', 0x00001030) 
    def click_canvas(self, event):
        if event.xdata != None:
            if self.campX.text() == "random" or self.campX.text() == "liniar":
                self.campX.setText(str(event.xdata))
            else:
                self.campX.setText(self.campX.text() + " " + str(event.xdata))

    def film(self):
        def frame_film(n):
            bern = np.zeros_like(x_val)
            for k in range(n + 1):
                bern += f(k/n * (b-a) + a)*math.comb(n,k)*t**k*(1-t)**(n-k)
            ax.plot(x_val, bern)
            plt.title('Gradul: ' + str(n))
        if self.n < 5:
            win32api.MessageBox(0, 'Nu poti salva un clip atat de scurt! Seteaza gradul polinomului la minim 5.', 'Eroare grad', 0x00001030) 
            return
        succes = True
        try:
            path_salvare = filedialog.asksaveasfilename(filetypes=[("Fisier video", "*.mp4")])
            metadata = dict(title = 'Polinom aproximare Bernstein')
            Writer = writers['ffmpeg']
            writer = Writer(fps = 5, metadata=metadata)
            fig = plt.figure()
            f = self.f
            a = self.a
            b = self.b
            x_val = self.x_val
            t = self.t_val
            ax = plt.axes()
            ax.scatter(x_val, f(x_val))
            nmax = self.n
            anim = FuncAnimation(fig, func = frame_film, interval = 200, frames = np.arange(1,nmax+1))
            anim.save(path_salvare, writer)
        except:
            win32api.MessageBox(0, 'Nu s-a putut salva. Extensia solcitata nu e valida.', 'Eroare film', 0x00001030)
            succes = False
        finally:#daca dam sys.exit in acel try-catch, aplicatia nu se va inchide.
            if succes == True:
                win32api.MessageBox(0, 'Aplicatia acum se va inchide si veti naviga la fisier.', 'Succes', 0x00001040)
                os.startfile(path_salvare)
                sys.exit()

#COPYRIGHT Pavel Alexandru Daniel
    def setup_validatori(self):
        self.campN.setMaxLength(4)
        self.campN.setValidator(QIntValidator())
        self.campB.setMaxLength(4)
        self.campB.setValidator(QIntValidator())
        self.campA.setMaxLength(4)
        self.campA.setValidator(QIntValidator())

    def validare_n(self):
        if len(self.campN.text()) == 0:
           win32api.MessageBox(0, 'Campul n este gol!', 'Eroare camp n ', 0x00001030)
           return False
        valoare_n = 0 if self.campN.text() == "-" else float(self.campN.text())
        if valoare_n > 1028 and len(self.campN.text()) != 0:
           win32api.MessageBox(0, 'Campul n trebuie sa fie mai mic ca 1028!', 'Eroare camp n ', 0x00001030)
           return False
        
        #if len(self.campN.text()) < 1028 and len(self.campN.text()) == 0:
        #    win32api.MessageBox(0, 'Campul n este gol!', 'Eroare camp n ', 0x00001030)
        #elif len(self.campN.text()) > 1028 and len(self.campN.text()) != 0:
        #    win32api.MessageBox(0, 'Campul n trebuie sa fie mai mic ca 1028!', 'Eroare camp n ', 0x00001030)
        #elif len(self.campN.text()) > 1028 and len(self.campN.text()) != 0:
        #    win32api.MessageBox(0, 'Aveti doua erori. Campul n este gol! si Campul n trebuie sa fie mai mic ca 1028!', 'Eroare camp n ', 0x00001030)
        #else:
        #    pass
        
        #print("Valideaza daca campul n este un numar sau o -, coloreaza-l cu rosu daca nu. Deasemenea, n sa fie mai mic ca 1028 (Alexandru)")
        return True

    def validare_a(self):
        #if len(self.campA.text()) == 0:
        #    win32api.MessageBox(0, 'Campul a este gol!', 'Eroare camp a', 0x00001030) 

        #print("Valideaza daca campul a e nr si e mai mic ca b, coloreaza cu rosu daca daca nu (Alexandru)")
        
        if len(self.campA.text()) == 0:
           win32api.MessageBox(0, 'Campul a este gol!', 'Eroare camp a ', 0x00001030)
           return False
        if float(self.campA.text()) >= float(self.campB.text()):
           win32api.MessageBox(0, 'Campul a trebuie sa fie mai mic ca b!', 'Eroare camp a ', 0x00001030)
           return False
        return True

    def validare_b(self):
        #if len(self.campB.text()) == 0:
        #    win32api.MessageBox(0, 'Campul b este gol!', 'Eroare camp b', 0x00001030) 
        
        #print("Valideaza daca campul b e nr si e mai mare ca a, coloreaza cu rosu daca nu (Alexandru)")

        if len(self.campB.text()) == 0:
           win32api.MessageBox(0, 'Campul b este gol!', 'Eroare camp b ', 0x00001030)
           return False
        if float(self.campB.text()) <= float(self.campA.text()):
           win32api.MessageBox(0, 'Campul b trebuie sa fie mai mare ca a!', 'Eroare camp b ', 0x00001030)
           return False
        return True

    def validare_x(self, x):
        for i in x:
            if i < self.a or i > self.b:
                win32api.MessageBox(0, 'Numerele din x trebuie sa fie intre a si b!', 'Eroare camp x ', 0x00001030)
                return False
        return True

#COPYRIGHT Zibileanu Sabin si Pavel Alexandru Daniel
dictionar_inlocuiri = {
            'sin' : 'np.sin',
            'cos' : 'np.cos',
            'exp': 'np.exp',
            'sqrt': 'np.sqrt',
            '^': '**',
        }

dictionar_functii = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
]



class Window(QMainWindow):

    def __init__(self,parent=None):
        
        self.t0 = time.time()
        x = Symbol('x')
        super(Window,self).__init__(parent)
        #fs = sin(x) #exemplu
        self.n = 1
        
        self.setWindowIcon(QtGui.QIcon('fmi.png'))
        self.setWindowTitle("Polinoame interpolare - Lagrange")
        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.butonfisier = QPushButton("Citeste din fisier numerele")
        self.butonRandom = QPushButton("Liniar")
        self.butonplay = QPushButton("Play")
        self.butonMP4 = QPushButton("Salveaza ca film")
        self.butonReset = QPushButton("Reset")
        self.butonStop = QPushButton("Stop")
        self.butonClick = QPushButton("Adauga puncte prin click")

        self.butonplay.clicked.connect(self.plot)
        self.butonReset.clicked.connect(self.reset)
        self.butonStop.clicked.connect(self.stop)
        self.butonMP4.clicked.connect(self.crearefilm)
        self.butonRandom.clicked.connect(self.verificaremodalitate)
        self.butonClick.clicked.connect(self.modclick)
        self.butonfisier.clicked.connect(self.modfisier)
        self.butonMP4.setEnabled(False)
        self.butonStop.setEnabled(False)
        self.butonReset.setEnabled(False)

        layout = QGridLayout()
        layout_intervale = QVBoxLayout()
        layout_functie = QHBoxLayout()
        layout_nrpct = QHBoxLayout()
        layout_canvas = QVBoxLayout()
        layout_butoane = QHBoxLayout()

        layout_butoane.addWidget(self.butonReset)
        
        layout_butoane.addWidget(self.butonStop)

        label = QLabel("Introdu functia dorita:")
        layout_functie.addWidget(label)
        self.textbox_fct = QLineEdit(self)
        layout_functie.addWidget(self.textbox_fct)

        label_a = QLabel("a:")
        layout_intervale.addWidget(label_a)
        self.textbox_a = QLineEdit(self)
        layout_intervale.addWidget(self.textbox_a)
        
        label_b = QLabel("b:")
        layout_intervale.addWidget(label_b)
        self.textbox_b = QLineEdit(self)
        layout_intervale.addWidget(self.textbox_b)


        label_puncte = QLabel("Modalitate citire puncte:")
        layout_nrpct.addWidget(label_puncte)
        self.textbox_puncte = QLineEdit(self)
        layout_nrpct.addWidget(self.textbox_puncte)
        layout_nrpct.addWidget(self.butonfisier)
        layout_nrpct.addWidget(self.butonRandom)
        layout_nrpct.addWidget(self.butonClick)

        layout_canvas.addWidget(self.canvas)

        
        label_restrictie = QLabel("Restrictie : a < b")
        layout.addWidget(label_restrictie,2,0)


        label_restrictie2 = QLabel("Trebuie scrisa metoda in care vor fi importate numerele altfel butonul de play nu va fi valabil")
        layout.addWidget(label_restrictie2,4,0)
        layout.addWidget(self.butonplay,6,0)
        layout.addWidget(self.butonMP4,7,0)
        self.butonplay.setEnabled(False)

        layout.addLayout(layout_intervale,1,0)
        layout.addLayout(layout_functie,0,0)
        layout.addLayout(layout_nrpct,3,0)
        layout.addLayout(layout_canvas,5,0)
        layout.addLayout(layout_butoane,8,0)
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()
        self.contor_clickuri = 0
        self.coordonate_puncte = np.empty(0)
        self.x_val = np.empty(0)
        self.regex = '^[0][0-9]+$'
        
    def plot(self):
        try:
            fs = self.textbox_fct.text()#fe.text()
            x = Symbol('x')
            self.f = lambdify(x,fs)
            eval(fs)
        except SyntaxError:
            win32api.MessageBox(0,'Nu ai introdus o functie valida','Eroare')
            self.butonplay.setEnabled(False)
            return   
        
        #fs = self.textbox_fct.text()#fe.text()
        #x = Symbol('x')
        #self.f = lambdify(x,fs)
        if(self.string2func() == False):
                win32api.MessageBox(0,'Nu ai introdus o functie valida','Eroare')
                self.figure.clear()
                self.canvas.draw()
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                return
    
        
        if(self.textbox_puncte.text() == "fisier"):
            try:
                with open("puncte.txt") as fisier:
                    for coord in fisier:
                       self.coordonate_puncte = np.append(self.coordonate_puncte,float(coord))
            except ValueError:
                win32api.MessageBox('0','In fisier trebuie sa ai doar numere reale!','Eroare')
                self.butonplay.setEnabled(False)
                return
            index_ultim = len(self.coordonate_puncte)
            if(self.coordonate_puncte[0] < float(self.textbox_a.text()) or self.coordonate_puncte[index_ultim - 1] > float(self.textbox_b.text())):
                    win32api.MessageBox('0','Datele pe care ai incercat sa le importi sunt invalide deoarece nu se incadreaza in intervalul a b','Eroare')
                    self.coordonate_puncte = np.empty(0)
                    self.textbox_puncte.clear()
                    self.butonplay.setEnabled(False)
                    return
            
            if(index_ultim < 3):
                    win32api.MessageBox('0','Lungimea intervalului este invalida','Eroare')
                    self.coordonate_puncte = np.empty(0)
                    self.textbox_puncte.clear()
                    self.butonplay.setEnabled(False)
                    return
            
           

            self.x_val = self.coordonate_puncte
            self.textbox_puncte.clear()
            self.textbox_puncte.setText(str(self.x_val))
    
        if(self.textbox_puncte.text() == "liniar"):
            if(re.search(self.regex,self.textbox_a.text()) or re.search(self.regex,self.textbox_b.text())):
                win32api.MessageBox('0','Nu poti introduce 0 inaintea unui numar','Eroare')
                self.butonplay.setEnabled(False)
                self.textbox_puncte.clear()
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.coordonate_puncte = np.empty(0)
                return
            try:
                self.a=float(self.textbox_a.text())
                self.b = float(self.textbox_b.text())
            except ValueError:
                win32api.MessageBox('0','Datele intervalului sunt invalide','Eroare')
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                return
            self.x_val = np.linspace(self.a,self.b,100)
            self.textbox_puncte.clear()
            self.textbox_puncte.setText(str(self.x_val))
            self.coordonate_puncte = self.x_val
            self.butonplay.setEnabled(True)
            self.butonStop.setEnabled(True)
            self.butonReset.setEnabled(True)
            self.butonMP4.setEnabled(True)
        
        if(self.textbox_puncte.text() == "click"):
            if(len(self.coordonate_puncte) < 3):
                win32api.MessageBox('0','Lungimea intervalului este invalida','Eroare')
                self.coordonate_puncte = np.empty(0)
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                self.figure.clear()
                self.canvas.draw()
                return
            
            self.x_val = self.coordonate_puncte
            self.x_val.sort()
            index_ultim = len(self.x_val)
            self.textbox_puncte.setText(str(self.coordonate_puncte))
            if(self.x_val[0] < float(self.textbox_a.text()) or self.x_val[index_ultim - 1] > float(self.textbox_b.text())):
                win32api.MessageBox('0','Datele pe care ai incercat sa le importi sunt invalide','Eroare')
                self.coordonate_puncte = np.empty(0)
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                self.figure.clear()
                self.canvas.draw()
                return
        
       
        self.butonStop.setEnabled(True)
        self.butonReset.setEnabled(True)
        self.butonMP4.setEnabled(True)
        t0 = time.time()
        self.t_val = (self.x_val-self.a)/(self.b-self.a) # x_val = t_val*(b-a)+a
        self.ax=self.figure.add_subplot(111)
        self.ax.scatter(self.x_val,self.f(self.x_val))
        
        self.figure.clear()
        self.ax=self.figure.add_subplot(111)
        self.ax.scatter(self.x_val,self.f(self.x_val))
        self.n+=1
        n=self.n
        f=self.f
        x_val=self.x_val
        t_val=self.t_val
        a=self.a
        b=self.b
        xi = np.linspace(a,b,n+1)
        #ax.scatter(xi,f(xi))
        l = np.zeros_like(self.x_val)
        for j in range(1,n+1):
            prod = 1
            for i in range(1,n+1):
                if i != j:
                    prod*=(x_val - xi[i])/(xi[j] - xi[i]) 
            l+=f(xi[j])*prod
        self.ax.plot(x_val,l)
        t1 = time.time()
        plt.suptitle('Grad ' + str(n) + '\n' + 'Timp:' + str(t1-t0))
        self.canvas.draw()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(400)
        self.timer.timeout.connect(self.plot)
        self.timer.start()
        #t1 = time.time()
    def reset(self):
        self.figure.clear()
        self.canvas.draw()
        self.n = 0
        self.timer.stop()
        self.textbox_puncte.clear()
        self.butonplay.setEnabled(False)
        self.coordonate_puncte = np.empty(0)
        self.butonMP4.setEnabled(False)
        self.butonStop.setEnabled(False)
        self.butonReset.setEnabled(False)
        self.textbox_a.clear()
        self.textbox_b.clear()
        self.textbox_fct.clear()
    def stop(self):
        self.timer.stop()
        #self.canvas = FigureCanvas(self.figure)
    
    def crearefilm(self):
        def vizualizare_film(n):
                xi = np.linspace(a,b,n+1)
                #ax.scatter(xi, f(xi))
                l = np.zeros_like(x_val) 
                for j in range(1,n+1):
                    prod = 1
                    for i in range(1, n+1):  
                        if i!=j:
                            prod*=(x_val - xi[i])/(xi[j] - xi[i]) 
                    l+=f(xi[j])*prod
                ax.plot(x_val,l)
                plt.title('Grad:' + str(n))
        succes = True        
        try:
                metadata = dict(title = 'Lagrange')
                Writer = writers['ffmpeg']
                writer = Writer(fps = 1, metadata=metadata)
                fig = plt.figure()
                f = self.f
                a = self.a
                b = self.b
                x_val = self.x_val
                t = self.t_val
                ax = plt.axes()
                ax.scatter(x_val, f(x_val))
                nmax = self.n
                anim = FuncAnimation(fig, func = vizualizare_film, interval = 200, frames = np.arange(1,nmax+1))
                anim.save('Lagrange.mp4', writer)
                self.reset()
                #self.plot()
        except:
                succes = False
            
    def verificaremodalitate(self):
        
        if(self.textbox_puncte.text() == "liniar"):
            if(re.search(self.regex,self.textbox_a.text()) or re.search(self.regex,self.textbox_b.text())):
                win32api.MessageBox('0','Nu poti introduce 0 inaintea unui numar','Eroare')
                self.butonplay.setEnabled(False)
                self.textbox_puncte.clear()
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.coordonate_puncte = np.empty(0)
                return
            try:
                self.a=float(self.textbox_a.text())
                self.b = float(self.textbox_b.text())
            except ValueError:
                win32api.MessageBox('0','Datele intervalului sunt invalide','Eroare')
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                return

            if(self.a >= self.b):
                win32api.MessageBox('0','Intervalul nu a fost introdus corect,te rugam verifica','Eroare')
                self.butonplay.setEnabled(False)
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.textbox_puncte.clear()
                self.coordonate_puncte = np.empty(0)
                return
            if(self.validari_campuri_goale() == False):
                return
            else:    
            #print(self.validari_campuri_goale())
                win32api.MessageBox(0,'Numerele au fost generate cu succes','Mesaj')
                self.butonplay.setEnabled(True)
                return true
        else:
            win32api.MessageBox(0,'Nu ai scris corect','Eroare')
    
    def _on_left_click(self, event):
        
        self.contor_clickuri+=1
        plt.title('Fa click pe ecran pentru a introduce puncte cu mouse-ul')
        if(self.contor_clickuri !=1):
            if event.xdata is not None:
                self.coordonate_puncte = np.append(self.coordonate_puncte,event.xdata)
            self.ax.scatter(event.xdata,event.ydata)
            self.canvas.draw()

    def modclick(self):
       
        if(self.textbox_puncte.text() == "click"):
            if(self.validari_campuri_goale() == False):
                return
            
            try:
                fs = self.textbox_fct.text()#fe.text()
                x = Symbol('x')
                self.f = lambdify(x,fs)
                eval(fs)
            except SyntaxError:
                win32api.MessageBox(0,'Nu ai introdus o functie valida','Eroare')
                self.butonplay.setEnabled(False)
                return  

            if(re.search(self.regex,self.textbox_a.text()) or re.search(self.regex,self.textbox_b.text())):
                win32api.MessageBox('0','Nu poti introduce 0 inaintea unui numar','Eroare')
                self.butonplay.setEnabled(False)
                self.textbox_puncte.clear()
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.coordonate_puncte = np.empty(0)
                return
            try:
                self.a=float(self.textbox_a.text())
                self.b = float(self.textbox_b.text())
            except ValueError:
                win32api.MessageBox('0','Datele intervalului sunt invalide','Eroare')
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                return

            if(self.a >= self.b):
                win32api.MessageBox('0','Intervalul nu a fost introdus corect,te rugam verifica','Eroare')
                self.butonplay.setEnabled(False)
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.textbox_puncte.clear()
                self.coordonate_puncte = np.empty(0)
                return

            if(self.string2func() == False):
                win32api.MessageBox('0','Functie invalida','Avertisment')
                return
            else:    
                win32api.MessageBox(0,'Vei adauga puncte prin click(Atentie:punctele nu trebuie sa depaseasca valoare b a intervalului)','Mesaj')
                self.butonplay.setEnabled(True)
                self.ax=self.figure.add_subplot(111)
                self.canvas.mpl_connect("button_press_event", self._on_left_click)
                plt.xlim(float(self.textbox_a.text()),float(self.textbox_b.text()))
            #plt.ylim(float(self.textbox_a.text()),float(self.textbox_b.text()))
                plt.ylim(0,25)
        else:
            win32api.MessageBox(0,'Nu ai scris corect','Eroare')
    
    def modfisier(self):
        if(self.textbox_puncte.text() == "fisier"):
            if(re.search(self.regex,self.textbox_a.text()) or re.search(self.regex,self.textbox_b.text())):
                win32api.MessageBox('0','Nu poti introduce 0 inaintea unui numar','Eroare')
                self.butonplay.setEnabled(False)
                self.textbox_puncte.clear()
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.coordonate_puncte = np.empty(0)
                return
            try:
                self.a=float(self.textbox_a.text())
                self.b = float(self.textbox_b.text())
            except ValueError:
                win32api.MessageBox('0','Datele intervalului sunt invalide','Eroare')
                self.textbox_puncte.clear()
                self.butonplay.setEnabled(False)
                return
            if(self.validari_campuri_goale() == False):
                return
            if(self.a >= self.b):
                win32api.MessageBox('0','Intervalul nu a fost introdus corect,te rugam verifica','Eroare')
                self.butonplay.setEnabled(False)
                self.butonMP4.setEnabled(False)
                self.butonStop.setEnabled(False)
                self.butonReset.setEnabled(False)
                self.textbox_puncte.clear()
                self.coordonate_puncte = np.empty(0)
                return
            else:
                win32api.MessageBox(0,'Numerele din fisierul puncte.txt vor fi adaugate','Mesaj')
                self.butonplay.setEnabled(True)
        else:
            win32api.MessageBox(0,'Nu ai scris corect','Eroare')
    def string2func(self):
        #verificam validitatea functiei
        string = self.textbox_fct.text()
        if(string.isdigit() == True):
            return False
        for cuvant in re.findall('[a-zA-Z_]+', string):
            
            if cuvant not in dictionar_functii:
                return false

        for replacement, nou in dictionar_inlocuiri.items():
            string = string.replace(replacement, nou)

        def func(x):
            return eval(string)

        return func
    def validari_campuri_goale(self):
        if(len(self.textbox_a.text()) != 0 and len(self.textbox_b.text()) != 0 and len(self.textbox_fct.text()) != 0):
            return True
        else:
            if(len(self.textbox_a.text()) == 0 and len(self.textbox_b.text()) == 0 and len(self.textbox_fct.text()) == 0):
                win32api.MessageBox('0','Toate campurile sunt goale!','Avertisment')
                return False
            if(len(self.textbox_a.text()) == 0 or len(self.textbox_b.text()) == 0):
                if(len(self.textbox_fct.text()) == 0):
                    win32api.MessageBox('0','Verifica campurile a si b deoarece unul din ele sau amandoua sunt goale si campul functiei este gol!','Avertisment')     
                    return False
                else:
                    win32api.MessageBox('0','Unul din campurile a si b este gol,te rugam verifica!','Avertisment')
                    return False
            if(len(self.textbox_fct.text()) == 0):
                win32api.MessageBox('0','Verifica campul functiei deoarece este gol!','Avertisment')
                return False 
    #COPYRIGHT Pavel Alexandru Daniel
    def validare_a(self):
        if len(self.textbox_a()) == 0:
           win32api.MessageBox(0, 'Campul a este gol!', 'Eroare camp a ', 0x00001030)
           return False
        elif len(self.textbox_a()) > len(self.textbox_b()):
           win32api.MessageBox(0, 'Campul a trebuie sa fie mai mic ca b!', 'Eroare camp a ', 0x00001030)
           return False
        return True

    def validare_b(self):
        if len(self.textbox_b()) == 0:
           win32api.MessageBox(0, 'Campul b este gol!', 'Eroare camp b ', 0x00001030)
           return False
        elif len(self.textbox_b()) < len(self.textbox_a()):
           win32api.MessageBox(0, 'Campul b trebuie sa fie mai mic ca a!', 'Eroare camp b ', 0x00001030)
           return False
        return True

#COPYRIGHT Pavel Alexandru Daniel
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QtGui.QIcon('univ.png'))
        self.setWindowTitle("Pagina principala - Proiect Calcul Numeric")

        self.setStyleSheet("""
            QLineEdit{
                font-size: 30px
            }
            QPushButton{
                font-size: 30px
            }
            """)

        self.window1 = Aproximare()
        self.window1.hide()
        self.window2 = Window()
        self.window2.hide()

        l = QVBoxLayout()
        button1 = QPushButton("Accesati Polinoame de aproximare - Bernstein ")
        button1.clicked.connect(self.toggle_window1)
        
        l.addWidget(button1)

        button2 = QPushButton("Accesati Polinoame interpolare - Lagrange")
        button2.clicked.connect(self.toggle_window2)
        l.addWidget(button2)

        w = QWidget()
        w.setLayout(l)
        self.setCentralWidget(w)

    def toggle_window1(self, checked):
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()

    def toggle_window2(self, checked):
        if self.window2.isVisible():
            self.window2.hide()

        else:
            self.window2.show()

app = QApplication(sys.argv)

interfata_principala = MainWindow()
interfata_principala.resize(1280, 720)
interfata_principala.show()
app.exec()