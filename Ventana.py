import sys
from PyQt4 import QtGui, QtCore
from Osciloscopio import *
#from Modbus import *
from Pines import *
import numpy as np
import time
import math
import pylab
from scipy.special import erfc
import logging

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter, MultipleLocator
from matplotlib.widgets import Cursor, Slider
from matplotlib.patches import Rectangle

class VentanaInfo(QtGui.QWidget):
  '''Tiene un boton aceptar para volver al orden de ejecucion'''
  
  def __init__(self, texto):
    '''Constructor de una ventana de informacion
    
    Parametros:
      texto: Texto que mostrar'a la ventana
    
    '''
    super(VentanaInfo, self).__init__()
    self.inicializa(texto)
  
  def inicializa(self, texto):
    win = QtGui.QMessageBox()
    win.timer = QtCore.QTimer(self)
    win.timer.timeout.connect(win.close)
    win.timer.start(10000) # Se cierra automaticamente a los 10 segundos
    win.setInformativeText(texto)
    win.setWindowTitle('Aviso')
    win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    win.exec_()

class VentanaAviso(QtGui.QDialog):
  '''No tiene boton'''
  
  def __init__(self, texto):
    QtGui.QDialog.__init__(self)
    self.setModal(True)
    self.inicializa(texto)
  
  def inicializa(self, texto):
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    aviso = QtGui.QLabel(texto)
    self.barra = QtGui.QProgressBar(self)
    self.barra.setMinimum(1)
    self.barra.setMaximum(64)

    grid.addWidget(aviso, 1, 1)
    grid.addWidget(self.barra, 2, 1)
    
    self.setLayout(grid) 
    self.setGeometry(200, 200, 200, 200)
    self.setWindowTitle('Aviso')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    
  def actualiza_barra(self, val):
    self.barra.setValue(val)

