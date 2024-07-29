
# codigo fucional. Pero se debe modificar la parte de que haga un solo registro por dia  
# y que luego los sume cada dia y lo muestre en la pantalla del lado derecho

import json
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
import sys
import time
import datetime

class Cronometro(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Cronómetro")
        self.setGeometry(200, 200, 600, 150)

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

        self.ultima_vez_label = QLabel(self)
        self.ultima_vez_label.setStyleSheet("font-size: 20px; color: green;")

        self.total_horas_label = QLabel(self)
        self.total_horas_label.setStyleSheet("font-size: 12px; color: red;")

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.milisegundos)
        left_layout.addWidget(self.pantalla_hora)
        left_layout.addWidget(self.botonStart)
        left_layout.addWidget(self.botonStop)
        left_layout.addWidget(self.botonValidar)
        left_layout.addWidget(self.ultima_vez_label)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.total_horas_label)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.tiempo_inicial = None
        self.tiempo_pausado = 0
        self.cronometro_activo = False

        self.load_data()

    def start_cronometro(self):
        if not self.cronometro_activo:
            self.tiempo_inicial = time.time() - self.tiempo_pausado
            self.cronometro_activo = True
            self.actualizar_cronometro()

    def stop_cronometro(self):
        if self.cronometro_activo:
            self.cronometro_activo = False
            tiempo_transcurrido = time.time() - self.tiempo_inicial
            horas_estudio = tiempo_transcurrido / 3600
            self.tiempo_pausado = tiempo_transcurrido

            # Guardar solo el último registro de horas de estudio en el archivo de registro
            self.guardar_horas_estudio(horas_estudio)

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
#############################################
# guardar_horas_estudio_V1 
# cuando se registra un dia distinto al presente simplemente no registra nada

    # def guardar_horas_estudio(self, horas):
    #      fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
    #      data = {'fecha': fecha_actual, 'horas': horas}

    #      try:
    #          with open('registro_estudio.json', 'w') as f:
    #              json.dump(data, f)
    #      except FileNotFoundError:
    #          pass  # Opcional: Manejar la excepción si es necesario

    #      self.load_data()


# esta versión ya registra nuevos días en el json. Pero en el día presente no modifica el primer registro ya que imprime:
#                                                          Ya existe un registro para la fecha actual
# ahora lo que hay que hacer es que cuando las fechas sí coincidan se ejecute la V1 de la funcion guardar_horas_estudio
# o simplemente hacer que para la fecha actual sí se reescriba cada que se le de stop y start.

    def guardar_horas_estudio(self, horas):
        fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')
        registro_nuevo = {'fecha': fecha_actual, 'horas': horas}

        # Crear la estructura de datos si el archivo no existe o está vacío
        if not os.path.exists('registro_estudio.json') or os.path.getsize('registro_estudio.json') == 0:
            data = {'fechas_y_horas': [registro_nuevo]}
        else:
            try:
                with open('registro_estudio.json', 'r') as f:
                    data = json.load(f)
            except Exception as e:
                print('Error al leer el archivo:', e)
                return

            # Verificar si ya hay un registro para la fecha actual
            for registro in data['fechas_y_horas']:
                if registro['fecha'] == fecha_actual:
                    print('Ya existe un registro para la fecha actual.')
                    return
            
            # Agregar el nuevo registro a la lista
            data['fechas_y_horas'].append(registro_nuevo)

        # Guardar los datos actualizados en el archivo JSON
        try:
            with open('registro_estudio.json', 'w') as f:
                json.dump(data, f, indent=2)
                print('Registro guardado exitosamente.')
        except Exception as e:
            print('Error al guardar el registro:', e)

        self.load_data()
###########################################
# esta versión no soporta la estructura de datos del json
    # def load_data(self):
    #     try:
    #         with open('registro_estudio.json', 'r') as f:
    #             data = json.load(f)
    #             if data:
    #                 self.ultima_vez_label.setText(f'Última vez ({data["fecha"]}): {data["horas"]:.2f} horas')
    #             else:
    #                 self.ultima_vez_label.setText('No hay registros')
    #     except FileNotFoundError:
    #         self.ultima_vez_label.setText('No hay registros')

# Esta load_data() ya soporta la estructura de datos nueva en el json
    def load_data(self):
        try:
            with open('registro_estudio.json', 'r') as f:
                data = json.load(f)
                if data and 'fechas_y_horas' in data:
                    ultimo_registro = data['fechas_y_horas'][-1]  # Obtener el último registro de la lista
                    fecha = ultimo_registro['fecha']
                    horas = ultimo_registro['horas']
                    self.ultima_vez_label.setText(f'Última vez ({fecha}): {horas:.2f} horas')
                else:
                    self.ultima_vez_label.setText('No hay registros')
        except FileNotFoundError:
            self.ultima_vez_label.setText('No hay registros')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Cronometro()
    ventana.show()
    sys.exit(app.exec_())


