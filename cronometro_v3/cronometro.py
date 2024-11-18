from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import sys
import time

class Cronometro(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cronómetro") #nombre de la ventana
        self.setGeometry(200, 400, 300, 150) # lugar geométrico en donde aparece la ventana al abrirse
 
        # crear layouts
        hLayout = QHBoxLayout() # (layout horizontal): Este layout es el de la ventana expandible
        layout = QVBoxLayout() # (layout vertical): Este layout es el de la ventana principal


        # caja de texto para los milisegundos
        self.milisegundos = QLineEdit(self) # caja de texto. El self indica que el widget es parte de la ventana principal de la aplicación.
        self.milisegundos.setAlignment(Qt.AlignRight) #Establece la alineación de los números hacia la derecha.
        self.milisegundos.setReadOnly(True) # Hace que la caja de texto sea de solo lectura
        self.milisegundos.setStyleSheet("font-size: 24px; background-color: black; color: #03f943;") #Aplica un estilo personalizado a la caja de texto usando CSS


        self.pantalla_hora = QLineEdit(self)
        self.botonStart = QPushButton("Start", self)
        self.botonStart.clicked.connect(self.start_cronometro)
        self.botonStop = QPushButton("Stop", self)
        self.botonStop.clicked.connect(self.stop_cronometro)
        self.botonValidar = QPushButton("Validar", self)
        self.botonValidar.clicked.connect(self.validar_cronometro)


#-----------------------------------------------------------------------------------------1
        # Botón para expandir la ventana
        self.expandirBtn = QPushButton("Expandir", self)
        self.expandirBtn.clicked.connect(self.expandirVentana)  # Conectar al evento de clic

        # Añadir la caja de texto y el botón al layout horizontal
        hLayout.addWidget(self.milisegundos)
        hLayout.addWidget(self.expandirBtn)
       
       
       

        # Sección extra que se va a expandir
        self.nuevaSeccion = QLineEdit(self)
        self.nuevaSeccion.setAlignment(Qt.AlignRight)
        self.nuevaSeccion.setReadOnly(True)
        self.nuevaSeccion.setStyleSheet("font-size: 24px; background-color: black; color: #03f943;")
        self.nuevaSeccion.setVisible(False)  # Inicialmente invisible

        layout.addLayout(hLayout) # Añadir el layout horizontal al layout principal

#----------------------------------------------------------------------------------------1

        #layout.addWidget(self.milisegundos) # en teoría, como esta ya esta en el layout horizontal, no debería estar aquí en el vertical?
        layout.addWidget(self.pantalla_hora) # es el campo donde se ingresa la hora
        layout.addWidget(self.botonStart)
        layout.addWidget(self.botonStop)
        layout.addWidget(self.botonValidar)
#---------------------------------------------------------------------------------------2  
        hLayout.addWidget(self.expandirBtn)                                             
        hLayout.addWidget(self.nuevaSeccion)  # Añadir nueva sección
#---------------------------------------------------------------------------------------2  

        widget = QWidget()
        widget.setLayout(layout) # de gpt: self.setLayout(layout) no se si eso haga diferiencia pero tengo ya una linea que se parece.
        self.setCentralWidget(widget)

        self.tiempo_inicial = None
        self.tiempo_pausado = 0
        self.cronometro_activo = False
        

#---------------------------------------------------------------------------------------3

    # Si la sección está visible, se oculta y se reduce el tamaño de la ventana. Si está oculta, se muestra y se expande el tamaño de la ventana.
    def expandirVentana(self):
        # Verificar si la sección está visible
        if self.nuevaSeccion.isVisible():
            # Si la sección está visible, ocultarla y reducir el tamaño de la ventana
            self.nuevaSeccion.setVisible(False)
            self.resize(300, 150)  # Tamaño original de la ventana
        else:
            # Si la sección está oculta, mostrarla y expandir el tamaño de la ventana
            self.nuevaSeccion.setVisible(True)
            self.resize(500, 150)  # Tamaño expandido de la ventana

#---------------------------------------------------------------------------------------3




    def start_cronometro(self):
        if not self.cronometro_activo:
            self.tiempo_inicial = time.time() - self.tiempo_pausado
            self.cronometro_activo = True
            self.actualizar_cronometro()

    def stop_cronometro(self):
        if self.cronometro_activo:
            self.cronometro_activo = False
            self.tiempo_pausado = time.time() - self.tiempo_inicial

    def validar_cronometro(self):
        tiempo_ingresado = self.pantalla_hora.text()
        tiempo_ms = self.convertir_a_milisegundos(tiempo_ingresado)
        self.tiempo_inicial = time.time() - tiempo_ms / 1000
        self.tiempo_pausado = tiempo_ms / 1000
        self.milisegundos.setText(f"Time: {self.obtener_tiempo_formateado(tiempo_ms)}")

    def actualizar_cronometro(self):
        if self.cronometro_activo:
            tiempo_actual = time.time() - self.tiempo_inicial
            milisegundos = int(tiempo_actual * 1000)
            self.milisegundos.setText(f"Time: {self.obtener_tiempo_formateado(milisegundos)}")
            QTimer.singleShot(1, self.actualizar_cronometro)

    def obtener_tiempo_formateado(self, tiempo_ms):
        horas, ms_restantes = divmod(tiempo_ms, 3600000)
        minutos, ms_restantes = divmod(ms_restantes, 60000)
        segundos, milisegundos = divmod(ms_restantes, 1000)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}.{milisegundos:02d}"

    def convertir_a_milisegundos(self, hora_str):
        try:
            horas, minutos, segundos = map(int, hora_str.split(":"))
            return (horas * 3600 + minutos * 60 + segundos) * 1000
        except ValueError:
            return 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Cronometro()
    ventana.show()
    sys.exit(app.exec_())
