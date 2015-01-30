import sys
from PyQt4 import QtGui, QtCore
from Osciloscopio import *
#from Modbus import *
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
    win.setInformativeText(texto)
    win.setWindowTitle('Aviso')
    #win.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    win.exec_()

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
    
    grid = QtGui.QGridLayout()
    grid.setSpacing(5)
    
    tit_up = QtGui.QLabel('Uplink')
    tit_dw = QtGui.QLabel('Downlink')
    tit_tasa_u = QtGui.QLabel('Tasa binaria')
    tit_tasa_d = QtGui.QLabel('Tasa binaria')
    tit_long_u = QtGui.QLabel('Longitud de trama')
    tit_long_d = QtGui.QLabel('Longitud de trama')
    tit_lambda_u = QtGui.QLabel('Longitud de onda')
    tit_lambda_d = QtGui.QLabel('Longitud de onda')
    
    desp_tasa_u = QtGui.QComboBox(self)
    desp_tasa_d = QtGui.QComboBox(self)
    desp_long_u = QtGui.QComboBox(self)
    desp_long_d = QtGui.QComboBox(self)
    desp_lambda_u = QtGui.QComboBox(self)
    desp_lambda_d = QtGui.QComboBox(self)
    
    tasas = ["5 Mbps","20 Mbps","70 Mbps","150 Mbps"]
    longitudes = ["4", "8", "12", "16"]
    lambdas = ["850","1300","1550"]
    
    for t in tasas:
      desp_tasa_u.addItem(t)
      desp_tasa_d.addItem(t)
    for l in longitudes:
      desp_long_u.addItem(l)
      desp_long_d.addItem(l)
    for l in lambdas:
      desp_lambda_u.addItem(l)
      desp_lambda_d.addItem(l)
    
    bot_aceptar = QtGui.QPushButton('Aceptar', self)
    
    grid.addWidget(tit_up, 0, 1)
    grid.addWidget(tit_dw, 0, 4)
    grid.addWidget(tit_tasa_u, 2, 1)
    grid.addWidget(tit_tasa_d, 2, 4)
    grid.addWidget(tit_long_u, 3, 1)
    grid.addWidget(tit_long_d, 3, 4)
    grid.addWidget(tit_lambda_u, 4, 1)
    grid.addWidget(tit_lambda_d, 4, 4)
    grid.addWidget(desp_tasa_u, 2, 2)
    grid.addWidget(desp_tasa_d, 2, 5)
    grid.addWidget(desp_long_u, 3, 2)
    grid.addWidget(desp_long_d, 3, 5)
    grid.addWidget(desp_lambda_u, 4, 2)
    grid.addWidget(desp_lambda_d, 4, 5)
    grid.addWidget(bot_aceptar, 5, 3)
    
    bot_aceptar.clicked.connect(lambda: self.aceptar(desp_tasa_u.currentText(), desp_long_u.currentText(), desp_lambda_u.currentText(), desp_tasa_d.currentText(), desp_long_d.currentText(), desp_lambda_d.currentText()))
    
    self.setLayout(grid)
    #self.setGeometry(100, 100, 500, 500)
    self.setWindowTitle('FTTH')
    #self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.show()
    
  def aceptar(self, tasa_u, long_u, lambda_u, tasa_d, long_d, lambda_d):
    # Diccionarios
    base_tiempos = {"5 Mbps":'25ns', "20 Mbps":'10ns', "70 Mbps":'5ns', "150 Mbps":'2.5ns'}
    
    self.osc.set_horizontal(base_tiempos[str(tasa_u)]) #Por los qstring de qt4
    self.osc.set_vertical("1", "500mv", "DC", "1")
    
    # Configuramos el disparo
    self.osc.set_trigger('ext', 0)
    aviso = VentanaInfo('La adquisicion de datos puede tardar un tiempo.\nPulse el boton "Ok" y espere, por favor.')
    lista_medidas = []
    
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      medidas , inc_tiempo = self.osc.get_data('1', 500, 2000, '1')
      lista_medidas.append(medidas)
    
    self.ojo1 = DisplayOjo(lista_medidas, inc_tiempo, "Enlace ascendente")
    self.ojo1.show()
    
    self.osc.set_horizontal(base_tiempos[str(tasa_d)]) #Por los qstring de qt4
    #self.osc.set_vertical("2", "500mv", "DC", "1")
    
    lista_medidas = []
    # Toma 32 trazas del osciloscopio
    for i in range(32):
      medidas , inc_tiempo = self.osc.get_data('2', 500, 2000, '1')
      lista_medidas.append(medidas)
    
    self.ojo2 = DisplayOjo(lista_medidas, inc_tiempo, "Enlace descendente")
    self.ojo2.show()
    
    # Quitamos el disiparo externo
    self.osc.set_trigger('1', 0)
    #print(str(tasa_u), str(long_u), str(lambda_u))
    

