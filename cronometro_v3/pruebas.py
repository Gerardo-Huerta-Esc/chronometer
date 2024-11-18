from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
import sys
import time

class Cronometro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cronómetro")
        self.setGeometry(200, 400, 300, 150)

        # Crear layouts
        mainLayout = QHBoxLayout()  # Layout principal horizontal
        leftLayout = QVBoxLayout()  # Layout vertical para los elementos existentes
        rightLayout = QVBoxLayout()  # Layout vertical para la nueva sección

        # Caja de texto para el tiempo
        self.tiempo = QLineEdit(self)
        self.tiempo.setAlignment(Qt.AlignRight)
        self.tiempo.setReadOnly(True)
        self.tiempo.setStyleSheet("font-size: 20px; background-color: black; color: #03f943;")
        self.tiempo.setFixedWidth(200)  # Reducir el tamaño de la pantalla de tiempo

        self.pantalla_hora = QLineEdit(self)
        self.botonStart = QPushButton("Start", self)
        self.botonStart.clicked.connect(self.start_cronometro)
        self.botonStop = QPushButton("Stop", self)
        self.botonStop.clicked.connect(self.stop_cronometro)
        self.botonValidar = QPushButton("Validar", self)
        self.botonValidar.clicked.connect(self.validar_cronometro)

        # Botón para expandir la ventana
        self.expandirBtn = QPushButton(self)
        self.expandirBtn.setFixedSize(20, 20)  # Hacer el botón lo más pequeño posible
        self.expandirBtn.clicked.connect(self.expandirVentana)

        # Añadir la caja de texto y el botón al layout horizontal
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.tiempo)
        hLayout.addWidget(self.expandirBtn)

        leftLayout.addLayout(hLayout)
        leftLayout.addWidget(self.pantalla_hora)
        leftLayout.addWidget(self.botonStart)
        leftLayout.addWidget(self.botonStop)
        leftLayout.addWidget(self.botonValidar)

        # Sección extra que se va a expandir
        self.nuevaSeccion = QLineEdit(self)
        self.nuevaSeccion.setAlignment(Qt.AlignRight)
        self.nuevaSeccion.setReadOnly(True)
        self.nuevaSeccion.setStyleSheet("font-size: 24px; background-color: black; color: #03f943;")
        self.nuevaSeccion.setVisible(False)  # Inicialmente invisible

        rightLayout.addWidget(self.nuevaSeccion)  # Añadir nueva sección al layout vertical de la derecha

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.tiempo_inicial = None
        self.tiempo_pausado = 0
        self.cronometro_activo = False

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
        tiempo_segundos = self.convertir_a_segundos(tiempo_ingresado)
        self.tiempo_inicial = time.time() - tiempo_segundos
        self.tiempo_pausado = tiempo_segundos
        self.tiempo.setText(self.obtener_tiempo_formateado(tiempo_segundos))

    def actualizar_cronometro(self):
        if self.cronometro_activo:
            tiempo_actual = time.time() - self.tiempo_inicial
            self.tiempo.setText(self.obtener_tiempo_formateado(int(tiempo_actual)))
            QTimer.singleShot(1000, self.actualizar_cronometro)

    def obtener_tiempo_formateado(self, tiempo_segundos):
        horas, resto = divmod(tiempo_segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    def convertir_a_segundos(self, hora_str):
        try:
            horas, minutos, segundos = map(int, hora_str.split(":"))
            return horas * 3600 + minutos * 60 + segundos
        except ValueError:
            return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Cronometro()
    ventana.show()
    sys.exit(app.exec_())