class VentanaPrincipal(QtGui.QWidget):
  global osc
  
  def __init__(self, osciloscopio):
    ''' Constructor de la ventana de inicio de la aplicacion.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    
    super(VentanaPrincipal, self).__init__()
    self.osc = osciloscopio
    self.rellenaVentana()
  
  def rellenaVentana(self):
    
    #grid = QtGui.QGridLayout()
    #grid.setSpacing(5)
    grid = QtGui.QVBoxLayout()
    
    tit_aptd1 = QtGui.QLabel('Configuracion del generador')
    tit_aptd2 = QtGui.QLabel('Adquisicion diagrama de ojo')
    
    bot_a1 = QtGui.QPushButton('Ir', self)
    bot_a2 = QtGui.QPushButton('Ir', self)
    bot_cerrar = QtGui.QPushButton('Cerrar', self)
    bot_a1.setFixedSize(60,30)
    bot_a2.setFixedSize(60,30)
    bot_cerrar.setFixedSize(60,30)
    
    l1 = QtGui.QHBoxLayout()
    l2 = QtGui.QHBoxLayout()
    l3 = QtGui.QHBoxLayout()
    
    l1.addWidget(tit_aptd1)
    l1.addWidget(bot_a1)
    l2.addWidget(tit_aptd2)
    l2.addWidget(bot_a2)
    l3.addWidget(bot_cerrar)
    
    bot_cerrar.clicked.connect(QtCore.QCoreApplication.instance().quit)
    bot_a1.clicked.connect(lambda: self.long_trama())
    bot_a2.clicked.connect(lambda: self.ojo())
    
    grid.addLayout(l1)
    grid.addLayout(l2)
    grid.addLayout(l3)
    
    self.setLayout(grid)
    self.setWindowTitle('Sistemas de Comunicacion')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    self.setFixedSize(280,150)
    self.show()
    
  def long_trama(self):
    self.c_trama = VentanaConfigIO()
  
  def ojo(self):
    self.ConfOjo = VentanaConfigOjo(self.osc)

class VentanaConfigOjo(QtGui.QWidget):
  global osc
  
  def __init__(self, osciloscopio):
    ''' Constructor de la ventana de inicio de la aplicacion.
    
    Parametros:
      osciloscopio: Objeto de la clase Osciloscopio
    
    '''
    
    super(VentanaConfigOjo, self).__init__()
    self.osc = osciloscopio
    self.rellenaVentana()
  
  def rellenaVentana(self):
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_up = QtGui.QLabel('Uplink')
    tit_dw = QtGui.QLabel('Downlink')
    tit_tasa_u = QtGui.QLabel('Tasa binaria')
    tit_tasa_d = QtGui.QLabel('Tasa binaria')
    tit_long_u = QtGui.QLabel('Longitud de trama')
    tit_long_d = QtGui.QLabel('Longitud de trama')
    
    desp_tasa_u = QtGui.QComboBox(self)
    desp_tasa_d = QtGui.QComboBox(self)
    desp_long_u = QtGui.QComboBox(self)
    desp_long_d = QtGui.QComboBox(self)
    
    tasas = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    longitudes = ["4", "8", "12", "16"]
    
    for t in tasas:
      desp_tasa_u.addItem(t)
      desp_tasa_d.addItem(t)
    for l in longitudes:
      desp_long_u.addItem(l)
      desp_long_d.addItem(l)
    
    bot_aceptar = QtGui.QPushButton('Adquirir', self)
    
    grid.addWidget(tit_up, 0, 1)
    grid.addWidget(tit_dw, 0, 4)
    grid.addWidget(tit_tasa_u, 2, 1)
    grid.addWidget(tit_tasa_d, 2, 4)
    grid.addWidget(tit_long_u, 3, 1)
    grid.addWidget(tit_long_d, 3, 4)
    grid.addWidget(desp_tasa_u, 2, 2)
    grid.addWidget(desp_tasa_d, 2, 5)
    grid.addWidget(desp_long_u, 3, 2)
    grid.addWidget(desp_long_d, 3, 5)
    grid.addWidget(bot_aceptar, 6, 3)
    
    bot_aceptar.clicked.connect(lambda: self.aceptar(desp_tasa_u.currentText(), desp_long_u.currentText(), desp_tasa_d.currentText(), desp_long_d.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle('FTTH')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    self.show()
    
  def aceptar(self, tasa_u, long_u, tasa_d, long_d):
    # Diccionarios
    base_tiempos = {"10 Mbps":'50ns', "30 Mbps":'10ns', "70 Mbps":'5ns', "125 Mbps":'2.5ns'}
    length = {"4":0, "8":1, "12":2, "16":3}
    rate = {"125 Mbps":3, "70 Mbps":2, "30 Mbps":1, "10 Mbps":0}
    
    # Mostramos los dos canales del osciloscopio
    self.osc.disp_channel(True, '1')
    self.osc.disp_channel(True, '2')
    
    # Llamada a Pines o a Modbus
    pines = PinesFPGA()
    pines.setClock(1)
    
    pines.setLength1(length[str(long_u)])
    pines.setRate1(rate[str(tasa_u)])
    
    pines.setLength2(length[str(long_d)])
    pines.setRate2(rate[str(tasa_d)])
    
    self.osc.set_display("YT")
    self.osc.set_persistence_off()
    self.osc.set_horizontal(base_tiempos[str(tasa_u)]) #Por los qstring de qt4
    self.osc.autoset('1')
    
    # Configuramos el disparo
    self.osc.set_trigger('ext', 1)
    aviso = VentanaAviso('La adquisicion de datos puede tardar un tiempo.\n\nEspere, por favor.')
    aviso.show()
    lista_medidas1 = []
    
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      aviso.actualiza_barra(i)
      QtCore.QCoreApplication.processEvents()
      medidas1 , inc_tiempo1 = self.osc.get_data('1', 250, 1750, '1')
      lista_medidas1.append(medidas1)
    
    pines.setClock(2)
    self.osc.set_horizontal(base_tiempos[str(tasa_d)]) #Por los qstring de qt4
    self.osc.autoset('2')
    
    
    lista_medidas2 = []
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      aviso.actualiza_barra(i+32)
      QtCore.QCoreApplication.processEvents()
      medidas2 , inc_tiempo2 = self.osc.get_data('2', 250, 1750, '1')
      lista_medidas2.append(medidas2)
    
    self.disp_ojo = DisplayOjo(lista_medidas1, inc_tiempo1, lista_medidas2, inc_tiempo2)
    self.disp_ojo.show()
    
    # Quitamos el disiparo externo
    self.osc.set_trigger('1', 0)
    
    #Quitamos los pines
    #pines.quitGPIO()
    

class DisplayOjo(QtGui.QWidget):
  
  def __init__(self, medidas1, tiempo1, medidas2, tiempo2):
    super(DisplayOjo, self).__init__()
    
    logging.basicConfig(level=logging.DEBUG) # Trazas para comprobar el correcto funcionamiento
    self.setWindowTitle('Diagrama de ojo')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    self.setFixedSize(900,700)
    tab_widget = QtGui.QTabWidget()
    tab1 = QtGui.QWidget()
    tab2 = QtGui.QWidget()
    
    p1 = QtGui.QVBoxLayout(tab1)
    p2 = QtGui.QVBoxLayout(tab2)
    
    tab_widget.addTab(tab1, "820 nm")
    tab_widget.addTab(tab2, "1300 nm")
    
    vbox = QtGui.QVBoxLayout()
    vbox.addWidget(tab_widget)
    
    # Hacemos las medidas disponibles a todo el objeto
    self.lista_medidas_t1 = medidas1
    self.lista_medidas_t2 = medidas2
    self.inc_tiempo_t1 = tiempo1
    self.inc_tiempo_t2 = tiempo2
    
    self.creaInterfaz(p1, p2)
    
    self.setLayout(vbox)
  
  def creaInterfaz(self, p1, p2):
    
    self.figure_t1 = plt.figure(1)
    self.canvas_t1 = FigureCanvas(self.figure_t1)
    self.canvas_t1.setParent(self)
    
    self.figure_t2 = plt.figure(2)
    self.canvas_t2 = FigureCanvas(self.figure_t2)
    self.canvas_t2.setParent(self)
    
    # Creamos los plots
    plt.figure(1)
    self.ax1_t1 = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
    self.ax2_t1 = plt.subplot2grid((2,2),(1,0))            #Histogramas
    self.ax3_t1 = plt.subplot2grid((2,2),(1,1))            #erfc
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)
    
    plt.figure(2)
    self.ax1_t2 = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
    self.ax2_t2 = plt.subplot2grid((2,2),(1,0))            #Histogramas
    self.ax3_t2 = plt.subplot2grid((2,2),(1,1))            #erfc
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)
    
    # Creamos los formatos que van a mostrar las unidades que se pintan
    formatter_tiempo = EngFormatter(unit='s', places=1)
    formatter_amp = EngFormatter(unit='v', places=1)
    self.lista_tiempo_t1 = []
    self.lista_tiempo_t2 = []
    
    # Sabemos la diferencia de tiempos entre medidas, asi que multiplicando la posicion
    # de cada dato por el incremento de tiempo sabemos su posicion en el eje X
    for i in range(len(self.lista_medidas_t1[1])):
      self.lista_tiempo_t1.append(self.inc_tiempo_t1*i)
    for i in range(len(self.lista_medidas_t2[1])):
      self.lista_tiempo_t2.append(self.inc_tiempo_t2*i)
    
    
    # Representamos el diagrama
    plt.figure(1)
    self.ax1_t1.hold(True)
    for i in range(len(self.lista_medidas_t1)):
      self.ax1_t1.plot(self.lista_tiempo_t1, self.lista_medidas_t1[i], '#0b610b')
    self.ax1_t1.hold(False)
    self.ax1_t1.set_xlabel('tiempo')
    self.ax1_t1.set_ylabel('amplitud')
    self.ax1_t1.xaxis.set_major_formatter(formatter_tiempo)
    self.ax1_t1.yaxis.set_major_formatter(formatter_amp)
    self.ax1_t1.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo_t1 * 25))
    self.ax1_t1.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    plt.figure(2)
    self.ax1_t2.hold(True)
    for i in range(len(self.lista_medidas_t2)):
      self.ax1_t2.plot(self.lista_tiempo_t2, self.lista_medidas_t2[i], '#0b610b')
    self.ax1_t2.hold(False)
    self.ax1_t2.set_xlabel('tiempo')
    self.ax1_t2.set_ylabel('amplitud')
    self.ax1_t2.xaxis.set_major_formatter(formatter_tiempo)
    self.ax1_t2.yaxis.set_major_formatter(formatter_amp)
    self.ax1_t2.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo_t2 * 25))
    self.ax1_t2.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    # Creamos las barras de muestreo y umbral
    plt.figure(1)
    self.intervalo_amplitud_t1 = self.ax1_t1.yaxis.get_data_interval()
    umbralInit_t1 = (self.intervalo_amplitud_t1[0]+self.intervalo_amplitud_t1[1])/2
    muestreoInit_t1 = self.lista_tiempo_t1[len(self.lista_tiempo_t1)-1]/2
    
    plt.figure(2)
    self.intervalo_amplitud_t2 = self.ax1_t2.yaxis.get_data_interval()
    umbralInit_t2 = (self.intervalo_amplitud_t2[0]+self.intervalo_amplitud_t2[1])/2
    muestreoInit_t2 = self.lista_tiempo_t2[len(self.lista_tiempo_t2)-1]/2
    
    # Pintamos la erfc
    eje_x = np.arange(0, 10, 0.5)
    plt.figure(1)
    self.ax3_t1.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    plt.figure(2)
    self.ax3_t2.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    
    logging.debug('se crea el eje semilogaritmico')
    
    plt.figure(1)
    self.ax3_t1.set_xlabel('q')
    self.ax3_t1.set_ylabel('BER')
    plt.figure(2)
    self.ax3_t2.set_xlabel('q')
    self.ax3_t2.set_ylabel('BER')
    
    # Creamos las barras horizontales y verticales de los subplots
    plt.figure(1)
    self.var_t1 = 25*self.inc_tiempo_t1
    self.barMuestreo_t1 = self.ax1_t1.axvline(linewidth=3, x=muestreoInit_t1, color='blue')
    self.barUmbral_t1 = self.ax1_t1.axhline(linewidth=3, y=umbralInit_t1, color='green')
    self.barDecision2_t1 = self.ax2_t1.axvline(x=umbralInit_t1, color='green')
    self.bar_q_t1 = self.ax3_t1.axvline(x=10, color='blue', linestyle='--') # Valor distinto de cero para el logaritmo
    self.bar_ber_t1 = self.ax3_t1.axhline(y=10, color='blue', linestyle='--')
    
    plt.figure(2)
    self.var_t2 = 25*self.inc_tiempo_t2
    self.barMuestreo_t2 = self.ax1_t2.axvline(linewidth=3, x=muestreoInit_t2, color='blue')
    self.barUmbral_t2 = self.ax1_t2.axhline(linewidth=3, y=umbralInit_t2, color='green')
    self.barDecision2_t2 = self.ax2_t2.axvline(x=umbralInit_t2, color='green')
    self.bar_q_t2 = self.ax3_t2.axvline(x=10, color='blue', linestyle='--') # Valor distinto de cero para el logaritmo
    self.bar_ber_t2 = self.ax3_t2.axhline(y=10, color='blue', linestyle='--')
    
    # Creamos la fuente que se va a usar
    font = QtGui.QFont()
    font.setFamily(QtCore.QString.fromUtf8("Helvetica"))
    font.setPixelSize(17)
    
    # Esto hay que hacerlo antes de dibujar para que pueda poner los valores medios, q y la ber
    self.resultados_label_t1 = QtGui.QLabel(self)
    self.resultados_label_t2 = QtGui.QLabel(self)
    self.resultados_label_t1.setFont(font)
    self.resultados_label_t2.setFont(font)
    
    # Pintamos el resto de subplots
    self.dibuja_t1(muestreoInit_t1, umbralInit_t1)
    self.dibuja_t2(muestreoInit_t2, umbralInit_t2)
    
    # Barra de herramientas de matplotlib
    plt.figure(1)
    self.mpl_toolbar_t1 = NavigationToolbar(self.canvas_t1, self)
    plt.figure(2)
    self.mpl_toolbar_t2 = NavigationToolbar(self.canvas_t2, self)
    
    p1.addWidget(self.canvas_t1)
    p1.addWidget(self.mpl_toolbar_t1)
    p1.addWidget(self.resultados_label_t1)
    
    p2.addWidget(self.canvas_t2)
    p2.addWidget(self.mpl_toolbar_t2)
    p2.addWidget(self.resultados_label_t2)
    
    self.cid_t1 = self.figure_t1.canvas.mpl_connect('button_press_event', self.on_press_t1)
    self.cid_t2 = self.figure_t2.canvas.mpl_connect('button_press_event', self.on_press_t2)
  
  def on_press_t1(self, event):
    valMuestreo = event.xdata
    valUmbral = event.ydata
    
    if (valMuestreo < 0) or (valMuestreo > self.lista_tiempo_t1[len(self.lista_tiempo_t1)-1]):
      valMuestreo = self.lista_tiempo_t1[750]
    if (valUmbral < self.intervalo_amplitud_t1[0]) or (valUmbral > self.intervalo_amplitud_t1[1]):
      valUmbral = (self.intervalo_amplitud_t1[0] + self.intervalo_amplitud_t1[1]) / 2
    
    logging.debug('muestreo %s umbral %s', str(valMuestreo), str(valUmbral))    
    self.dibuja_t1(valMuestreo, valUmbral)
  
  def on_press_t2(self, event):
    valMuestreo = event.xdata
    valUmbral = event.ydata
    
    if (valMuestreo < 0) or (valMuestreo > self.lista_tiempo_t2[len(self.lista_tiempo_t2)-1]):
      valMuestreo = self.lista_tiempo_t2[750]
    if (valUmbral < self.intervalo_amplitud_t2[0]) or (valUmbral > self.intervalo_amplitud_t2[1]):
      valUmbral = (self.intervalo_amplitud_t2[0] + self.intervalo_amplitud_t2[1]) / 2
    
    logging.debug('muestreo %s umbral %s', str(valMuestreo), str(valUmbral))    
    self.dibuja_t2(valMuestreo, valUmbral)
    
  def dibuja_t1(self, muestreo, umbral):
    plt.figure(1)
    logging.debug('entramos en dibuja')
    puntoMuestreo = int(muestreo/self.inc_tiempo_t1)
    amp = []
    
    for i in range(len(self.lista_medidas_t1)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
      for j in range(-25, 25):
        try:
          amp.append(self.lista_medidas_t1[i][puntoMuestreo + j])
        except IndexError:
          logging.debug('oob')
    
    # Discriminamos segun el umbral
    val0 = []
    val1 = []
    
    for i in range(len(amp)):
      if(amp[i] < umbral):
        val0.append(amp[i])
      else:
        val1.append(amp[i])
    
    # Pintamos los histogramas y las gaussianas
    self.ax2_t1.cla()
    self.ax2_t1.set_xlabel('amplitud')
    norm0, bins, patches = self.ax2_t1.hist(val0, bins=200,range=[(5/4)*self.intervalo_amplitud_t1[0], (5/4)*self.intervalo_amplitud_t1[1]], normed=True, histtype='step', color='#8181f7', rwidth=100)
    
    norm1, bins, patches = self.ax2_t1.hist(val1, bins=200,range=[(5/4)*self.intervalo_amplitud_t1[0], (5/4)*self.intervalo_amplitud_t1[1]], normed=True, histtype='step', color='#fa5858', rwidth=100)
    
    v0, sigma0 = self.media_y_varianza(val0)
    gauss0 = pylab.normpdf(bins, v0, sigma0)
    self.ax2_t1.plot(bins, gauss0, linewidth=2, color='#0404b4')#azul
    
    v1, sigma1 = self.media_y_varianza(val1)
    gauss1 = pylab.normpdf(bins, v1, sigma1)
    self.ax2_t1.plot(bins, gauss1, linewidth=2, color='#b40404')#rojo
    
    # Calculamos la ber
    q = math.fabs(v1-v0)/(sigma1+sigma0)
    ber = 0.5*erfc(q/math.sqrt(2))
    
    self.muestra_resultados_t1(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
    
    # Recolocamos todas las barras
    self.ax2_t1.add_line(self.barDecision2_t1) # Vuelve a pintar la barra del umbral cuando se redibuja
    self.ax3_t1.add_line(self.bar_q_t1)
    self.ax3_t1.add_line(self.bar_ber_t1)
    self.barMuestreo_t1.set_xdata(muestreo)
    self.barUmbral_t1.set_ydata(umbral)
    self.barDecision2_t1.set_xdata(umbral)
    logging.debug('colocamos las barras en ax3')
    self.bar_q_t1.set_xdata(q)
    self.bar_ber_t1.set_ydata(ber)
    logging.debug('colocadas')
    
    self.canvas_t1.draw()
    logging.debug('ya se ha redibujado')
  
  def dibuja_t2(self, muestreo, umbral):
    logging.debug('entramos en dibuja')
    plt.figure(2)
    puntoMuestreo = int(muestreo/self.inc_tiempo_t2)
    amp = []
    
    for i in range(len(self.lista_medidas_t2)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
      for j in range(-25, 25):
        try:
          amp.append(self.lista_medidas_t2[i][puntoMuestreo + j])
        except IndexError:
          logging.debug('oob')
    
    # Discriminamos segun el umbral
    val0 = []
    val1 = []
    
    for i in range(len(amp)):
      if(amp[i] < umbral):
        val0.append(amp[i])
      else:
        val1.append(amp[i])
    
    # Pintamos los histogramas y las gaussianas
    self.ax2_t2.cla()
    self.ax2_t2.set_xlabel('amplitud')
    norm0, bins, patches = self.ax2_t2.hist(val0, bins=200,range=[(5/4)*self.intervalo_amplitud_t2[0], (5/4)*self.intervalo_amplitud_t2[1]], normed=True, histtype='step', color='#8181f7', rwidth=100)
    
    norm1, bins, patches = self.ax2_t2.hist(val1, bins=200,range=[(5/4)*self.intervalo_amplitud_t2[0], (5/4)*self.intervalo_amplitud_t2[1]], normed=True, histtype='step', color='#fa5858', rwidth=100)
    
    v0, sigma0 = self.media_y_varianza(val0)
    gauss0 = pylab.normpdf(bins, v0, sigma0)
    self.ax2_t2.plot(bins, gauss0, linewidth=2, color='#0404b4')#azul
    
    v1, sigma1 = self.media_y_varianza(val1)
    gauss1 = pylab.normpdf(bins, v1, sigma1)
    self.ax2_t2.plot(bins, gauss1, linewidth=2, color='#b40404')#rojo
    
    # Calculamos la ber
    q = math.fabs(v1-v0)/(sigma1+sigma0)
    ber = 0.5*erfc(q/math.sqrt(2))
    
    self.muestra_resultados_t2(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
    
    # Recolocamos todas las barras
    self.ax2_t2.add_line(self.barDecision2_t2) # Vuelve a pintar la barra del umbral cuando se redibuja
    self.ax3_t2.add_line(self.bar_q_t2)
    self.ax3_t2.add_line(self.bar_ber_t2)
    self.barMuestreo_t2.set_xdata(muestreo)
    self.barUmbral_t2.set_ydata(umbral)
    self.barDecision2_t2.set_xdata(umbral)
    logging.debug('colocamos las barras en ax3')
    self.bar_q_t2.set_xdata(q)
    self.bar_ber_t2.set_ydata(ber)
    logging.debug('colocadas')
    
    self.canvas_t2.draw()
    logging.debug('ya se ha redibujado')
  
  def muestra_resultados_t1(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
    string = '\tv0: %-*s Sigma 0: %-*s N. muestras 0: %-*s Q: %-*s \n\n\tv1: %-*s Sigma 1: %-*s N. muestras 1: %-*s BER: %.2e' % (17, str(round(v0*1000,1))+' mV', 17, str(round(sigma0*1000,1))+' mV', 17, str(num0), 17, str(round(q,2)), 17, str(round(v1*1000,1))+' mV', 17, str(round(sigma1*1000,1))+' mV', 17, str(num1), ber)
    plt.figure(1)
    self.resultados_label_t1.setText(string)
  
  def muestra_resultados_t2(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
    string = '\tv0: %-*s Sigma 0: %-*s N. muestras 0: %-*s Q: %-*s \n\n\tv1: %-*s Sigma 1: %-*s N. muestras 1: %-*s BER: %.2e' % (17, str(round(v0*1000,1))+' mV', 17, str(round(sigma0*1000,1))+' mV', 17, str(num0), 17, str(round(q,2)), 17, str(round(v1*1000,1))+' mV', 17, str(round(sigma1*1000,1))+' mV', 17, str(num1), ber)
    plt.figure(2)
    self.resultados_label_t2.setText(string)
  
  def media_y_varianza(self, data): 
    media = 0.0
    var = 0.0
    n = len(data)
    for i in range(n):
      media = media + data[i]
    media = media/n
    for i in range(n):
      var = var + math.pow(media - data[i], 2)
    var = math.sqrt(var / (n-1))
    return media, var

class VentanaConfigIO(QtGui.QWidget):
  
  def __init__(self):
    super(VentanaConfigIO, self).__init__()
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_rate1 = QtGui.QLabel('Rate 1')
    tit_rate2 = QtGui.QLabel('Rate 2')
    tit_len1 = QtGui.QLabel('Length 1')
    tit_len2 = QtGui.QLabel('Length 2')
    tit_sync = QtGui.QLabel('Sync')
    
    tasas = ["10 Mbps","30 Mbps","70 Mbps","125 Mbps"]
    longitudes = ["4", "8", "12", "16"]
    
    combo_rate1 = QtGui.QComboBox(self)
    combo_rate2 = QtGui.QComboBox(self)
    combo_len1 = QtGui.QComboBox(self)
    combo_len2 = QtGui.QComboBox(self)
    combo_sync = QtGui.QComboBox(self)
    
    for t in tasas:
      combo_rate1.addItem(t)
      combo_rate2.addItem(t)
    
    for l in longitudes:
      combo_len1.addItem(l)
      combo_len2.addItem(l)
    
    combo_sync.addItem('sync 1')
    combo_sync.addItem('sync 2')
    combo_sync.addItem('SoF 1')
    combo_sync.addItem('SoF 2')
    
    bot_aceptar = QtGui.QPushButton('Aceptar', self)
    
    grid.addWidget(tit_rate1, 1, 1)
    grid.addWidget(combo_rate1, 1, 2)
    grid.addWidget(tit_len1, 1, 3)
    grid.addWidget(combo_len1, 1, 4)
    
    grid.addWidget(tit_rate2, 2, 1)
    grid.addWidget(combo_rate2, 2, 2)
    grid.addWidget(tit_len2, 2, 3)
    grid.addWidget(combo_len2, 2, 4)
    
    grid.addWidget(tit_sync, 3, 2)
    grid.addWidget(combo_sync, 3, 3)
    grid.addWidget(bot_aceptar, 3, 5)
    
    bot_aceptar.clicked.connect(lambda: self.aceptar(combo_rate1.currentText(), combo_rate2.currentText(), combo_len1.currentText(), combo_len2.currentText(), combo_sync.currentText()))
    
    self.setLayout(grid)
    self.setWindowTitle('Configuracion del generador')
    self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/lab_master/img/icono.gif'))
    self.setFixedSize(420, 130)
    self.show()
    
  def aceptar(self, rate1, rate2, len1, len2, sync):
    length = {"4":0, "8":1, "12":2, "16":3}
    rate = {"10 Mbps":0, "30 Mbps":1, "70 Mbps":2, "125 Mbps":3}
    syn = {'sync 1':1, 'sync 2':2, 'SoF 1':3, 'SoF 2':4}
    
    pines = PinesFPGA()
    pines.setClock(syn[str(sync)])
    pines.setLength1(length[str(len1)])
    pines.setRate1(rate[str(rate1)])
    pines.setLength2(length[str(len2)])
    pines.setRate2(rate[str(rate2)])