class DisplayOjo(QtGui.QWidget):
  
  def __init__(self, medidas, tiempo, num):
    super(DisplayOjo, self).__init__()
    
    logging.basicConfig(level=logging.DEBUG) # Trazas para comprobar el correcto funcionamiento
    self.setWindowTitle('Diagrama de ojo %s' %num)
    #self.setWindowIcon(QtGui.QIcon('/home/debian/Desktop/Aplicacion/img/icono.gif'))
    self.setFixedSize(900,700)
    
    self.creaInterfaz(medidas, tiempo)
  
  def creaInterfaz(self, medidas, tiempo):
    
    self.figure = plt.figure()
    self.canvas = FigureCanvas(self.figure)
    self.canvas.setParent(self)
    
    # Creamos los plots
    self.ax = plt.subplot2grid((2,2),(0,0), colspan=2) #Diagrama de ojo
    self.ax2 = plt.subplot2grid((2,2),(1,0))           #Histogramas
    self.ax3 = plt.subplot2grid((2,2),(1,1))           #erfc
    plt.subplots_adjust(left=0.15, right=0.85, bottom=0.1, top=0.9, hspace=0.25)
    
    # Hacemos las medidas disponibles para todo el objeto
    self.lista_medidas = medidas
    self.inc_tiempo = tiempo
    
    # Creamos los formatos que van a mostrar las unidades que se pintan
    formatter_tiempo = EngFormatter(unit='s', places=1)
    formatter_amp = EngFormatter(unit='v', places=1)
    self.lista_tiempo = []
    
    # Sabemos la diferencia de tiempos entre medidas, asi que multiplicando la posicion
    # de cada dato por el incremento de tiempo sabemos su posicion en el eje X
    for i in range(len(self.lista_medidas[1])):
      self.lista_tiempo.append(self.inc_tiempo*i)
    
    # Representamos el diagrama
    self.ax.hold(True)
    for i in range(len(self.lista_medidas)):
      self.ax.plot(self.lista_tiempo, self.lista_medidas[i], 'y')
    self.ax.hold(False)
    self.ax.set_xlabel('tiempo')
    self.ax.set_ylabel('amplitud')
    self.ax.xaxis.set_major_formatter(formatter_tiempo)
    self.ax.yaxis.set_major_formatter(formatter_amp)
    self.ax.xaxis.set_minor_locator(MultipleLocator(self.inc_tiempo * 25))
    self.ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    
    # Creamos las barras de muestreo y umbral
    self.intervalo_amplitud = self.ax.yaxis.get_data_interval()
    umbralInit = (self.intervalo_amplitud[0]+self.intervalo_amplitud[1])/2
    muestreoInit = self.lista_tiempo[len(self.lista_tiempo)-1]/2
    
    # Pintamos la erfc
    eje_x = np.arange(0, 10, 0.5)
    self.ax3.semilogy(eje_x, 0.5*erfc(eje_x/math.sqrt(2)), color='#08088a')
    
    logging.debug('se crea el eje semilogaritmico')
    
    self.ax3.set_xlabel('q')
    self.ax3.set_ylabel('BER')
    
    # Creamos las barras horizontales y verticales de los subplots
    self.var = 25*self.inc_tiempo
    self.barMuestreo = self.ax.axvline(x=muestreoInit, color='green')
    self.barMuestreoMas = self.ax.axvline(x=muestreoInit + self.var, color='green', linestyle='--')
    self.barMuestreoMenos = self.ax.axvline(x=muestreoInit - self.var, color='green', linestyle='--')
    self.barUmbral = self.ax.axhline(y=umbralInit, color='blue')
    self.barDecision2 = self.ax2.axvline(x=umbralInit, color='blue')
    self.bar_q = self.ax3.axvline(x=10, color='blue') # Valor distinto de cero para el logaritmo
    self.bar_ber = self.ax3.axhline(y=10, color='blue')
    
    # Esto hay que hacerlo antes de dibujar para que pueda poner los valores medios, q y la ber
    self.resultados_label = QtGui.QLabel(self)
    
    # Pintamos el resto de subplots
    self.dibuja(muestreoInit, umbralInit)
    
    # Barra de herramientas de matplotlib
    self.mpl_toolbar = NavigationToolbar(self.canvas, self)
    
    self.box1 = QtGui.QLineEdit(self)
    self.box2 = QtGui.QLineEdit(self)
    self.muestreo_label = QtGui.QLabel('Punto de muestreo', self)
    self.umbral_label = QtGui.QLabel('Umbral', self)
    
    self.boton = QtGui.QPushButton("Pintar", self)
    self.connect(self.boton, QtCore.SIGNAL('clicked()'), self.botonClick)
    
    hbox = QtGui.QHBoxLayout()
    
    for w in [self.muestreo_label, self.box1, self.umbral_label, self.box2, self.boton]:
      hbox.addWidget(w)
      hbox.setAlignment(w, QtCore.Qt.AlignVCenter)
    
    vbox = QtGui.QVBoxLayout()
    vbox.addWidget(self.canvas)
    vbox.addWidget(self.mpl_toolbar)
    vbox.addWidget(self.resultados_label)
    vbox.addLayout(hbox)
    
    self.setLayout(vbox)
    
  
  def botonClick(self):
    logging.debug('entramos en la rutina botonclick')
    muestreo = int(self.box1.text()) # Cogemos los valores de los porcentajes como enteros de las cajas de texto
    umbral = int(self.box2.text())
    
    if muestreo > 100: # Nos aseguramos de que estan entre cero y cien
      muestreo = 100
    if muestreo < 0:
      muestreo = 0
    muestreo = muestreo/100.0 # Los ponemos en tanto por uno y los convertimos a decimales
    
    if umbral > 100: # Nos aseguramos de que estan entre cero y cien
      umbral = 100
    if umbral < 0:
      umbral = 0
    umbral = umbral/100.0 # Los ponemos en tanto por uno y los convertimos a decimales
    
    # Calculamos con que valores corresponden los porcentajes
    valMuestreo = (muestreo*self.lista_tiempo[len(self.lista_tiempo)-1])
    valUmbral = ((self.intervalo_amplitud[1] - self.intervalo_amplitud[0]) * umbral) + self.intervalo_amplitud[0]
    logging.debug('muestreo %s umbral %s', str(valMuestreo), str(valUmbral))    
    self.dibuja(valMuestreo, valUmbral)
  
  def dibuja(self, muestreo, umbral):
    logging.debug('entramos en dibuja')
    puntoMuestreo = int(muestreo/self.inc_tiempo)
    amp = []
    
    for i in range(len(self.lista_medidas)): # Guardamos los puntos entre mas y menos 25 posiciones del punto de muestreo de todas las tramas guardadas
      for j in range(-25, 25):
        try:
          amp.append(self.lista_medidas[i][puntoMuestreo + j])
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
    self.ax2.cla()
    self.ax2.set_xlabel('amplitud')
    norm0, bins, patches = self.ax2.hist(val0, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#ced8f6', rwidth=100)
    
    norm1, bins, patches = self.ax2.hist(val1, bins=200,range=[(5/4)*self.intervalo_amplitud[0], (5/4)*self.intervalo_amplitud[1]], normed=True, histtype='stepfilled', color='#f5a9a9', rwidth=100)
    
    v0, sigma0 = self.media_y_varianza(val0)
    gauss0 = pylab.normpdf(bins, v0, sigma0)
    self.ax2.plot(bins, gauss0, linewidth=2, color='#08088a')#azul
    
    v1, sigma1 = self.media_y_varianza(val1)
    gauss1 = pylab.normpdf(bins, v1, sigma1)
    self.ax2.plot(bins, gauss1, linewidth=2, color='#8a0808')#rojo
    
    # Calculamos la ber
    q = math.fabs(v1-v0)/(sigma1+sigma0)
    ber = 0.5*erfc(q/math.sqrt(2))
    
    self.muestra_resultados(v0, sigma0, v1, sigma1, q, ber, len(val0), len(val1))
    
    # Recolocamos todas las barras
    self.ax2.add_line(self.barDecision2) # Vuelve a pintar la barra del umbral cuando se redibuja
    self.ax3.add_line(self.bar_q)
    self.ax3.add_line(self.bar_ber)
    self.barMuestreo.set_xdata(muestreo)
    self.barMuestreoMas.set_xdata(muestreo + self.var)
    self.barMuestreoMenos.set_xdata(muestreo - self.var)
    self.barUmbral.set_ydata(umbral)
    self.barDecision2.set_xdata(umbral)
    logging.debug('colocamos las barras en ax3')
    self.bar_q.set_xdata(q)
    self.bar_ber.set_ydata(ber)
    logging.debug('colocadas')
    
    self.canvas.draw()
    logging.debug('ya se ha redibujado')
  
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
  
  def muestra_resultados(self, v0, sigma0, v1, sigma1, q, ber, num0, num1):
    string = 'v0: ' + str(round(v0,3)) + '\tsigma0: ' + str(round(sigma0,3)) + '\tnumero de muestras0: ' + str(num0) + '\tQ: ' + str(round(q,2)) + '\n\n' + 'v1: ' + str(round(v1,3)) + '\tsigma1: ' + str(round(sigma1,3)) + '\tnumero de muestras1: ' + str(num1) + '\tBER: ' + '%.2e' % ber # se muestra la ber en notacion cientifica
    self.resultados_label.setText(string)


