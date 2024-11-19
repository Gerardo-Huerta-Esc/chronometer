from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
import sys
import time

class Cronometro(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cronómetro")
        self.setGeometry(200, 200, 300, 150)

        self.milisegundos = QLineEdit(self)
        self.milisegundos.setAlignment(Qt.AlignRight)
        self.milisegundos.setReadOnly(True)
        self.milisegundos.setStyleSheet("font-size: 24px; background-color: black; color: #03f943;")

        self.pantalla_hora = QLineEdit(self)

        self.botonStart = QPushButton("Start", self)
        self.botonStart.clicked.connect(self.start_cronometro)
        self.botonStop = QPushButton("Stop", self)
        self.botonStop.clicked.connect(self.stop_cronometro)
        self.botonValidar = QPushButton("Validar", self)
        self.botonValidar.clicked.connect(self.validar_cronometro)

        layout = QVBoxLayout()
        layout.addWidget(self.milisegundos)
        layout.addWidget(self.pantalla_hora)
        layout.addWidget(self.botonStart)
        layout.addWidget(self.botonStop)
        layout.addWidget(self.botonValidar)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.tiempo_inicial = None
        self.tiempo_pausado = 0
        self.cronometro_activo = False

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





